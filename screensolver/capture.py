"""
ScreenSolver AI - Módulo de Captura de Tela
============================================
Responsável por capturar áreas selecionadas da tela.

Funcionalidades:
- Seleção de área com mouse
- Overlay semi-transparente durante seleção
- Captura otimizada para performance
"""

import logging
from typing import Optional, Tuple
from PIL import Image, ImageGrab
import tkinter as tk
from tkinter import Canvas
import pyautogui

logger = logging.getLogger(__name__)

# ============================================================================
# CLASSE DE SELEÇÃO DE ÁREA
# ============================================================================

class ScreenSelector:
    """
    Interface para seleção de área da tela.
    
    Cria uma janela fullscreen semi-transparente onde o usuário
    pode arrastar o mouse para selecionar uma região.
    """
    
    def __init__(self):
        """Inicializa o seletor de tela."""
        self.root = None
        self.canvas = None
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        self.selection = None
        self.cancelled = False
        
        logger.debug("ScreenSelector inicializado")
    
    def _on_mouse_down(self, event):
        """
        Callback quando o botão do mouse é pressionado.
        
        Args:
            event: Evento do mouse
        """
        self.start_x = event.x
        self.start_y = event.y
        logger.debug(f"Início da seleção: ({self.start_x}, {self.start_y})")
    
    def _on_mouse_move(self, event):
        """
        Callback quando o mouse é movido (arrastado).
        
        Args:
            event: Evento do mouse
        """
        if self.start_x is None or self.start_y is None:
            return
        
        # Remove retângulo anterior
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        
        # Desenha novo retângulo
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='#3b82f6',  # Azul
            width=2,
            fill='#3b82f6',
            stipple='gray50'  # Padrão semi-transparente
        )
    
    def _on_mouse_up(self, event):
        """
        Callback quando o botão do mouse é solto.
        
        Args:
            event: Evento do mouse
        """
        if self.start_x is None or self.start_y is None:
            return
        
        end_x = event.x
        end_y = event.y
        
        # Garante que as coordenadas estejam na ordem correta
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        
        # Valida se a seleção tem tamanho mínimo
        if (x2 - x1) < 10 or (y2 - y1) < 10:
            logger.warning("Seleção muito pequena, cancelando")
            self.cancelled = True
        else:
            self.selection = (x1, y1, x2, y2)
            logger.info(f"Área selecionada: {self.selection}")
        
        self.root.quit()
    
    def _on_key_press(self, event):
        """
        Callback quando uma tecla é pressionada.
        
        Args:
            event: Evento do teclado
        """
        if event.keysym == 'Escape':
            logger.info("Seleção cancelada pelo usuário (ESC)")
            self.cancelled = True
            self.root.quit()
    
    def select_area(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Inicia o processo de seleção de área.
        
        Returns:
            Tupla (x1, y1, x2, y2) com as coordenadas da área selecionada,
            ou None se cancelado
        """
        try:
            # Cria janela fullscreen
            self.root = tk.Tk()
            self.root.attributes('-fullscreen', True)
            self.root.attributes('-alpha', 0.3)  # Semi-transparente
            self.root.attributes('-topmost', True)
            self.root.configure(cursor='cross')
            
            # Cria canvas para desenhar a seleção
            self.canvas = Canvas(
                self.root,
                cursor='cross',
                bg='black',
                highlightthickness=0
            )
            self.canvas.pack(fill=tk.BOTH, expand=True)
            
            # Adiciona texto de instrução
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            self.canvas.create_text(
                screen_width // 2,
                50,
                text="Arraste o mouse para selecionar a área | ESC para cancelar",
                fill='white',
                font=('Arial', 16, 'bold')
            )
            
            # Bind eventos do mouse
            self.canvas.bind('<ButtonPress-1>', self._on_mouse_down)
            self.canvas.bind('<B1-Motion>', self._on_mouse_move)
            self.canvas.bind('<ButtonRelease-1>', self._on_mouse_up)
            
            # Bind tecla ESC
            self.root.bind('<KeyPress>', self._on_key_press)
            
            # Inicia loop
            logger.info("Aguardando seleção do usuário...")
            self.root.mainloop()
            
            # Limpa recursos
            try:
                self.root.destroy()
            except:
                pass
            
            # Retorna seleção ou None se cancelado
            if self.cancelled:
                return None
            
            return self.selection
        
        except Exception as e:
            logger.error(f"Erro durante seleção de área: {e}", exc_info=True)
            return None

# ============================================================================
# FUNÇÕES DE CAPTURA
# ============================================================================

def capture_screen_area(bbox: Tuple[int, int, int, int]) -> Optional[Image.Image]:
    """
    Captura uma área específica da tela.
    
    Args:
        bbox: Tupla (x1, y1, x2, y2) com as coordenadas da área
        
    Returns:
        Imagem PIL da área capturada ou None em caso de erro
    """
    try:
        logger.info(f"Capturando área: {bbox}")
        
        # Captura a área usando PIL (mais rápido que pyautogui)
        screenshot = ImageGrab.grab(bbox=bbox)
        
        logger.info(f"Área capturada com sucesso: {screenshot.size}")
        return screenshot
    
    except Exception as e:
        logger.error(f"Erro ao capturar tela: {e}", exc_info=True)
        return None

def capture_full_screen() -> Optional[Image.Image]:
    """
    Captura a tela inteira.
    
    Returns:
        Imagem PIL da tela completa ou None em caso de erro
    """
    try:
        logger.info("Capturando tela completa")
        screenshot = ImageGrab.grab()
        logger.info(f"Tela capturada: {screenshot.size}")
        return screenshot
    
    except Exception as e:
        logger.error(f"Erro ao capturar tela completa: {e}", exc_info=True)
        return None

def get_screen_resolution() -> Tuple[int, int]:
    """
    Obtém a resolução da tela.
    
    Returns:
        Tupla (largura, altura) da tela
    """
    try:
        size = pyautogui.size()
        return (size.width, size.height)
    except:
        # Fallback
        return (1920, 1080)

# ============================================================================
# FUNÇÃO PRINCIPAL DE CAPTURA
# ============================================================================

def capture_selected_area() -> Optional[Image.Image]:
    """
    Fluxo completo de captura: seleção + captura.
    
    Returns:
        Imagem PIL da área selecionada ou None se cancelado/erro
    """
    logger.info("=" * 60)
    logger.info("Iniciando processo de captura de tela")
    logger.info("=" * 60)
    
    # Etapa 1: Seleção da área
    selector = ScreenSelector()
    bbox = selector.select_area()
    
    if bbox is None:
        logger.warning("Captura cancelada ou falhou na seleção")
        return None
    
    # Etapa 2: Captura da área selecionada
    screenshot = capture_screen_area(bbox)
    
    if screenshot is None:
        logger.error("Falha ao capturar a área selecionada")
        return None
    
    logger.info("Captura concluída com sucesso!")
    return screenshot

# ============================================================================
# TESTES
# ============================================================================

if __name__ == "__main__":
    """Teste do módulo de captura."""
    
    # Configura logging para teste
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    
    print("Teste do módulo de captura")
    print("Pressione F8 para iniciar a captura...")
    
    # Simula captura
    img = capture_selected_area()
    
    if img:
        print(f"✓ Imagem capturada: {img.size}")
        img.show()  # Abre a imagem
    else:
        print("✗ Captura cancelada ou falhou")
