"""
ScreenSolver AI - Utilitários
==============================
Funções auxiliares utilizadas em todo o projeto.
"""

import logging
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import config

# ============================================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================================

def setup_logging():
    """
    Configura o sistema de logging do projeto.
    
    Cria logs tanto em arquivo quanto no console.
    Formato: [TIMESTAMP] [LEVEL] Message
    """
    logging.basicConfig(
        level=logging.DEBUG if config.DEBUG_MODE else logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            # Log em arquivo
            logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
            # Log no console
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("ScreenSolver AI iniciado")
    logger.info("=" * 60)
    return logger

# ============================================================================
# CACHE DE RESPOSTAS
# ============================================================================

class ResponseCache:
    """
    Sistema de cache para evitar requisições duplicadas ao modelo.
    
    Usa hash MD5 do texto extraído como chave.
    Implementa LRU (Least Recently Used) para limitar tamanho.
    """
    
    def __init__(self, max_size: int = config.CACHE_MAX_SIZE):
        """
        Inicializa o cache.
        
        Args:
            max_size: Número máximo de entradas no cache
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.access_order = []  # Para implementar LRU
        self.logger = logging.getLogger(__name__)
    
    def _generate_key(self, text: str) -> str:
        """
        Gera uma chave única para o texto.
        
        Args:
            text: Texto a ser hasheado
            
        Returns:
            Hash MD5 do texto
        """
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def get(self, text: str) -> Optional[str]:
        """
        Busca uma resposta no cache.
        
        Args:
            text: Texto da questão
            
        Returns:
            Resposta em cache ou None se não encontrada
        """
        if not config.ENABLE_CACHE:
            return None
        
        key = self._generate_key(text)
        
        if key in self.cache:
            # Atualiza ordem de acesso (LRU)
            self.access_order.remove(key)
            self.access_order.append(key)
            
            self.logger.info(f"Cache HIT para questão (key: {key[:8]}...)")
            return self.cache[key]['response']
        
        self.logger.info(f"Cache MISS para questão (key: {key[:8]}...)")
        return None
    
    def set(self, text: str, response: str):
        """
        Armazena uma resposta no cache.
        
        Args:
            text: Texto da questão
            response: Resposta do modelo
        """
        if not config.ENABLE_CACHE:
            return
        
        key = self._generate_key(text)
        
        # Remove item mais antigo se cache estiver cheio
        if len(self.cache) >= self.max_size and key not in self.cache:
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
            self.logger.info(f"Cache cheio. Removido item antigo (key: {oldest_key[:8]}...)")
        
        # Adiciona ao cache
        self.cache[key] = {
            'text': text,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        
        # Atualiza ordem de acesso
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)
        
        self.logger.info(f"Resposta armazenada no cache (key: {key[:8]}...)")
    
    def clear(self):
        """Limpa todo o cache."""
        self.cache.clear()
        self.access_order.clear()
        self.logger.info("Cache limpo")

# ============================================================================
# HISTÓRICO DE RESPOSTAS
# ============================================================================

class HistoryManager:
    """
    Gerencia o histórico de questões e respostas.
    
    Salva em arquivo JSON para persistência entre sessões.
    """
    
    def __init__(self, max_items: int = config.MAX_HISTORY_ITEMS):
        """
        Inicializa o gerenciador de histórico.
        
        Args:
            max_items: Número máximo de itens no histórico
        """
        self.max_items = max_items
        self.history_file = config.HISTORY_DIR / "history.json"
        self.history = self._load_history()
        self.logger = logging.getLogger(__name__)
    
    def _load_history(self) -> list:
        """
        Carrega histórico do arquivo JSON.
        
        Returns:
            Lista de itens do histórico
        """
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Erro ao carregar histórico: {e}")
                return []
        return []
    
    def _save_history(self):
        """Salva histórico no arquivo JSON."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"Erro ao salvar histórico: {e}")
    
    def add_entry(self, question: str, response: str, screenshot_path: Optional[str] = None):
        """
        Adiciona uma entrada ao histórico.
        
        Args:
            question: Texto da questão
            response: Resposta do modelo
            screenshot_path: Caminho do screenshot (opcional)
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'response': response,
            'screenshot': screenshot_path
        }
        
        # Adiciona no início da lista (mais recente primeiro)
        self.history.insert(0, entry)
        
        # Remove itens excedentes
        if len(self.history) > self.max_items:
            self.history = self.history[:self.max_items]
        
        self._save_history()
        self.logger.info("Nova entrada adicionada ao histórico")
    
    def get_history(self, limit: Optional[int] = None) -> list:
        """
        Retorna o histórico.
        
        Args:
            limit: Número máximo de itens a retornar
            
        Returns:
            Lista de itens do histórico
        """
        if limit:
            return self.history[:limit]
        return self.history
    
    def clear_history(self):
        """Limpa todo o histórico."""
        self.history.clear()
        self._save_history()
        self.logger.info("Histórico limpo")

# ============================================================================
# UTILITÁRIOS DE ARQUIVO
# ============================================================================

def save_screenshot(image, prefix: str = "screenshot") -> Optional[Path]:
    """
    Salva um screenshot no diretório de screenshots.
    
    Args:
        image: Imagem PIL a ser salva
        prefix: Prefixo do nome do arquivo
        
    Returns:
        Caminho do arquivo salvo ou None em caso de erro
    """
    if not config.AUTO_SAVE_SCREENSHOTS:
        return None
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.png"
        filepath = config.SCREENSHOTS_DIR / filename
        
        image.save(filepath, "PNG", quality=config.IMAGE_QUALITY)
        logging.info(f"Screenshot salvo: {filepath}")
        return filepath
    
    except Exception as e:
        logging.error(f"Erro ao salvar screenshot: {e}")
        return None

def format_timestamp(iso_timestamp: str) -> str:
    """
    Formata timestamp ISO para formato legível.
    
    Args:
        iso_timestamp: Timestamp em formato ISO
        
    Returns:
        Timestamp formatado (ex: "06/05/2026 21:32")
    """
    try:
        dt = datetime.fromisoformat(iso_timestamp)
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return iso_timestamp

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Trunca texto longo adicionando reticências.
    
    Args:
        text: Texto a ser truncado
        max_length: Comprimento máximo
        
    Returns:
        Texto truncado
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

# ============================================================================
# VALIDAÇÕES
# ============================================================================

def validate_ollama_connection() -> bool:
    """
    Valida se o Ollama está rodando e acessível.
    
    Returns:
        True se conectado, False caso contrário
    """
    import requests
    
    try:
        response = requests.get(config.OLLAMA_BASE_URL, timeout=5)
        return response.status_code == 200
    except:
        return False

def validate_tesseract_installation() -> bool:
    """
    Valida se o Tesseract está instalado e acessível.
    
    Returns:
        True se instalado, False caso contrário
    """
    import pytesseract
    
    try:
        pytesseract.get_tesseract_version()
        return True
    except:
        return False

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

# Cria logger global
logger = setup_logging()

# Cria instâncias globais
cache = ResponseCache()
history = HistoryManager()
