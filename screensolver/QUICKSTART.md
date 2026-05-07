# ⚡ Guia Rápido - ScreenSolver AI

**Comece a usar em 5 minutos!**

---

## 🎯 Pré-requisitos

Antes de começar, você precisa ter instalado:

1. ✅ **Python 3.11+** → [Download](https://www.python.org/downloads/)
2. ✅ **Tesseract OCR** → [Download](https://github.com/UB-Mannheim/tesseract/wiki)
3. ✅ **Ollama** → [Download](https://ollama.ai/download)
4. ✅ **Modelo qwen3:59b** → `ollama pull qwen3:59b`

---

## 🚀 Instalação em 3 Passos

### 1. Instalar Dependências

```bash
cd screensolver
pip install -r requirements.txt
```

### 2. Verificar Instalação

```bash
python test_setup.py
```

Você deve ver ✅ em todos os testes.

### 3. Executar

**Opção A - Script Batch (Windows):**
```bash
run.bat
```

**Opção B - Python direto:**
```bash
python main.py
```

---

## 🎮 Como Usar

### Passo a Passo

1. **Inicie o programa**
   - Execute `run.bat` ou `python main.py`
   - Uma janela aparecerá

2. **Capture uma questão**
   - Pressione **F8**
   - Arraste o mouse sobre a questão
   - Solte para capturar

3. **Aguarde a resposta**
   - OCR extrai o texto
   - IA processa
   - Resposta aparece

4. **Copie a resposta**
   - Clique em "📋 Copiar Resposta"
   - Cole onde precisar

---

## ⌨️ Atalhos

| Tecla | Ação |
|-------|------|
| **F8** | Capturar tela |
| **ESC** | Cancelar seleção |
| **Ctrl+C** | Copiar texto selecionado |

---

## 🔧 Configuração Rápida

### Mudar Modelo (se 59B estiver lento)

Edite `config.py`:

```python
OLLAMA_MODEL = "qwen3:14b"  # Modelo menor e mais rápido
```

Depois baixe:
```bash
ollama pull qwen3:14b
```

### Mudar Hotkey

Edite `config.py`:

```python
HOTKEY_CAPTURE = "f9"  # Ou qualquer outra tecla
```

### Ajustar Qualidade do OCR

Edite `config.py`:

```python
OCR_UPSCALE_FACTOR = 3.0  # Maior = melhor qualidade, mais lento
```

---

## ❓ Problemas Comuns

### "Tesseract não encontrado"

**Solução:**
1. Instale o Tesseract
2. Adicione ao PATH: `C:\Program Files\Tesseract-OCR`
3. Reinicie o terminal

### "Ollama não está rodando"

**Solução:**
```bash
ollama serve
```

### "Modelo não encontrado"

**Solução:**
```bash
ollama pull qwen3:59b
```

### Hotkey não funciona

**Solução:**
- Execute como Administrador (Windows)

---

## 📊 Exemplo de Uso

### Questão de Matemática

1. Abra uma questão no navegador/PDF
2. Pressione **F8**
3. Selecione a questão
4. Aguarde 10-30 segundos
5. Leia a explicação passo a passo

### Questão de Programação

1. Capture o código da tela
2. IA explica linha por linha
3. Copie a explicação

### Múltipla Escolha

1. Capture a questão com alternativas
2. IA analisa cada alternativa
3. Explica qual é correta e por quê

---

## 🎯 Dicas Pro

### 1. Use Cache

O programa salva respostas automaticamente. Se capturar a mesma questão, a resposta é instantânea!

### 2. Histórico

Clique na tab "📚 Histórico" para ver questões anteriores.

### 3. Screenshots

Todas as capturas são salvas em `screenshots/` automaticamente.

### 4. Logs

Se algo der errado, veja `logs/screensolver.log`

### 5. Debug Mode

Para mais informações, edite `config.py`:
```python
DEBUG_MODE = True
```

---

## 📚 Próximos Passos

Agora que está funcionando:

1. ✅ Leia o [README.md](README.md) completo
2. ✅ Explore as configurações em `config.py`
3. ✅ Teste com diferentes tipos de questões
4. ✅ Ajuste parâmetros para seu uso

---

## 💡 Recursos Adicionais

- **README.md** - Documentação completa
- **INSTALL.md** - Guia de instalação detalhado
- **CHANGELOG.md** - Histórico de versões
- **test_setup.py** - Teste de configuração

---

## 🆘 Precisa de Ajuda?

1. Execute `python test_setup.py` para diagnóstico
2. Veja `logs/screensolver.log` para erros
3. Consulte [README.md](README.md) seção "Solução de Problemas"

---

**Pronto! Você está usando ScreenSolver AI! 🎉**

Pressione F8 e comece a resolver questões!
