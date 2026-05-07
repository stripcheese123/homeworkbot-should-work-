# 🤖 ScreenSolver AI

**Assistente inteligente que resolve questões capturadas da tela usando IA local**

ScreenSolver AI é um software profissional que captura áreas da sua tela, extrai o texto usando OCR e envia para um modelo de IA local (Ollama) para obter explicações detalhadas e resoluções passo a passo.

---

## 📋 Índice

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Solução de Problemas](#-solução-de-problemas)
- [Otimizações](#-otimizações)
- [FAQ](#-faq)

---

## ✨ Características

### 🎯 Funcionalidades Principais

- **Captura de Tela Inteligente**: Pressione F8 e selecione qualquer área da tela
- **OCR Avançado**: Extração de texto com pré-processamento de imagem
- **IA Local**: Usa modelo Qwen3 59B rodando no Ollama (100% offline)
- **Interface Moderna**: Dark mode com CustomTkinter
- **Histórico**: Salva todas as questões e respostas
- **Cache Inteligente**: Evita consultas duplicadas ao modelo
- **Multi-threading**: Não trava a interface durante processamento

### 🚀 Diferenciais

- ✅ **Totalmente Offline** - Nenhum dado sai do seu computador
- ✅ **Otimizado para GPU NVIDIA RTX 4060**
- ✅ **Código Profissional** - Modular, comentado e testável
- ✅ **Pré-processamento de Imagem** - Melhora precisão do OCR
- ✅ **Prompt Inteligente** - Detecta matéria automaticamente
- ✅ **Respostas Detalhadas** - Explicações passo a passo

---

## 💻 Requisitos

### Sistema Operacional
- Windows 10 ou 11
- Python 3.11 ou superior

### Hardware Recomendado
- **GPU**: NVIDIA RTX 4060 (ou superior)
- **RAM**: 16GB mínimo (32GB recomendado para modelo 59B)
- **Armazenamento**: 50GB livres (para modelo e dependências)

### Software Necessário
1. **Python 3.11+**
2. **Tesseract OCR**
3. **Ollama**
4. **CUDA Toolkit** (para GPU NVIDIA)

---

## 📦 Instalação

### Passo 1: Instalar Python

1. Baixe Python 3.11+ em: https://www.python.org/downloads/
2. Durante instalação, marque **"Add Python to PATH"**
3. Verifique a instalação:
   ```bash
   python --version
   ```

### Passo 2: Instalar Tesseract OCR

#### Windows:

1. Baixe o instalador: https://github.com/UB-Mannheim/tesseract/wiki
2. Execute o instalador
3. Durante instalação, selecione idiomas:
   - ✅ Portuguese
   - ✅ English
4. Adicione ao PATH do sistema:
   - Caminho padrão: `C:\Program Files\Tesseract-OCR`
   - Painel de Controle → Sistema → Variáveis de Ambiente
   - Adicione o caminho à variável `Path`

5. Verifique a instalação:
   ```bash
   tesseract --version
   ```

#### Linux:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-por
```

### Passo 3: Instalar Ollama

1. Baixe em: https://ollama.ai/download
2. Execute o instalador
3. Verifique a instalação:
   ```bash
   ollama --version
   ```

### Passo 4: Baixar Modelo Qwen3.5 9B

```bash
ollama pull qwen3.5:9b
```

⚠️ **ATENÇÃO**: O download pode demorar (modelo tem ~5GB)

### Passo 5: Instalar CUDA (para GPU NVIDIA)

1. Baixe CUDA Toolkit 12.x: https://developer.nvidia.com/cuda-downloads
2. Execute o instalador
3. Reinicie o computador
4. Verifique:
   ```bash
   nvidia-smi
   ```

### Passo 6: Clonar/Baixar o Projeto

```bash
cd C:\Users\SeuUsuario\Downloads
# Se tiver git:
git clone <url-do-repositorio> screensolver
# Ou extraia o ZIP baixado
```

### Passo 7: Instalar Dependências Python

```bash
cd screensolver
pip install -r requirements.txt
```

---

## ⚙️ Configuração

### Configuração Básica

O arquivo `config.py` contém todas as configurações. Principais opções:

```python
# Modelo Ollama
OLLAMA_MODEL = "qwen3:59b"

# Hotkey de captura
HOTKEY_CAPTURE = "f8"

# OCR
TESSERACT_LANG = "por+eng"
OCR_UPSCALE_FACTOR = 2.0

# Interface
UI_THEME = "dark-blue"
UI_ALPHA = 0.95
```

### Configuração Avançada

#### Otimizar para sua GPU:

```python
OLLAMA_OPTIONS = {
    "num_gpu": 1,        # Número de GPUs
    "num_thread": 8,     # Threads da CPU
    "temperature": 0.7,  # Criatividade (0.0-1.0)
}
```

#### Ajustar Timeout:

```python
OLLAMA_TIMEOUT = 120  # Segundos
```

---

## 🎮 Como Usar

### Iniciar o Programa

```bash
cd screensolver
python main.py
```

### Fluxo de Uso

1. **Inicie o programa**
   - Uma janela overlay aparecerá
   - Status: "Aguardando... (Pressione F8)"

2. **Pressione F8**
   - A tela ficará semi-transparente
   - Instruções aparecerão no topo

3. **Selecione a área**
   - Clique e arraste o mouse sobre a questão
   - Solte para capturar
   - Pressione ESC para cancelar

4. **Aguarde o processamento**
   - OCR extrai o texto
   - Modelo gera a resposta
   - Resultado aparece na overlay

5. **Visualize a resposta**
   - Tab "Questão": Texto extraído
   - Tab "Resposta": Explicação do modelo
   - Tab "Histórico": Questões anteriores

6. **Copiar resposta**
   - Clique em "📋 Copiar Resposta"
   - Cole onde precisar (Ctrl+V)

### Atalhos

- **F8**: Capturar tela
- **ESC**: Cancelar seleção
- **Ctrl+C**: Copiar (na área de texto)

---

## 📁 Estrutura do Projeto

```
screensolver/
│
├── main.py              # Arquivo principal (inicia aqui)
├── config.py            # Configurações centralizadas
├── utils.py             # Funções utilitárias
│
├── capture.py           # Módulo de captura de tela
├── ocr.py               # Módulo de OCR
├── ollama_client.py     # Cliente da API Ollama
├── overlay.py           # Interface gráfica
│
├── requirements.txt     # Dependências Python
├── README.md            # Este arquivo
│
├── screenshots/         # Screenshots salvos automaticamente
├── history/             # Histórico em JSON
└── logs/                # Logs da aplicação
```

### Descrição dos Módulos

#### `main.py`
- Orquestra todo o fluxo
- Gerencia hotkeys
- Coordena módulos

#### `capture.py`
- Seleção de área com mouse
- Captura de screenshot
- Overlay de seleção

#### `ocr.py`
- Pré-processamento de imagem
- Extração de texto com Tesseract
- Validação de texto

#### `ollama_client.py`
- Comunicação com Ollama
- Streaming de respostas
- Tratamento de erros

#### `overlay.py`
- Interface gráfica moderna
- Exibição de resultados
- Histórico visual

#### `utils.py`
- Cache de respostas
- Gerenciamento de histórico
- Logging
- Funções auxiliares

---

## 🔧 Solução de Problemas

### Erro: "Tesseract não encontrado"

**Solução:**
1. Verifique se Tesseract está instalado:
   ```bash
   tesseract --version
   ```
2. Se não estiver no PATH, adicione manualmente
3. Ou configure o caminho no código:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Erro: "Ollama não está rodando"

**Solução:**
1. Inicie o Ollama:
   ```bash
   ollama serve
   ```
2. Verifique se está rodando:
   ```bash
   curl http://localhost:11434
   ```

### Erro: "Modelo qwen3.5:9b não encontrado"

**Solução:**
```bash
ollama pull qwen3.5:9b
```

### OCR não detecta texto corretamente

**Soluções:**
1. Aumente o fator de upscale em `config.py`:
   ```python
   OCR_UPSCALE_FACTOR = 3.0
   ```
2. Capture área com texto maior/mais claro
3. Ajuste threshold:
   ```python
   OCR_THRESHOLD_VALUE = 180
   ```

### Modelo muito lento

**Soluções:**
1. Verifique se GPU está sendo usada:
   - No Ollama, deve aparecer "CUDA" ou "GPU"
2. Use modelo menor:
   ```python
   OLLAMA_MODEL = "qwen3:14b"  # Mais rápido
   ```
3. Aumente threads:
   ```python
   OLLAMA_OPTIONS = {"num_thread": 16}
   ```

### Hotkey F8 não funciona

**Soluções:**
1. Execute como Administrador (Windows)
2. Verifique se outra aplicação usa F8
3. Mude a hotkey em `config.py`:
   ```python
   HOTKEY_CAPTURE = "f9"
   ```

### Interface não abre

**Solução:**
```bash
pip install --upgrade customtkinter
```

---

## ⚡ Otimizações

### Para GPU NVIDIA RTX 4060

O projeto já está otimizado, mas você pode ajustar:

```python
# config.py
OLLAMA_OPTIONS = {
    "num_gpu": 1,           # Usa 1 GPU
    "num_thread": 8,        # 8 threads CPU
    "num_ctx": 4096,        # Contexto (tokens)
    "temperature": 0.7,
}
```

### Reduzir Uso de RAM

Use modelo menor:
```bash
ollama pull qwen3:14b
```

```python
OLLAMA_MODEL = "qwen3:14b"
```

### Aumentar Velocidade do OCR

```python
OCR_UPSCALE_FACTOR = 1.5  # Menor = mais rápido
SAVE_PROCESSED_IMAGES = False  # Não salvar debug
```

### Cache Agressivo

```python
CACHE_MAX_SIZE = 100  # Mais itens em cache
ENABLE_CACHE = True
```

---

## ❓ FAQ

### O projeto funciona offline?

**Sim!** 100% offline. Nenhum dado sai do computador.

### Preciso de internet?

Apenas para:
- Instalar dependências (`pip install`)
- Baixar modelo Ollama (`ollama pull`)

Depois disso, funciona totalmente offline.

### Funciona em Linux/macOS?

O código é compatível, mas foi testado principalmente no Windows. Ajustes podem ser necessários.

### Posso usar outro modelo?

Sim! Edite `config.py`:
```python
OLLAMA_MODEL = "llama3:70b"  # Ou qualquer modelo
```

### Quanto de RAM preciso?

- **Modelo 9B**: 8GB suficiente
- **Modelo 14B**: 16GB suficiente
- **Modelo 59B**: 32GB recomendado

### Funciona sem GPU?

Sim, mas será **muito mais lento**. GPU NVIDIA é altamente recomendada.

### Os dados são salvos?

Sim:
- Screenshots em `screenshots/`
- Histórico em `history/history.json`
- Logs em `logs/screensolver.log`

### Como desinstalar?

1. Delete a pasta `screensolver/`
2. Desinstale Ollama (opcional)
3. Desinstale Tesseract (opcional)

---

## 📝 Licença

Este projeto é fornecido como está, para uso educacional e pessoal.

---

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!

---

## 📧 Suporte

Para problemas:
1. Verifique a seção [Solução de Problemas](#-solução-de-problemas)
2. Consulte os logs em `logs/screensolver.log`
3. Ative modo debug em `config.py`:
   ```python
   DEBUG_MODE = True
   ```

---

## 🎉 Agradecimentos

- **Ollama**: Framework para rodar LLMs localmente
- **Tesseract**: OCR open-source
- **CustomTkinter**: Interface moderna para Python

---

**Desenvolvido com ❤️ para estudantes e entusiastas de IA**

**Versão**: 1.0.0  
**Data**: 2026
