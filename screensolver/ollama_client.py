"""
ScreenSolver AI - Cliente Ollama
=================================
Responsável pela comunicação com o modelo Ollama local.

Funcionalidades:
- Envio de prompts para o modelo qwen3:59b
- Streaming de respostas
- Tratamento de erros e timeouts
- Otimização para GPU NVIDIA RTX 4060
"""

import logging
import requests
import json
from typing import Optional, Callable, Generator
import config

logger = logging.getLogger(__name__)

# ============================================================================
# CLASSE CLIENTE OLLAMA
# ============================================================================

class OllamaClient:
    """
    Cliente para interação com a API do Ollama.
    
    Gerencia requisições, streaming e tratamento de erros.
    """
    
    def __init__(self):
        """Inicializa o cliente Ollama."""
        self.base_url = config.OLLAMA_BASE_URL
        self.generate_url = config.OLLAMA_GENERATE_ENDPOINT
        self.model = config.OLLAMA_MODEL
        self.timeout = config.OLLAMA_TIMEOUT
        
        logger.info(f"OllamaClient inicializado")
        logger.info(f"  Endpoint: {self.generate_url}")
        logger.info(f"  Modelo: {self.model}")
        logger.info(f"  Timeout: {self.timeout}s")
    
    def check_connection(self) -> bool:
        """
        Verifica se o Ollama está rodando e acessível.
        
        Returns:
            True se conectado, False caso contrário
        """
        try:
            logger.debug("Verificando conexão com Ollama...")
            response = requests.get(self.base_url, timeout=5)
            
            if response.status_code == 200:
                logger.info("✓ Ollama está rodando e acessível")
                return True
            else:
                logger.error(f"✗ Ollama retornou status: {response.status_code}")
                return False
        
        except requests.exceptions.ConnectionError:
            logger.error("✗ Não foi possível conectar ao Ollama. Certifique-se de que está rodando.")
            return False
        
        except Exception as e:
            logger.error(f"✗ Erro ao verificar conexão: {e}")
            return False
    
    def check_model(self) -> bool:
        """
        Verifica se o modelo está disponível.
        
        Returns:
            True se modelo disponível, False caso contrário
        """
        try:
            logger.debug(f"Verificando disponibilidade do modelo {self.model}...")
            
            # Lista modelos disponíveis
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            
            if response.status_code != 200:
                logger.error("Erro ao listar modelos")
                return False
            
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            
            if self.model in models:
                logger.info(f"✓ Modelo {self.model} está disponível")
                return True
            else:
                logger.error(f"✗ Modelo {self.model} não encontrado")
                logger.info(f"Modelos disponíveis: {', '.join(models)}")
                return False
        
        except Exception as e:
            logger.error(f"Erro ao verificar modelo: {e}")
            return False
    
    def generate(
        self,
        prompt: str,
        stream: bool = False,
        callback: Optional[Callable[[str], None]] = None
    ) -> Optional[str]:
        """
        Gera resposta do modelo para um prompt.
        
        Args:
            prompt: Texto do prompt
            stream: Se True, usa streaming
            callback: Função chamada a cada chunk (apenas se stream=True)
            
        Returns:
            Resposta completa do modelo ou None em caso de erro
        """
        try:
            logger.info("=" * 60)
            logger.info("Enviando prompt para o modelo")
            logger.info("=" * 60)
            logger.debug(f"Prompt (preview): {prompt[:200]}...")
            
            # Prepara payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream,
                "options": config.OLLAMA_OPTIONS
            }
            
            # Faz requisição
            logger.info("Aguardando resposta do modelo...")
            
            if stream:
                return self._generate_stream(payload, callback)
            else:
                return self._generate_blocking(payload)
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout após {self.timeout}s aguardando resposta do modelo")
            return None
        
        except requests.exceptions.ConnectionError:
            logger.error("Erro de conexão com Ollama. Verifique se está rodando.")
            return None
        
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}", exc_info=True)
            return None
    
    def _generate_blocking(self, payload: dict) -> Optional[str]:
        """
        Gera resposta sem streaming (bloqueante).
        
        Args:
            payload: Dados da requisição
            
        Returns:
            Resposta completa
        """
        response = requests.post(
            self.generate_url,
            json=payload,
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            logger.error(f"Erro na requisição: {response.status_code}")
            logger.error(f"Resposta: {response.text}")
            return None
        
        data = response.json()
        answer = data.get('response', '').strip()
        
        logger.info(f"Resposta recebida ({len(answer)} caracteres)")
        logger.debug(f"Resposta (preview): {answer[:200]}...")
        
        return answer
    
    def _generate_stream(
        self,
        payload: dict,
        callback: Optional[Callable[[str], None]]
    ) -> Optional[str]:
        """
        Gera resposta com streaming.
        
        Args:
            payload: Dados da requisição
            callback: Função chamada a cada chunk
            
        Returns:
            Resposta completa
        """
        full_response = ""
        
        with requests.post(
            self.generate_url,
            json=payload,
            timeout=self.timeout,
            stream=True
        ) as response:
            
            if response.status_code != 200:
                logger.error(f"Erro na requisição: {response.status_code}")
                return None
            
            # Processa cada chunk
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        chunk = data.get('response', '')
                        
                        if chunk:
                            full_response += chunk
                            
                            # Chama callback se fornecido
                            if callback:
                                callback(chunk)
                        
                        # Verifica se terminou
                        if data.get('done', False):
                            logger.info("Streaming concluído")
                            break
                    
                    except json.JSONDecodeError:
                        logger.warning(f"Erro ao decodificar chunk: {line}")
                        continue
        
        logger.info(f"Resposta completa recebida ({len(full_response)} caracteres)")
        return full_response
    
    def generate_answer(self, question: str) -> Optional[str]:
        """
        Gera resposta para uma questão usando o prompt do sistema.
        
        Args:
            question: Texto da questão extraída
            
        Returns:
            Resposta do modelo
        """
        # Formata prompt usando template do config
        prompt = config.SYSTEM_PROMPT.format(question=question)
        
        # Gera resposta
        return self.generate(prompt, stream=False)
    
    def generate_answer_stream(
        self,
        question: str,
        callback: Callable[[str], None]
    ) -> Optional[str]:
        """
        Gera resposta com streaming para uma questão.
        
        Args:
            question: Texto da questão extraída
            callback: Função chamada a cada chunk
            
        Returns:
            Resposta completa do modelo
        """
        # Formata prompt usando template do config
        prompt = config.SYSTEM_PROMPT.format(question=question)
        
        # Gera resposta com streaming
        return self.generate(prompt, stream=True, callback=callback)

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def validate_ollama_setup() -> bool:
    """
    Valida se o Ollama está configurado corretamente.
    
    Verifica:
    1. Ollama está rodando
    2. Modelo está disponível
    
    Returns:
        True se tudo OK, False caso contrário
    """
    logger.info("Validando configuração do Ollama...")
    
    client = OllamaClient()
    
    # Verifica conexão
    if not client.check_connection():
        logger.error("Falha na validação: Ollama não está rodando")
        return False
    
    # Verifica modelo
    if not client.check_model():
        logger.error(f"Falha na validação: Modelo {config.OLLAMA_MODEL} não disponível")
        return False
    
    logger.info("✓ Ollama configurado corretamente!")
    return True

def get_available_models() -> list:
    """
    Lista modelos disponíveis no Ollama.
    
    Returns:
        Lista de nomes de modelos
    """
    try:
        response = requests.get(
            f"{config.OLLAMA_BASE_URL}/api/tags",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        
        return []
    
    except Exception as e:
        logger.error(f"Erro ao listar modelos: {e}")
        return []

# ============================================================================
# TESTES
# ============================================================================

if __name__ == "__main__":
    """Teste do cliente Ollama."""
    
    # Configura logging para teste
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    
    print("=" * 60)
    print("Teste do Cliente Ollama")
    print("=" * 60)
    
    # Valida setup
    print("\n1. Validando configuração...")
    if not validate_ollama_setup():
        print("✗ Configuração inválida. Verifique se o Ollama está rodando.")
        exit(1)
    
    # Lista modelos
    print("\n2. Listando modelos disponíveis...")
    models = get_available_models()
    print(f"Modelos: {', '.join(models)}")
    
    # Testa geração
    print("\n3. Testando geração de resposta...")
    client = OllamaClient()
    
    test_question = "Quanto é 2 + 2? Explique o cálculo."
    print(f"Questão: {test_question}")
    
    print("\nGerando resposta...")
    answer = client.generate_answer(test_question)
    
    if answer:
        print(f"\n✓ Resposta recebida:\n{answer}")
    else:
        print("\n✗ Falha ao gerar resposta")
    
    print("\n" + "=" * 60)
