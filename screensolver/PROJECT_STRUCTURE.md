# 📂 Estrutura do Projeto - ScreenSolver AI

Visão completa da organização do projeto.

---

## 🌳 Árvore de Diretórios

```
screensolver/
│
├── 📄 main.py                    # ⭐ ARQUIVO PRINCIPAL - Execute este
├── 📄 config.py                  # ⚙️ Configurações centralizadas
├── 📄 utils.py                   # 🛠️ Funções utilitárias
│
├── 📄 capture.py                 # 📸 Módulo de captura de tela
├── 📄 ocr.py                     # 🔍 Módulo de OCR
├── 📄 ollama_client.py           # 🤖 Cliente da API Ollama
├── 📄 overlay.py                 # 🎨 Interface gráfica
│
├── 📄 requirements.txt           # 📦 Dependências Python
├── 📄 __init__.py                # 📦 Inicialização do pacote
│
├── 📄 README.md                  # 📖 Documentação principal
├── 📄 INSTALL.md                 # 🚀 Guia de instalação
├── 📄 QUICKSTART.md              # ⚡ Guia rápido
├── 📄 TECHNICAL.md               # 🔧 Documentação técnica
├── 📄 CHANGELOG.md               # 📝 Histórico de versões
├── 📄 PROJECT_STRUCTURE.md       # 📂 Este arquivo
│
├── 📄 run.bat                    # ▶️ Script de execução (Windows)
├── 📄 test_setup.py              # 🧪 Teste de configuração
├── 📄 .gitignore                 # 🚫 Arquivos ignorados pelo Git
├── 📄 LICENSE                    # ⚖️ Licença MIT
│
├── 📁 screenshots/               # 🖼️ Screenshots salvos (criado automaticamente)
├── 📁 history/                   # 📚 Histórico em JSON (criado automaticamente)
└── 📁 logs/                      # 📋 Logs da aplicação (criado automaticamente)
```

---

## 📊 Estatísticas do Projeto

| Categoria | Quantidade |
|-----------|------------|
| **Arquivos Python** | 8 |
| **Arquivos de Documentação** | 7 |
| **Arquivos de Configuração** | 3 |
| **Total de Arquivos** | 18 |
| **Linhas de Código** | ~2.500 |
| **Linhas de Documentação** | ~1.500 |

---

## 🎯 Arquivos por Categoria

### 🔴 Arquivos Essenciais (Não Delete!)

| Arquivo | Descrição | Tamanho |
|---------|-----------|---------|
| `main.py` | Ponto de entrada da aplicação | ~300 linhas |
| `config.py` | Todas as configurações | ~200 linhas |
| `utils.py` | Funções auxiliares | ~350 linhas |
| `capture.py` | Captura de tela | ~300 linhas |
| `ocr.py` | OCR e pré-processamento | ~350 linhas |
| `ollama_client.py` | Cliente Ollama | ~400 linhas |
| `overlay.py` | Interface gráfica | ~500 linhas |
| `requirements.txt` | Dependências | ~50 linhas |

### 🟡 Arquivos de Suporte

| Arquivo | Descrição | Uso |
|---------|-----------|-----|
| `run.bat` | Script de execução | Windows |
| `test_setup.py` | Validação de instalação | Diagnóstico |
| `__init__.py` | Inicialização do pacote | Python |
| `.gitignore` | Exclusões do Git | Versionamento |
| `LICENSE` | Licença MIT | Legal |

### 🟢 Documentação

| Arquivo | Conteúdo | Público |
|---------|----------|---------|
| `README.md` | Documentação completa | Todos |
| `INSTALL.md` | Guia de instalação | Iniciantes |
| `QUICKSTART.md` | Início rápido | Iniciantes |
| `TECHNICAL.md` | Documentação técnica | Desenvolvedores |
| `CHANGELOG.md` | Histórico de versões | Todos |
| `PROJECT_STRUCTURE.md` | Estrutura do projeto | Desenvolvedores |

---

## 🔗 Dependências entre Módulos

```
main.py
  ├─ imports config.py
  ├─ imports utils.py
  │   └─ imports config.py
  ├─ imports capture.py
  ├─ imports ocr.py
  │   └─ imports config.py
  ├─ imports ollama_client.py
  │   └─ imports config.py
  └─ imports overlay.py
      ├─ imports config.py
      └─ imports utils.py
```

### Ordem de Importação

1. `config.py` (sem dependências)
2. `utils.py` (depende de config)
3. `capture.py` (independente)
4. `ocr.py` (depende de config)
5. `ollama_client.py` (depende de config)
6. `overlay.py` (depende de config e utils)
7. `main.py` (depende de todos)

---

## 📝 Descrição Detalhada

### `main.py` (300 linhas)

**Função**: Orquestrador principal

**Contém**:
- Classe `ScreenSolverApp`
- Função `main()`
- Gerenciamento de hotkeys
- Pipeline de processamento
- Tratamento de erros

**Importa**:
- Todos os outros módulos
- `keyboard` (hotkeys)
- `threading` (multi-threading)

---

### `config.py` (200 linhas)

**Função**: Configurações centralizadas

**Seções**:
- Ollama (endpoint, modelo, opções)
- Hotkeys (F8, ESC)
- OCR (idioma, upscale, threshold)
- Interface (tema, cores, tamanho)
- Diretórios (screenshots, logs, histórico)
- Cache (tamanho, habilitado)
- Prompt do sistema

**Sem dependências externas**

---

### `utils.py` (350 linhas)

**Função**: Funções auxiliares

**Contém**:
- `setup_logging()`: Configura logs
- `ResponseCache`: Cache LRU
- `HistoryManager`: Gerencia histórico
- `save_screenshot()`: Salva imagens
- `validate_*()`: Validações

**Importa**:
- `config.py`
- `logging`, `json`, `hashlib`

---

### `capture.py` (300 linhas)

**Função**: Captura de tela

**Contém**:
- Classe `ScreenSelector`
- `capture_screen_area()`
- `capture_selected_area()`

**Importa**:
- `tkinter` (interface de seleção)
- `PIL.ImageGrab` (captura)
- `pyautogui` (resolução)

---

### `ocr.py` (350 linhas)

**Função**: Extração de texto

**Contém**:
- `preprocess_image()`: Pipeline de processamento
- `extract_text()`: OCR com Tesseract
- `process_image_to_text()`: Fluxo completo
- `get_text_confidence()`: Confiança do OCR

**Importa**:
- `config.py`
- `pytesseract` (OCR)
- `cv2` (OpenCV)
- `PIL` (processamento de imagem)

---

### `ollama_client.py` (400 linhas)

**Função**: Cliente da API Ollama

**Contém**:
- Classe `OllamaClient`
- `generate()`: Gera resposta
- `generate_answer()`: Resposta para questão
- `check_connection()`: Valida conexão
- `check_model()`: Valida modelo

**Importa**:
- `config.py`
- `requests` (HTTP)
- `json` (parsing)

---

### `overlay.py` (500 linhas)

**Função**: Interface gráfica

**Contém**:
- Classe `ScreenSolverOverlay`
- Tabs (Questão, Resposta, Histórico)
- Botões de ação
- Gerenciamento de estado

**Importa**:
- `config.py`
- `utils.py`
- `customtkinter` (interface moderna)
- `tkinter` (base)

---

### `requirements.txt` (50 linhas)

**Função**: Lista de dependências

**Contém**:
- customtkinter>=5.2.0
- Pillow>=10.0.0
- pyautogui>=0.9.54
- pytesseract>=0.3.10
- opencv-python>=4.8.0
- numpy>=1.24.0
- keyboard>=0.13.5
- requests>=2.31.0

---

### `run.bat` (Script Windows)

**Função**: Facilita execução no Windows

**Faz**:
1. Verifica Python
2. Verifica Tesseract
3. Verifica Ollama
4. Inicia Ollama se necessário
5. Executa `main.py`

---

### `test_setup.py` (250 linhas)

**Função**: Valida instalação

**Testa**:
1. Versão do Python
2. Dependências instaladas
3. Tesseract OCR
4. Ollama rodando
5. Modelo disponível
6. GPU NVIDIA (opcional)
7. Permissões

---

## 📁 Diretórios Criados Automaticamente

### `screenshots/`

**Conteúdo**: Screenshots salvos automaticamente

**Formato**: `screenshot_YYYYMMDD_HHMMSS.png`

**Configurável**: `AUTO_SAVE_SCREENSHOTS` em `config.py`

---

### `history/`

**Conteúdo**: Histórico de questões/respostas

**Arquivo**: `history.json`

**Formato**:
```json
[
  {
    "timestamp": "2026-05-06T21:32:15",
    "question": "Quanto é 2+2?",
    "response": "A resposta é 4...",
    "screenshot": "screenshots/screenshot_20260506_213215.png"
  }
]
```

---

### `logs/`

**Conteúdo**: Logs da aplicação

**Arquivo**: `screensolver.log`

**Formato**:
```
2026-05-06 21:32:15 [INFO] ScreenSolver AI iniciado
2026-05-06 21:32:16 [DEBUG] Hotkey F8 registrada
...
```

---

## 🎯 Como Navegar no Projeto

### Para Usuários

1. **Começar**: Leia `README.md`
2. **Instalar**: Siga `INSTALL.md`
3. **Usar**: Consulte `QUICKSTART.md`
4. **Problemas**: Veja seção "Solução de Problemas" no `README.md`

### Para Desenvolvedores

1. **Arquitetura**: Leia `TECHNICAL.md`
2. **Estrutura**: Este arquivo (`PROJECT_STRUCTURE.md`)
3. **Código**: Comece por `main.py`
4. **Configurar**: Edite `config.py`
5. **Testar**: Execute `test_setup.py`

---

## 🔧 Modificações Comuns

### Mudar Modelo IA

**Arquivo**: `config.py`
```python
OLLAMA_MODEL = "qwen3:14b"  # Linha 23
```

### Mudar Hotkey

**Arquivo**: `config.py`
```python
HOTKEY_CAPTURE = "f9"  # Linha 31
```

### Ajustar OCR

**Arquivo**: `config.py`
```python
OCR_UPSCALE_FACTOR = 3.0  # Linha 48
```

### Customizar Interface

**Arquivo**: `config.py`
```python
UI_THEME = "dark-blue"  # Linha 60
UI_ALPHA = 0.95  # Linha 72
```

### Modificar Prompt

**Arquivo**: `config.py`
```python
SYSTEM_PROMPT = """..."""  # Linha 105
```

---

## 📦 Tamanho do Projeto

| Componente | Tamanho |
|------------|---------|
| **Código Python** | ~100 KB |
| **Documentação** | ~50 KB |
| **Total (sem dependências)** | ~150 KB |
| **Com dependências** | ~500 MB |
| **Com modelo 59B** | ~35 GB |

---

## 🚀 Próximos Passos

Agora que você entende a estrutura:

1. ✅ Explore cada arquivo
2. ✅ Leia os comentários no código
3. ✅ Execute `test_setup.py`
4. ✅ Rode `main.py`
5. ✅ Experimente modificar `config.py`

---

**Estrutura do Projeto v1.0.0**

Última atualização: 2026-05-06
