"""
ScreenSolver AI - Módulo de OCR
================================
Responsável por extrair texto de imagens usando Tesseract OCR.

Funcionalidades:
- Pré-processamento de imagem para melhor precisão
- Extração de texto otimizada
- Tratamento de erros robusto
"""

import logging
from pathlib import Path
from typing import Optional
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import cv2
import numpy as np
import config

if Path(config.TESSERACT_CMD).exists():
    pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD

logger = logging.getLogger(__name__)

def get_available_ocr_language() -> str:
    """
    Retorna o melhor idioma disponível para OCR.
    
    Usa português + inglês quando ambos existem. Se o pacote português
    não estiver instalado no Tesseract, usa inglês como fallback para
    evitar falhas durante a execução.
    """
    try:
        available_languages = pytesseract.get_languages(config='')
        requested_languages = config.TESSERACT_LANG.split("+")
        usable_languages = [lang for lang in requested_languages if lang in available_languages]
        
        if usable_languages:
            selected_language = "+".join(usable_languages)
            logger.info(f"Idioma OCR selecionado: {selected_language}")
            return selected_language
        
        if "eng" in available_languages:
            logger.warning("Idioma português do Tesseract não encontrado. Usando fallback: eng")
            return "eng"
        
        logger.warning("Nenhum idioma preferido encontrado. Usando configuração padrão do Tesseract.")
        return ""
    except Exception as e:
        logger.warning(f"Não foi possível detectar idiomas do Tesseract: {e}")
        return "eng"

# ============================================================================
# PRÉ-PROCESSAMENTO DE IMAGEM
# ============================================================================

def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Aplica pré-processamento na imagem para melhorar OCR.
    
    Etapas:
    1. Upscale (aumenta resolução)
    2. Grayscale (converte para tons de cinza)
    3. Sharpen (aumenta nitidez)
    4. Threshold (binarização)
    
    Args:
        image: Imagem PIL original
        
    Returns:
        Imagem PIL processada
    """
    try:
        logger.debug("Iniciando pré-processamento da imagem")
        
        # Etapa 1: Upscale para melhorar precisão
        if config.OCR_UPSCALE_FACTOR > 1.0:
            new_size = (
                int(image.width * config.OCR_UPSCALE_FACTOR),
                int(image.height * config.OCR_UPSCALE_FACTOR)
            )
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            logger.debug(f"Imagem redimensionada para: {new_size}")
        
        # Etapa 2: Converte para grayscale
        image = image.convert('L')
        logger.debug("Imagem convertida para grayscale")
        
        # Etapa 3: Aumenta nitidez
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)  # Fator de nitidez
        logger.debug("Nitidez aumentada")
        
        # Etapa 4: Aplica filtro de nitidez adicional
        image = image.filter(ImageFilter.SHARPEN)
        
        # Etapa 5: Binarização (threshold)
        # Converte PIL para numpy array para usar OpenCV
        img_array = np.array(image)
        
        # Aplica threshold adaptativo (melhor para diferentes iluminações)
        img_array = cv2.adaptiveThreshold(
            img_array,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,  # Tamanho do bloco
            2    # Constante subtraída da média
        )
        
        # Converte de volta para PIL
        image = Image.fromarray(img_array)
        logger.debug("Threshold aplicado")
        
        # Etapa 6: Remove ruído (opcional)
        img_array = cv2.medianBlur(np.array(image), 3)
        image = Image.fromarray(img_array)
        logger.debug("Ruído removido")
        
        logger.info("Pré-processamento concluído com sucesso")
        
        # Salva imagem processada se modo debug ativo
        if config.SAVE_PROCESSED_IMAGES:
            debug_path = config.SCREENSHOTS_DIR / "debug_processed.png"
            image.save(debug_path)
            logger.debug(f"Imagem processada salva em: {debug_path}")
        
        return image
    
    except Exception as e:
        logger.error(f"Erro no pré-processamento: {e}", exc_info=True)
        # Retorna imagem original em caso de erro
        return image.convert('L')

# ============================================================================
# EXTRAÇÃO DE TEXTO
# ============================================================================

def extract_text(image: Image.Image, preprocess: bool = True) -> Optional[str]:
    """
    Extrai texto de uma imagem usando Tesseract OCR.
    
    Args:
        image: Imagem PIL
        preprocess: Se True, aplica pré-processamento
        
    Returns:
        Texto extraído ou None em caso de erro
    """
    try:
        logger.info("Iniciando extração de texto (OCR)")
        
        # Aplica pré-processamento se solicitado
        if preprocess:
            image = preprocess_image(image)
        
        # Extrai texto usando Tesseract
        logger.debug(f"Executando Tesseract com config: {config.TESSERACT_CONFIG}")
        
        text = pytesseract.image_to_string(
            image,
            lang=get_available_ocr_language(),
            config=config.TESSERACT_CONFIG
        )
        
        # Limpa o texto extraído
        text = text.strip()
        
        if not text:
            logger.warning("Nenhum texto detectado na imagem")
            return None
        
        logger.info(f"Texto extraído com sucesso ({len(text)} caracteres)")
        logger.debug(f"Texto extraído (preview): {text[:100]}...")
        
        return text
    
    except pytesseract.TesseractNotFoundError:
        logger.warning(
            "Tesseract não encontrado! "
            "Retornando mensagem padrão. "
            "Instale o Tesseract para usar OCR: https://github.com/UB-Mannheim/tesseract/wiki"
        )
        return "[OCR não disponível - Tesseract não instalado]\n\nPor favor, digite sua questão manualmente ou instale o Tesseract OCR."
    
    except Exception as e:
        logger.error(f"Erro ao extrair texto: {e}", exc_info=True)
        return None

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def get_text_confidence(image: Image.Image) -> float:
    """
    Calcula a confiança média do OCR.
    
    Args:
        image: Imagem PIL
        
    Returns:
        Confiança média (0-100)
    """
    try:
        data = pytesseract.image_to_data(
            image,
            lang=get_available_ocr_language(),
            output_type=pytesseract.Output.DICT
        )
        
        # Filtra apenas palavras com confiança válida
        confidences = [
            int(conf) for conf in data['conf']
            if conf != '-1' and conf.isdigit()
        ]
        
        if not confidences:
            return 0.0
        
        avg_confidence = sum(confidences) / len(confidences)
        logger.debug(f"Confiança média do OCR: {avg_confidence:.2f}%")
        
        return avg_confidence
    
    except Exception as e:
        logger.error(f"Erro ao calcular confiança: {e}")
        return 0.0

def detect_text_regions(image: Image.Image) -> list:
    """
    Detecta regiões com texto na imagem.
    
    Args:
        image: Imagem PIL
        
    Returns:
        Lista de bounding boxes (x, y, w, h)
    """
    try:
        data = pytesseract.image_to_data(
            image,
            lang=get_available_ocr_language(),
            output_type=pytesseract.Output.DICT
        )
        
        regions = []
        n_boxes = len(data['text'])
        
        for i in range(n_boxes):
            # Filtra apenas palavras com confiança > 60
            if int(data['conf'][i]) > 60:
                x, y, w, h = (
                    data['left'][i],
                    data['top'][i],
                    data['width'][i],
                    data['height'][i]
                )
                regions.append((x, y, w, h))
        
        logger.debug(f"Detectadas {len(regions)} regiões com texto")
        return regions
    
    except Exception as e:
        logger.error(f"Erro ao detectar regiões: {e}")
        return []

def validate_text(text: str) -> bool:
    """
    Valida se o texto extraído é válido.
    
    Args:
        text: Texto a validar
        
    Returns:
        True se válido, False caso contrário
    """
    if not text or len(text.strip()) < 3:
        logger.warning("Texto muito curto ou vazio")
        return False
    
    # Verifica se tem pelo menos algumas letras
    letter_count = sum(c.isalpha() for c in text)
    if letter_count < 3:
        logger.warning("Texto não contém letras suficientes")
        return False
    
    return True

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def process_image_to_text(image: Image.Image) -> Optional[str]:
    """
    Processa uma imagem e extrai texto com validação.
    
    Pipeline completo:
    1. Pré-processamento
    2. Extração de texto
    3. Validação
    4. Cálculo de confiança
    
    Args:
        image: Imagem PIL
        
    Returns:
        Texto extraído e validado ou None
    """
    logger.info("=" * 60)
    logger.info("Processando imagem para extração de texto")
    logger.info("=" * 60)
    
    # Extrai texto
    text = extract_text(image, preprocess=True)
    
    if text is None:
        logger.error("Falha na extração de texto")
        return None
    
    # Valida texto
    if not validate_text(text):
        logger.error("Texto extraído não passou na validação")
        return None
    
    # Calcula confiança
    confidence = get_text_confidence(image)
    logger.info(f"Confiança do OCR: {confidence:.2f}%")
    
    if confidence < 30:
        logger.warning("Confiança do OCR muito baixa, resultado pode ser impreciso")
    
    logger.info("Processamento de texto concluído com sucesso")
    return text

# ============================================================================
# TESTES
# ============================================================================

if __name__ == "__main__":
    """Teste do módulo de OCR."""
    
    # Configura logging para teste
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    
    print("Teste do módulo de OCR")
    print("\nCriando imagem de teste...")
    
    # Cria uma imagem de teste com texto
    from PIL import ImageDraw, ImageFont
    
    test_img = Image.new('RGB', (800, 200), color='white')
    draw = ImageDraw.Draw(test_img)
    
    # Adiciona texto
    text = "Quanto é 2 + 2?"
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 80), text, fill='black', font=font)
    
    print("Imagem de teste criada")
    print("\nExtraindo texto...")
    
    # Testa extração
    extracted = process_image_to_text(test_img)
    
    if extracted:
        print(f"\n✓ Texto extraído: '{extracted}'")
    else:
        print("\n✗ Falha na extração")
