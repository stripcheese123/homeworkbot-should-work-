# 🔧 Documentação Técnica - ScreenSolver AI

**Guia para desenvolvedores e usuários avançados**

---

## 📐 Arquitetura

### Visão Geral

```
┌─────────────────────────────────────────────────────────┐
│                     main.py                              │
│              (Orquestrador Principal)                    │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  capture.py  │  │    ocr.py    │  │ ollama_      │
│              │  │              │  │ client.py    │
│ Captura de   │  │ Extração de  │  │              │
│ Tela         │  │ Texto (OCR)  │  │ Cliente IA   │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │  overlay.py  │
                  │              │
                  │  Interface   │
                  │  Gráfica     │
                  └──────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │   utils.py   │
                  │              │
                  │ Cache, Log,  │
                  │ Histórico    │
                  └──────────────┘
```

### Fluxo de Dados

```
1. Usuário pressiona F8
   ↓
2. capture.py → Captura área da tela
   ↓
3. ocr.py → Extrai texto da imagem
   ↓
4. utils.py → Verifica cache
   ↓
5. ollama_client.py → Consulta modelo (se não em cache)
   ↓
6. utils.py → Salva em cache e histórico
   ↓
7. overlay.py → Exibe resultado
```

---

## 🗂️ Estrutura de Módulos

### `main.py`

**Responsabilidade**: Orquestração geral

**Classes**:
- `ScreenSolverApp`: Aplicação principal

**Métodos principais**:
- `__init__()`: Inicializa componentes
- `_initialize()`: Valida dependências
- `_register_hotkeys()`: Registra F8
- `_on_capture_hotkey()`: Callback do F8
- `_process_capture()`: Pipeline completo
- `run()`: Loop principal
- `cleanup()`: Limpeza de recursos

**Threading**: Usa `threading.Thread` para não travar interface

---

### `config.py`

**Responsabilidade**: Configurações centralizadas

**Seções**:
- Ollama (endpoint, modelo, opções)
- Hotkeys (captura, cancelar)
- OCR (idioma, config, upscale)
- Interface (tema, cores, tamanho)
- Diretórios (screenshots, logs, histórico)
- Cache (tamanho, habilitado)
- Prompt do sistema

**Variáveis importantes**:
```python
OLLAMA_MODEL = "qwen3:59b"
HOTKEY_CAPTURE = "f8"
OCR_UPSCALE_FACTOR = 2.0
UI_ALPHA = 0.95
CACHE_MAX_SIZE = 50
```

---

### `utils.py`

**Responsabilidade**: Funções auxiliares

**Classes**:
- `ResponseCache`: Cache LRU de respostas
- `HistoryManager`: Gerenciamento de histórico

**Funções**:
- `setup_logging()`: Configura sistema de logs
- `save_screenshot()`: Salva imagem
- `format_timestamp()`: Formata data/hora
- `truncate_text()`: Trunca texto longo
- `validate_ollama_connection()`: Valida Ollama
- `validate_tesseract_installation()`: Valida Tesseract

**Cache**:
- Algoritmo: LRU (Least Recently Used)
- Chave: Hash MD5 do texto
- Persistência: Apenas em memória (não salvo em disco)

**Histórico**:
- Formato: JSON
- Arquivo: `history/history.json`
- Campos: timestamp, question, response, screenshot

---

### `capture.py`

**Responsabilidade**: Captura de tela

**Classes**:
- `ScreenSelector`: Interface de seleção

**Métodos**:
- `select_area()`: Inicia seleção
- `_on_mouse_down()`: Mouse pressionado
- `_on_mouse_move()`: Mouse arrastado
- `_on_mouse_up()`: Mouse solto
- `_on_key_press()`: Tecla pressionada (ESC)

**Funções**:
- `capture_screen_area()`: Captura bbox
- `capture_full_screen()`: Captura tela inteira
- `capture_selected_area()`: Fluxo completo

**Tecnologias**:
- `tkinter`: Interface de seleção
- `PIL.ImageGrab`: Captura de tela
- `pyautogui`: Resolução da tela

---

### `ocr.py`

**Responsabilidade**: Extração de texto

**Pipeline de pré-processamento**:
1. **Upscale**: Aumenta resolução (2x padrão)
2. **Grayscale**: Converte para tons de cinza
3. **Sharpen**: Aumenta nitidez
4. **Threshold**: Binarização adaptativa
5. **Denoise**: Remove ruído (median blur)

**Funções principais**:
- `preprocess_image()`: Aplica pipeline
- `extract_text()`: Extrai texto com Tesseract
- `process_image_to_text()`: Fluxo completo
- `get_text_confidence()`: Calcula confiança
- `validate_text()`: Valida texto extraído

**Parâmetros Tesseract**:
```python
lang = "por+eng"
config = "--psm 6 --oem 3"
```

**Otimizações**:
- Upscale melhora precisão em textos pequenos
- Threshold adaptativo funciona com diferentes iluminações
- Median blur remove ruído sem perder detalhes

---

### `ollama_client.py`

**Responsabilidade**: Comunicação com Ollama

**Classes**:
- `OllamaClient`: Cliente da API

**Métodos**:
- `check_connection()`: Verifica se Ollama está rodando
- `check_model()`: Verifica se modelo existe
- `generate()`: Gera resposta (genérico)
- `generate_answer()`: Gera resposta para questão
- `generate_answer_stream()`: Com streaming
- `_generate_blocking()`: Sem streaming
- `_generate_stream()`: Com streaming

**Endpoints**:
- Base: `http://localhost:11434`
- Generate: `/api/generate`
- Tags: `/api/tags`

**Payload exemplo**:
```json
{
  "model": "qwen3:59b",
  "prompt": "...",
  "stream": false,
  "options": {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "num_gpu": 1,
    "num_thread": 8
  }
}
```

**Tratamento de erros**:
- Timeout (120s padrão)
- ConnectionError
- Status code != 200
- JSON decode errors

---

### `overlay.py`

**Responsabilidade**: Interface gráfica

**Classes**:
- `ScreenSolverOverlay`: Janela principal

**Componentes**:
- **Header**: Título e status
- **TabView**: 3 tabs (Questão, Resposta, Histórico)
- **Footer**: Botões de ação

**Métodos principais**:
- `set_status()`: Atualiza status
- `set_question()`: Define questão
- `set_answer()`: Define resposta
- `show_loading()`: Mostra loading
- `hide_loading()`: Esconde loading
- `show_error()`: Exibe erro
- `update_history_display()`: Atualiza histórico
- `_copy_answer()`: Copia resposta
- `_clear_all()`: Limpa interface
- `_clear_history()`: Limpa histórico

**Tecnologias**:
- `customtkinter`: Interface moderna
- Tema: Dark mode
- Transparência: 95% (configurável)

**Cores**:
- Background: `#1a1a1a`
- Texto: `#ffffff`
- Accent: `#3b82f6` (azul)
- Erro: `#dc2626` (vermelho)
- Sucesso: `#22c55e` (verde)

---

## 🔄 Ciclo de Vida

### Inicialização

```python
1. main.py importa módulos
2. Configura logging (utils.py)
3. Valida Tesseract
4. Valida Ollama
5. Cria OllamaClient
6. Cria ScreenSolverOverlay
7. Registra hotkey F8
8. Inicia loop da interface
```

### Processamento

```python
1. Usuário pressiona F8
2. Debounce (0.5s)
3. Verifica se já está processando
4. Inicia thread de processamento
5. Captura tela (capture.py)
6. Extrai texto (ocr.py)
7. Verifica cache (utils.py)
8. Se não em cache:
   - Consulta Ollama (ollama_client.py)
   - Salva em cache
9. Adiciona ao histórico
10. Atualiza interface (overlay.py)
```

### Finalização

```python
1. Usuário fecha janela
2. cleanup() é chamado
3. Remove hotkeys
4. Salva histórico
5. Fecha logs
6. Encerra aplicação
```

---

## 🧪 Testes

### Teste Manual

```bash
# Teste de configuração
python test_setup.py

# Teste de módulo individual
python capture.py
python ocr.py
python ollama_client.py
python overlay.py
```

### Teste de Integração

```bash
# Executa aplicação completa
python main.py
```

---

## 🔒 Segurança

### Dados Locais

- ✅ Nenhum dado enviado para internet
- ✅ Processamento 100% local
- ✅ Screenshots salvos localmente
- ✅ Histórico em JSON local
- ✅ Logs locais

### Permissões

**Windows**:
- Administrador recomendado (para hotkeys globais)
- Acesso à tela (para captura)
- Acesso ao sistema de arquivos

**Rede**:
- Apenas localhost:11434 (Ollama)
- Nenhuma conexão externa

---

## ⚡ Performance

### Benchmarks (RTX 4060)

| Operação | Tempo Médio |
|----------|-------------|
| Captura de tela | ~0.1s |
| OCR (pré-processamento) | ~0.5s |
| OCR (extração) | ~1-2s |
| Consulta modelo 59B | ~10-30s |
| Consulta modelo 14B | ~3-10s |
| Atualização interface | ~0.01s |

### Otimizações Implementadas

1. **Threading**: Não trava interface
2. **Cache LRU**: Respostas instantâneas para duplicatas
3. **Debounce**: Evita múltiplos triggers
4. **GPU**: Usa NVIDIA RTX 4060
5. **Upscale seletivo**: Apenas quando necessário

### Gargalos

1. **Modelo 59B**: Lento em CPUs
   - Solução: Usar GPU ou modelo menor
2. **OCR**: Pode demorar em imagens grandes
   - Solução: Reduzir upscale factor
3. **Primeira execução**: Carrega modelo
   - Solução: Manter Ollama rodando

---

## 🛠️ Customização

### Adicionar Novo Modelo

```python
# 1. Baixe o modelo
ollama pull nome-do-modelo

# 2. Edite config.py
OLLAMA_MODEL = "nome-do-modelo"

# 3. Ajuste opções se necessário
OLLAMA_OPTIONS = {
    "temperature": 0.7,
    # ...
}
```

### Adicionar Nova Hotkey

```python
# config.py
HOTKEY_NOVA_FUNCAO = "f9"

# main.py
def _register_hotkeys(self):
    keyboard.add_hotkey(
        config.HOTKEY_NOVA_FUNCAO,
        self._on_nova_funcao,
        suppress=True
    )

def _on_nova_funcao(self):
    # Sua lógica aqui
    pass
```

### Customizar Prompt

```python
# config.py
SYSTEM_PROMPT = """
Seu prompt customizado aqui.

Questão: {question}

Resposta:
"""
```

### Adicionar Novo Idioma OCR

```python
# 1. Instale pacote de idioma Tesseract
# Windows: Durante instalação
# Linux: sudo apt-get install tesseract-ocr-fra

# 2. Edite config.py
TESSERACT_LANG = "por+eng+fra"  # Adiciona francês
```

---

## 📊 Logs

### Formato

```
2026-05-06 21:32:15 [INFO] Mensagem
```

### Níveis

- **DEBUG**: Informações detalhadas
- **INFO**: Eventos normais
- **WARNING**: Avisos
- **ERROR**: Erros

### Localização

- Arquivo: `logs/screensolver.log`
- Console: Saída padrão

### Habilitar Debug

```python
# config.py
DEBUG_MODE = True
```

---

## 🐛 Debug

### Problemas Comuns

**OCR não detecta texto**:
```python
# Salve imagens processadas
SAVE_PROCESSED_IMAGES = True

# Verifique em screenshots/debug_processed.png
```

**Modelo não responde**:
```python
# Aumente timeout
OLLAMA_TIMEOUT = 300  # 5 minutos

# Verifique logs
tail -f logs/screensolver.log
```

**Interface trava**:
```python
# Verifique se threading está ativo
USE_THREADING = True
```

---

## 📈 Métricas

### Cache Hit Rate

```python
# Adicione em utils.py
def get_cache_stats():
    hits = cache.hits
    misses = cache.misses
    rate = hits / (hits + misses) * 100
    return f"{rate:.2f}%"
```

### Tempo de Resposta

```python
# Adicione em main.py
import time

start = time.time()
# ... processamento ...
end = time.time()
logger.info(f"Tempo total: {end - start:.2f}s")
```

---

## 🔮 Roadmap Técnico

### v1.1.0
- [ ] Testes unitários (pytest)
- [ ] CI/CD (GitHub Actions)
- [ ] Profiling de performance
- [ ] Cobertura de código

### v1.2.0
- [ ] API REST (FastAPI)
- [ ] WebSocket para streaming
- [ ] Docker container
- [ ] Kubernetes deployment

### v2.0.0
- [ ] Suporte multi-plataforma
- [ ] Interface web (React)
- [ ] Banco de dados (SQLite)
- [ ] Autenticação

---

## 📚 Referências

### Bibliotecas

- **CustomTkinter**: https://github.com/TomSchimansky/CustomTkinter
- **Tesseract**: https://github.com/tesseract-ocr/tesseract
- **Ollama**: https://ollama.ai/
- **Pillow**: https://pillow.readthedocs.io/
- **OpenCV**: https://opencv.org/

### Documentação

- **Ollama API**: https://github.com/ollama/ollama/blob/main/docs/api.md
- **Tesseract Config**: https://tesseract-ocr.github.io/tessdoc/
- **Tkinter**: https://docs.python.org/3/library/tkinter.html

---

**Documentação Técnica v1.0.0**

Última atualização: 2026-05-06
