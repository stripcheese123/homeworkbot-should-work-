"""
ScreenSolver AI - Arquivo de Configuração
==========================================
Todas as configurações centralizadas do projeto.
Facilita manutenção e personalização.
"""

import os
from pathlib import Path

# ============================================================================
# CONFIGURAÇÕES DO OLLAMA
# ============================================================================

# Endpoint da API local do Ollama
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_GENERATE_ENDPOINT = f"{OLLAMA_BASE_URL}/api/generate"

# Modelo a ser utilizado (otimizado para RTX 4060)
OLLAMA_MODEL = "qwen3.5:9b"

# Timeout para requisições (em segundos)
OLLAMA_TIMEOUT = 120

# Configurações de geração do modelo
OLLAMA_OPTIONS = {
    "temperature": 0.7,      # Criatividade moderada
    "top_p": 0.9,            # Nucleus sampling
    "top_k": 40,             # Top-k sampling
    "num_gpu": 1,            # Usar GPU NVIDIA RTX 4060
    "num_thread": 8,         # Threads da CPU
}

# ============================================================================
# CONFIGURAÇÕES DE HOTKEYS
# ============================================================================

# Tecla para iniciar captura de tela
HOTKEY_CAPTURE = "f8"

# Tecla para cancelar captura
HOTKEY_CANCEL = "esc"

# ============================================================================
# CONFIGURAÇÕES DE OCR
# ============================================================================

# Idioma do Tesseract (português + inglês)
TESSERACT_LANG = "por+eng"
TESSERACT_CMD = os.environ.get("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")

# Configurações personalizadas do Tesseract
# --psm 6: Assume um único bloco uniforme de texto
# --oem 3: Usa LSTM neural network (melhor precisão)
TESSERACT_CONFIG = r"--psm 6 --oem 3"

# Fator de upscale da imagem antes do OCR (melhora precisão)
OCR_UPSCALE_FACTOR = 2.0

# Threshold para binarização da imagem
OCR_THRESHOLD_VALUE = 150

# ============================================================================
# CONFIGURAÇÕES DE INTERFACE
# ============================================================================

# Tema da interface
UI_THEME = "dark-blue"

# Cor de fundo da overlay
UI_BG_COLOR = "#1a1a1a"

# Cor do texto
UI_TEXT_COLOR = "#ffffff"

# Cor de destaque
UI_ACCENT_COLOR = "#3b82f6"

# Transparência da janela (0.0 a 1.0)
UI_ALPHA = 0.95

# Tamanho da janela overlay
UI_WIDTH = 600
UI_HEIGHT = 500

# ============================================================================
# CONFIGURAÇÕES DE DIRETÓRIOS
# ============================================================================

# Diretório raiz do projeto
PROJECT_ROOT = Path(__file__).parent

# Diretório para screenshots salvos
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Diretório para histórico
HISTORY_DIR = PROJECT_ROOT / "history"
HISTORY_DIR.mkdir(exist_ok=True)

# Diretório para logs
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Arquivo de log
LOG_FILE = LOGS_DIR / "screensolver.log"

# ============================================================================
# CONFIGURAÇÕES DE CACHE
# ============================================================================

# Habilitar cache de respostas
ENABLE_CACHE = True

# Tamanho máximo do cache (número de entradas)
CACHE_MAX_SIZE = 50

# ============================================================================
# CONFIGURAÇÕES DE HISTÓRICO
# ============================================================================

# Número máximo de itens no histórico
MAX_HISTORY_ITEMS = 20

# Salvar screenshots automaticamente
AUTO_SAVE_SCREENSHOTS = True

# ============================================================================
# PROMPT DO MODELO
# ============================================================================

SYSTEM_PROMPT = """Você é um tutor extremamente inteligente e didático.

Sua missão é ajudar estudantes a entender questões e problemas de qualquer área do conhecimento.

INSTRUÇÕES:
1. Leia atentamente a questão extraída da tela do usuário
2. Identifique automaticamente a matéria/área (matemática, física, química, programação, etc.)
3. Explique o raciocínio passo a passo de forma clara e detalhada
4. Se for matemática: resolva mostrando cada etapa do cálculo
5. Se for física: explique as fórmulas e conceitos envolvidos
6. Se for química: detalhe as reações e processos
7. Se for programação: explique a lógica e o código linha por linha
8. Se houver múltipla escolha: analise cada alternativa explicando por que está certa ou errada
9. Use linguagem clara e acessível
10. Sempre responda em português brasileiro

FORMATO DA RESPOSTA:
- Comece identificando o tipo de questão
- Apresente a solução de forma estruturada
- Use exemplos quando necessário
- Destaque pontos importantes

Questão extraída:
{question}

Sua resposta detalhada:"""

# ============================================================================
# CONFIGURAÇÕES DE PERFORMANCE
# ============================================================================

# Usar threading para não travar a interface
USE_THREADING = True

# Delay para debounce da hotkey (em segundos)
HOTKEY_DEBOUNCE = 0.5

# Qualidade da compressão de imagem (1-100)
IMAGE_QUALITY = 85

# ============================================================================
# CONFIGURAÇÕES DE DEBUG
# ============================================================================

# Modo debug (mostra mais informações no console)
DEBUG_MODE = False

# Salvar imagens processadas para debug
SAVE_PROCESSED_IMAGES = False
