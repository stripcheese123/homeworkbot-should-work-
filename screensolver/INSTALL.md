# 🚀 Guia de Instalação Rápida - ScreenSolver AI

Este guia fornece instruções passo a passo para instalar e executar o ScreenSolver AI.

---

## ⚡ Instalação Rápida (Windows)

### 1️⃣ Instalar Python 3.11+

```powershell
# Baixe em: https://www.python.org/downloads/
# Durante instalação, marque "Add Python to PATH"

# Verifique:
python --version
```

### 2️⃣ Instalar Tesseract OCR

```powershell
# Baixe: https://github.com/UB-Mannheim/tesseract/wiki
# Execute o instalador
# Selecione idiomas: Portuguese + English

# Adicione ao PATH:
# C:\Program Files\Tesseract-OCR

# Verifique:
tesseract --version
```

### 3️⃣ Instalar Ollama

```powershell
# Baixe: https://ollama.ai/download
# Execute o instalador

# Verifique:
ollama --version
```

### 4️⃣ Baixar Modelo Qwen3 59B

```powershell
# Este comando baixará ~35GB
ollama pull qwen3:59b

# Aguarde o download completar
```

### 5️⃣ Instalar CUDA (para GPU NVIDIA)

```powershell
# Baixe CUDA Toolkit 12.x:
# https://developer.nvidia.com/cuda-downloads

# Execute o instalador
# Reinicie o computador

# Verifique:
nvidia-smi
```

### 6️⃣ Instalar Dependências do Projeto

```powershell
# Navegue até a pasta do projeto
cd C:\Users\SeuUsuario\Downloads\screensolver

# Instale as dependências
pip install -r requirements.txt
```

---

## ▶️ Executar o Projeto

### Passo 1: Iniciar Ollama (se não estiver rodando)

```powershell
ollama serve
```

Deixe esta janela aberta.

### Passo 2: Executar ScreenSolver AI

Abra um novo terminal:

```powershell
cd C:\Users\SeuUsuario\Downloads\screensolver
python main.py
```

### Passo 3: Usar o Programa

1. Pressione **F8**
2. Selecione a área da tela com a questão
3. Aguarde a resposta aparecer

---

## 🔍 Verificação da Instalação

Execute este script para verificar se tudo está instalado:

```powershell
# Verificar Python
python --version

# Verificar Tesseract
tesseract --version

# Verificar Ollama
ollama --version

# Verificar CUDA (se tiver GPU NVIDIA)
nvidia-smi

# Listar modelos Ollama
ollama list
```

**Resultado esperado:**
- Python 3.11+
- Tesseract 5.x
- Ollama 0.x
- CUDA 12.x (se GPU NVIDIA)
- Modelo `qwen3:59b` na lista

---

## ⚠️ Problemas Comuns

### "Tesseract não encontrado"

**Solução:**
1. Reinstale o Tesseract
2. Adicione ao PATH: `C:\Program Files\Tesseract-OCR`
3. Reinicie o terminal

### "Ollama não está rodando"

**Solução:**
```powershell
ollama serve
```

### "Modelo não encontrado"

**Solução:**
```powershell
ollama pull qwen3:59b
```

### "Erro ao instalar dependências"

**Solução:**
```powershell
# Atualize pip
python -m pip install --upgrade pip

# Tente novamente
pip install -r requirements.txt
```

### "Hotkey não funciona"

**Solução:**
- Execute como Administrador
- Clique com botão direito em PowerShell → "Executar como Administrador"

---

## 📊 Requisitos de Sistema

### Mínimo
- Windows 10
- Python 3.11
- 16GB RAM
- 50GB espaço livre

### Recomendado
- Windows 11
- Python 3.12
- 32GB RAM
- GPU NVIDIA RTX 4060
- 100GB espaço livre

---

## 🎯 Próximos Passos

Após instalação bem-sucedida:

1. Leia o [README.md](README.md) completo
2. Ajuste configurações em `config.py` se necessário
3. Execute `python main.py`
4. Pressione F8 e teste!

---

## 💡 Dicas

### Usar modelo menor (mais rápido)

Se o modelo 59B estiver muito lento:

```powershell
# Baixe modelo menor
ollama pull qwen3:14b

# Edite config.py:
# OLLAMA_MODEL = "qwen3:14b"
```

### Executar em segundo plano

```powershell
# Windows
start /B python main.py
```

### Criar atalho

1. Crie arquivo `ScreenSolver.bat`:
   ```batch
   @echo off
   cd C:\Users\SeuUsuario\Downloads\screensolver
   python main.py
   ```
2. Clique com botão direito → "Criar atalho"
3. Mova atalho para área de trabalho

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique logs em `logs/screensolver.log`
2. Ative debug em `config.py`: `DEBUG_MODE = True`
3. Consulte [README.md](README.md) seção "Solução de Problemas"

---

**Instalação concluída! 🎉**

Aproveite o ScreenSolver AI!
