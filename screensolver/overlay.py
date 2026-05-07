"""
ScreenSolver AI - Interface Overlay
====================================
Interface gráfica moderna para exibir resultados.

Funcionalidades:
- Janela overlay moderna em dark mode
- Exibição de status, questão e resposta
- Histórico de respostas
- Botões para copiar e limpar
- Sempre no topo
"""

import logging
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import customtkinter as ctk
from typing import Optional, Callable
import config
from utils import history, format_timestamp, truncate_text

logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURAÇÃO DO CUSTOMTKINTER
# ============================================================================

# Define tema e modo de cor
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ============================================================================
# CLASSE PRINCIPAL DA OVERLAY
# ============================================================================

class ScreenSolverOverlay:
    """
    Janela overlay moderna para exibir resultados do ScreenSolver AI.
    
    Features:
    - Dark mode
    - Transparência
    - Sempre no topo
    - Tabs para questão, resposta e histórico
    - Loading spinner
    """
    
    def __init__(self):
        """Inicializa a overlay."""
        logger.info("Inicializando ScreenSolver Overlay")
        
        # Cria janela principal
        self.root = ctk.CTk()
        self.root.title("ScreenSolver AI")
        self.root.geometry(f"{config.UI_WIDTH}x{config.UI_HEIGHT}")
        
        # Configurações da janela
        self.root.attributes('-topmost', True)  # Sempre no topo
        self.root.attributes('-alpha', config.UI_ALPHA)  # Transparência
        
        # Variáveis de estado
        self.current_question = ""
        self.current_answer = ""
        self.is_processing = False
        
        # Cria interface
        self._create_widgets()
        
        logger.info("Overlay inicializada com sucesso")
    
    def _create_widgets(self):
        """Cria todos os widgets da interface."""
        
        # ====================================================================
        # HEADER
        # ====================================================================
        
        header_frame = ctk.CTkFrame(self.root, corner_radius=0)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text="🤖 ScreenSolver AI",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Status
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="Aguardando... (Pressione F8)",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=15)
        
        # ====================================================================
        # TABVIEW
        # ====================================================================
        
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cria tabs
        self.tab_question = self.tabview.add("📝 Questão")
        self.tab_answer = self.tabview.add("💡 Resposta")
        self.tab_history = self.tabview.add("📚 Histórico")
        
        # Configura cada tab
        self._create_question_tab()
        self._create_answer_tab()
        self._create_history_tab()
        
        # ====================================================================
        # FOOTER
        # ====================================================================
        
        footer_frame = ctk.CTkFrame(self.root, corner_radius=0)
        footer_frame.pack(fill=tk.X, padx=0, pady=0)
        
        # Botões
        btn_copy = ctk.CTkButton(
            footer_frame,
            text="📋 Copiar Resposta",
            command=self._copy_answer,
            width=150
        )
        btn_copy.pack(side=tk.LEFT, padx=10, pady=10)
        
        btn_clear = ctk.CTkButton(
            footer_frame,
            text="🗑️ Limpar",
            command=self._clear_all,
            width=100,
            fg_color="#dc2626",
            hover_color="#991b1b"
        )
        btn_clear.pack(side=tk.LEFT, padx=5, pady=10)
        
        btn_history_clear = ctk.CTkButton(
            footer_frame,
            text="🗑️ Limpar Histórico",
            command=self._clear_history,
            width=150,
            fg_color="#dc2626",
            hover_color="#991b1b"
        )
        btn_history_clear.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def _create_question_tab(self):
        """Cria conteúdo da tab de questão."""
        
        # Label
        label = ctk.CTkLabel(
            self.tab_question,
            text="Texto extraído da imagem:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Text area para questão
        self.question_text = ctk.CTkTextbox(
            self.tab_question,
            font=ctk.CTkFont(size=13),
            wrap=tk.WORD
        )
        self.question_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.question_text.insert("1.0", "Nenhuma questão capturada ainda.\n\nPressione F8 para capturar uma área da tela.")
        self.question_text.configure(state="disabled")
    
    def _create_answer_tab(self):
        """Cria conteúdo da tab de resposta."""
        
        # Label
        label = ctk.CTkLabel(
            self.tab_answer,
            text="Resposta do modelo:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Text area para resposta
        self.answer_text = ctk.CTkTextbox(
            self.tab_answer,
            font=ctk.CTkFont(size=13),
            wrap=tk.WORD
        )
        self.answer_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.answer_text.insert("1.0", "Aguardando resposta do modelo...")
        self.answer_text.configure(state="disabled")
    
    def _create_history_tab(self):
        """Cria conteúdo da tab de histórico."""
        
        # Frame para lista
        list_frame = ctk.CTkFrame(self.tab_history)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollable frame para histórico
        self.history_frame = ctk.CTkScrollableFrame(
            list_frame,
            label_text="Últimas questões resolvidas"
        )
        self.history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Carrega histórico inicial
        self._refresh_history()
    
    def _refresh_history(self):
        """Atualiza a exibição do histórico."""
        
        # Limpa widgets existentes
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Obtém histórico
        items = history.get_history(limit=config.MAX_HISTORY_ITEMS)
        
        if not items:
            # Mensagem se vazio
            empty_label = ctk.CTkLabel(
                self.history_frame,
                text="Nenhum item no histórico ainda.",
                text_color="#888888"
            )
            empty_label.pack(pady=20)
            return
        
        # Cria card para cada item
        for idx, item in enumerate(items):
            self._create_history_card(item, idx)
    
    def _create_history_card(self, item: dict, index: int):
        """
        Cria um card de histórico.
        
        Args:
            item: Dicionário com dados do item
            index: Índice do item
        """
        # Frame do card
        card = ctk.CTkFrame(self.history_frame)
        card.pack(fill=tk.X, padx=5, pady=5)
        
        # Timestamp
        timestamp = format_timestamp(item['timestamp'])
        time_label = ctk.CTkLabel(
            card,
            text=f"🕒 {timestamp}",
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        )
        time_label.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Questão (truncada)
        question_preview = truncate_text(item['question'], 80)
        question_label = ctk.CTkLabel(
            card,
            text=f"❓ {question_preview}",
            font=ctk.CTkFont(size=12),
            anchor=tk.W
        )
        question_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # Botão para ver detalhes
        btn_view = ctk.CTkButton(
            card,
            text="Ver Detalhes",
            command=lambda i=item: self._load_history_item(i),
            width=100,
            height=25,
            font=ctk.CTkFont(size=11)
        )
        btn_view.pack(anchor=tk.E, padx=10, pady=(5, 10))
    
    def _load_history_item(self, item: dict):
        """
        Carrega um item do histórico nas tabs principais.
        
        Args:
            item: Dicionário com dados do item
        """
        self.set_question(item['question'])
        self.set_answer(item['answer'])
        
        # Muda para tab de resposta
        self.tabview.set("💡 Resposta")
        
        logger.info("Item do histórico carregado")
    
    def set_status(self, status: str, color: str = "#888888"):
        """
        Atualiza o status exibido.
        
        Args:
            status: Texto do status
            color: Cor do texto
        """
        self.status_label.configure(text=status, text_color=color)
        self.root.update()
    
    def set_question(self, question: str):
        """
        Define o texto da questão.
        
        Args:
            question: Texto da questão
        """
        self.current_question = question
        
        self.question_text.configure(state="normal")
        self.question_text.delete("1.0", tk.END)
        self.question_text.insert("1.0", question)
        self.question_text.configure(state="disabled")
        
        logger.debug("Questão atualizada na interface")
    
    def set_answer(self, answer: str):
        """
        Define o texto da resposta.
        
        Args:
            answer: Texto da resposta
        """
        self.current_answer = answer
        
        self.answer_text.configure(state="normal")
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", answer)
        self.answer_text.configure(state="disabled")
        
        logger.debug("Resposta atualizada na interface")
    
    def show_loading(self, message: str = "Processando..."):
        """
        Mostra estado de loading.
        
        Args:
            message: Mensagem a exibir
        """
        self.is_processing = True
        self.set_status(f"⏳ {message}", "#3b82f6")
        
        self.answer_text.configure(state="normal")
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", f"{message}\n\nAguarde...")
        self.answer_text.configure(state="disabled")
    
    def hide_loading(self):
        """Esconde estado de loading."""
        self.is_processing = False
        self.set_status("✓ Pronto", "#22c55e")
    
    def _copy_answer(self):
        """Copia a resposta para a área de transferência."""
        if not self.current_answer:
            messagebox.showwarning("Aviso", "Nenhuma resposta para copiar.")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_answer)
        self.set_status("✓ Resposta copiada!", "#22c55e")
        
        logger.info("Resposta copiada para área de transferência")
    
    def _clear_all(self):
        """Limpa questão e resposta."""
        self.current_question = ""
        self.current_answer = ""
        
        self.question_text.configure(state="normal")
        self.question_text.delete("1.0", tk.END)
        self.question_text.insert("1.0", "Nenhuma questão capturada ainda.\n\nPressione F8 para capturar uma área da tela.")
        self.question_text.configure(state="disabled")
        
        self.answer_text.configure(state="normal")
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", "Aguardando resposta do modelo...")
        self.answer_text.configure(state="disabled")
        
        self.set_status("Aguardando... (Pressione F8)", "#888888")
        
        logger.info("Interface limpa")
    
    def _clear_history(self):
        """Limpa o histórico."""
        result = messagebox.askyesno(
            "Confirmar",
            "Tem certeza que deseja limpar todo o histórico?"
        )
        
        if result:
            history.clear_history()
            self._refresh_history()
            logger.info("Histórico limpo")
    
    def show_error(self, message: str):
        """
        Exibe mensagem de erro.
        
        Args:
            message: Mensagem de erro
        """
        self.set_status(f"✗ Erro: {message}", "#dc2626")
        messagebox.showerror("Erro", message)
    
    def update_history_display(self):
        """Atualiza a exibição do histórico."""
        self._refresh_history()
    
    def run(self):
        """Inicia o loop principal da interface."""
        logger.info("Iniciando loop da interface")
        self.root.mainloop()
    
    def destroy(self):
        """Fecha a janela."""
        logger.info("Fechando overlay")
        self.root.destroy()

# ============================================================================
# TESTES
# ============================================================================

if __name__ == "__main__":
    """Teste da overlay."""
    
    # Configura logging para teste
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    
    print("Teste da Overlay")
    
    # Cria e exibe overlay
    overlay = ScreenSolverOverlay()
    
    # Simula dados
    overlay.set_question("Quanto é 2 + 2?")
    overlay.set_answer("A resposta é 4.\n\nExplicação:\n2 + 2 = 4")
    overlay.set_status("✓ Teste concluído", "#22c55e")
    
    # Inicia
    overlay.run()
