"""
ScreenSolver AI - Arquivo Principal
====================================
Orquestra todos os módulos e gerencia o fluxo da aplicação.

Fluxo:
1. Usuário pressiona F8
2. Captura área da tela
3. Extrai texto com OCR
4. Envia para modelo Ollama
5. Exibe resposta na overlay

Autor: ScreenSolver AI Team
Versão: 1.0.0
"""

import logging
import threading
import time
import sys
from typing import Optional

# Importa módulos do projeto
import config
from utils import logger, cache, history, save_screenshot, validate_ollama_connection, validate_tesseract_installation
from capture import capture_selected_area
from ocr import process_image_to_text
from ollama_client import OllamaClient, validate_ollama_setup
from overlay import ScreenSolverOverlay

# Importa biblioteca de hotkey
import keyboard

# ============================================================================
# CLASSE PRINCIPAL
# ============================================================================

class ScreenSolverApp:
    """
    Aplicação principal do ScreenSolver AI.
    
    Gerencia:
    - Hotkeys
    - Fluxo de captura -> OCR -> IA
    - Interface gráfica
    - Threading para não travar
    """
    
    def __init__(self):
        """Inicializa a aplicação."""
        logger.info("=" * 60)
        logger.info("ScreenSolver AI - Inicializando")
        logger.info("=" * 60)
        
        # Componentes
        self.overlay: Optional[ScreenSolverOverlay] = None
        self.ollama_client: Optional[OllamaClient] = None
        
        # Estado
        self.is_processing = False
        self.last_hotkey_time = 0
        
        # Inicializa componentes
        self._initialize()
    
    def _initialize(self):
        """Inicializa todos os componentes."""
        
        # Valida dependências
        logger.info("Validando dependências...")
        
        if not validate_tesseract_installation():
            logger.warning("Tesseract OCR não encontrado!")
            logger.warning("O OCR não funcionará. Instale o Tesseract para usar essa funcionalidade.")
            logger.warning("Download: https://github.com/UB-Mannheim/tesseract/wiki")
        
        if not validate_ollama_connection():
            logger.error("Ollama não está rodando!")
            logger.error("Inicie o Ollama antes de executar o ScreenSolver AI.")
            sys.exit(1)
        
        logger.info("✓ Dependências validadas")
        
        # Valida configuração do Ollama
        logger.info("Validando configuração do Ollama...")
        
        if not validate_ollama_setup():
            logger.error("Configuração do Ollama inválida!")
            logger.error(f"Certifique-se de que o modelo {config.OLLAMA_MODEL} está instalado.")
            logger.error(f"Execute: ollama pull {config.OLLAMA_MODEL}")
            sys.exit(1)
        
        logger.info("✓ Ollama configurado corretamente")
        
        # Cria cliente Ollama
        self.ollama_client = OllamaClient()
        logger.info("✓ Cliente Ollama criado")
        
        # Cria interface
        self.overlay = ScreenSolverOverlay()
        logger.info("✓ Interface criada")
        
        # Registra hotkeys
        self._register_hotkeys()
        logger.info("✓ Hotkeys registradas")
        
        logger.info("=" * 60)
        logger.info("ScreenSolver AI pronto para uso!")
        logger.info(f"Pressione {config.HOTKEY_CAPTURE.upper()} para capturar tela")
        logger.info("=" * 60)
    
    def _register_hotkeys(self):
        """Registra as hotkeys do sistema."""
        
        # Hotkey para captura (F8)
        keyboard.add_hotkey(
            config.HOTKEY_CAPTURE,
            self._on_capture_hotkey,
            suppress=True
        )
        
        logger.info(f"Hotkey registrada: {config.HOTKEY_CAPTURE.upper()} -> Capturar tela")
    
    def _on_capture_hotkey(self):
        """Callback quando F8 é pressionado."""
        
        # Debounce: evita múltiplos triggers rápidos
        current_time = time.time()
        if current_time - self.last_hotkey_time < config.HOTKEY_DEBOUNCE:
            logger.debug("Hotkey ignorada (debounce)")
            return
        
        self.last_hotkey_time = current_time
        
        # Verifica se já está processando
        if self.is_processing:
            logger.warning("Já existe um processamento em andamento")
            self.overlay.show_error("Aguarde o processamento atual terminar")
            return
        
        # Inicia processamento em thread separada
        logger.info("Hotkey F8 detectada - Iniciando captura")
        
        if config.USE_THREADING:
            thread = threading.Thread(target=self._process_capture, daemon=True)
            thread.start()
        else:
            self._process_capture()
    
    def _process_capture(self):
        """
        Processa captura completa: captura -> OCR -> IA -> exibição.
        
        Este é o fluxo principal da aplicação.
        """
        self.is_processing = True
        
        try:
            # ================================================================
            # ETAPA 1: CAPTURA DE TELA
            # ================================================================
            
            logger.info("ETAPA 1/4: Captura de tela")
            self.overlay.set_status("📸 Selecione a área da tela...", "#3b82f6")
            
            screenshot = capture_selected_area()
            
            if screenshot is None:
                logger.warning("Captura cancelada ou falhou")
                self.overlay.set_status("Aguardando... (Pressione F8)", "#888888")
                return
            
            logger.info("✓ Captura concluída")
            
            # Salva screenshot
            screenshot_path = save_screenshot(screenshot)
            
            # ================================================================
            # ETAPA 2: OCR (EXTRAÇÃO DE TEXTO)
            # ================================================================
            
            logger.info("ETAPA 2/4: Extração de texto (OCR)")
            self.overlay.show_loading("🔍 Extraindo texto da imagem...")
            
            question_text = process_image_to_text(screenshot)
            
            if question_text is None or not question_text.strip():
                logger.error("Falha ao extrair texto")
                self.overlay.hide_loading()
                self.overlay.show_error(
                    "Não foi possível extrair texto da imagem.\n"
                    "Tente capturar uma área com texto mais claro."
                )
                return
            
            logger.info(f"✓ Texto extraído: {len(question_text)} caracteres")
            
            # Atualiza interface com questão
            self.overlay.set_question(question_text)
            self.overlay.tabview.set("📝 Questão")
            
            # ================================================================
            # ETAPA 3: VERIFICAR CACHE
            # ================================================================
            
            logger.info("ETAPA 3/4: Verificando cache")
            
            cached_answer = cache.get(question_text)
            
            if cached_answer:
                logger.info("✓ Resposta encontrada no cache!")
                self.overlay.set_answer(cached_answer)
                self.overlay.tabview.set("💡 Resposta")
                self.overlay.hide_loading()
                return
            
            logger.info("Cache miss - Consultando modelo")
            
            # ================================================================
            # ETAPA 4: CONSULTAR MODELO OLLAMA
            # ================================================================
            
            logger.info("ETAPA 4/4: Consultando modelo Ollama")
            self.overlay.show_loading(f"🤖 Consultando {config.OLLAMA_MODEL}...")
            
            answer = self.ollama_client.generate_answer(question_text)
            
            if answer is None or not answer.strip():
                logger.error("Falha ao gerar resposta")
                self.overlay.hide_loading()
                self.overlay.show_error(
                    "Não foi possível obter resposta do modelo.\n"
                    "Verifique se o Ollama está rodando corretamente."
                )
                return
            
            logger.info(f"✓ Resposta recebida: {len(answer)} caracteres")
            
            # ================================================================
            # FINALIZAÇÃO
            # ================================================================
            
            # Armazena no cache
            cache.set(question_text, answer)
            
            # Adiciona ao histórico
            history.add_entry(
                question=question_text,
                response=answer,
                screenshot_path=str(screenshot_path) if screenshot_path else None
            )
            
            # Atualiza interface
            self.overlay.set_answer(answer)
            self.overlay.tabview.set("💡 Resposta")
            self.overlay.update_history_display()
            self.overlay.hide_loading()
            
            logger.info("=" * 60)
            logger.info("✓ Processamento concluído com sucesso!")
            logger.info("=" * 60)
        
        except Exception as e:
            logger.error(f"Erro durante processamento: {e}", exc_info=True)
            self.overlay.hide_loading()
            self.overlay.show_error(f"Erro inesperado: {str(e)}")
        
        finally:
            self.is_processing = False
    
    def run(self):
        """Inicia a aplicação."""
        try:
            # Inicia loop da interface
            self.overlay.run()
        
        except KeyboardInterrupt:
            logger.info("Aplicação interrompida pelo usuário")
        
        except Exception as e:
            logger.error(f"Erro fatal: {e}", exc_info=True)
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Limpa recursos antes de fechar."""
        logger.info("Limpando recursos...")
        
        # Remove hotkeys
        try:
            keyboard.unhook_all()
            logger.info("✓ Hotkeys removidas")
        except:
            pass
        
        logger.info("=" * 60)
        logger.info("ScreenSolver AI encerrado")
        logger.info("=" * 60)

# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

def main():
    """Função principal."""
    
    # Banner
    print("=" * 60)
    print("  ____                           ____        _                ")
    print(" / ___|  ___ _ __ ___  ___ _ __ / ___|  ___ | |_   _____ _ __ ")
    print(" \\___ \\ / __| '__/ _ \\/ _ \\ '_ \\\\___ \\ / _ \\| \\ \\ / / _ \\ '__|")
    print("  ___) | (__| | |  __/  __/ | | |___) | (_) | |\\ V /  __/ |   ")
    print(" |____/ \\___|_|  \\___|\\___|_| |_|____/ \\___/|_| \\_/ \\___|_|   ")
    print("                                                               ")
    print("                      AI - Versão 1.0.0                        ")
    print("=" * 60)
    print()
    print("🤖 Assistente inteligente para resolver questões da tela")
    print()
    print("Instruções:")
    print("  1. Pressione F8 para capturar uma área da tela")
    print("  2. Selecione a área com a questão")
    print("  3. Aguarde a resposta do modelo")
    print("  4. Pressione ESC para cancelar a seleção")
    print()
    print("=" * 60)
    print()
    
    # Cria e executa aplicação
    app = ScreenSolverApp()
    app.run()

if __name__ == "__main__":
    main()
