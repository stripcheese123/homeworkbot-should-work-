"""
ScreenSolver AI - Script de Teste de Configuração
==================================================
Execute este script para verificar se tudo está instalado corretamente.

Uso:
    python test_setup.py
"""

import sys
import os

print("=" * 70)
print("  ScreenSolver AI - Teste de Configuração")
print("=" * 70)
print()

# ============================================================================
# TESTE 1: Python
# ============================================================================

print("1️⃣  Testando Python...")
print(f"   Versão: {sys.version}")

if sys.version_info < (3, 11):
    print("   ❌ ERRO: Python 3.11+ é necessário")
    sys.exit(1)
else:
    print("   ✅ OK: Python compatível")

print()

# ============================================================================
# TESTE 2: Dependências Python
# ============================================================================

print("2️⃣  Testando dependências Python...")

required_packages = [
    "PIL",
    "customtkinter",
    "pytesseract",
    "cv2",
    "numpy",
    "keyboard",
    "requests",
    "pyautogui"
]

missing_packages = []

for package in required_packages:
    try:
        if package == "PIL":
            import PIL
            print(f"   ✅ {package} (Pillow {PIL.__version__})")
        elif package == "cv2":
            import cv2
            print(f"   ✅ {package} (OpenCV {cv2.__version__})")
        else:
            module = __import__(package)
            version = getattr(module, "__version__", "desconhecida")
            print(f"   ✅ {package} ({version})")
    except ImportError:
        print(f"   ❌ {package} - NÃO INSTALADO")
        missing_packages.append(package)

if missing_packages:
    print()
    print(f"   ⚠️  Pacotes faltando: {', '.join(missing_packages)}")
    print(f"   Execute: pip install -r requirements.txt")
    print()
else:
    print()
    print("   ✅ Todas as dependências instaladas!")
    print()

# ============================================================================
# TESTE 3: Tesseract OCR
# ============================================================================

print("3️⃣  Testando Tesseract OCR...")

try:
    import pytesseract
    
    # Tenta obter versão
    version = pytesseract.get_tesseract_version()
    print(f"   ✅ Tesseract instalado: {version}")
    
    # Testa OCR básico
    from PIL import Image, ImageDraw, ImageFont
    
    # Cria imagem de teste
    test_img = Image.new('RGB', (300, 100), color='white')
    draw = ImageDraw.Draw(test_img)
    draw.text((10, 30), "Teste OCR", fill='black')
    
    # Tenta extrair texto
    text = pytesseract.image_to_string(test_img, lang='por')
    
    if "Teste" in text or "OCR" in text:
        print("   ✅ OCR funcionando corretamente")
    else:
        print("   ⚠️  OCR pode não estar funcionando corretamente")
        print(f"   Texto detectado: '{text.strip()}'")

except pytesseract.TesseractNotFoundError:
    print("   ❌ ERRO: Tesseract não encontrado!")
    print("   Instale o Tesseract OCR:")
    print("   https://github.com/UB-Mannheim/tesseract/wiki")
    print()
    print("   Adicione ao PATH do sistema:")
    print("   C:\\Program Files\\Tesseract-OCR")

except Exception as e:
    print(f"   ❌ ERRO ao testar Tesseract: {e}")

print()

# ============================================================================
# TESTE 4: Ollama
# ============================================================================

print("4️⃣  Testando Ollama...")

try:
    import requests
    
    # Testa conexão
    response = requests.get("http://localhost:11434", timeout=5)
    
    if response.status_code == 200:
        print("   ✅ Ollama está rodando")
        
        # Lista modelos
        models_response = requests.get("http://localhost:11434/api/tags", timeout=10)
        
        if models_response.status_code == 200:
            data = models_response.json()
            models = [m['name'] for m in data.get('models', [])]
            
            print(f"   Modelos instalados: {len(models)}")
            
            for model in models:
                print(f"      - {model}")
            
            # Verifica se qwen3:59b está instalado
            if "qwen3:59b" in models:
                print()
                print("   ✅ Modelo qwen3:59b encontrado!")
            else:
                print()
                print("   ⚠️  Modelo qwen3:59b NÃO encontrado")
                print("   Execute: ollama pull qwen3:59b")
        
    else:
        print(f"   ❌ Ollama retornou status: {response.status_code}")

except requests.exceptions.ConnectionError:
    print("   ❌ ERRO: Ollama não está rodando!")
    print("   Inicie o Ollama:")
    print("   ollama serve")

except Exception as e:
    print(f"   ❌ ERRO ao testar Ollama: {e}")

print()

# ============================================================================
# TESTE 5: GPU NVIDIA (opcional)
# ============================================================================

print("5️⃣  Testando GPU NVIDIA (opcional)...")

try:
    import subprocess
    
    result = subprocess.run(
        ["nvidia-smi"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if result.returncode == 0:
        print("   ✅ GPU NVIDIA detectada")
        
        # Extrai informações básicas
        output = result.stdout
        if "RTX 4060" in output:
            print("   ✅ RTX 4060 encontrada!")
        
        # Mostra uso de memória
        lines = output.split('\n')
        for line in lines:
            if 'MiB' in line and '/' in line:
                print(f"   Memória GPU: {line.strip()}")
                break
    else:
        print("   ⚠️  nvidia-smi falhou")

except FileNotFoundError:
    print("   ⚠️  GPU NVIDIA não detectada (opcional)")
    print("   O programa funcionará, mas será mais lento")

except Exception as e:
    print(f"   ⚠️  Erro ao verificar GPU: {e}")

print()

# ============================================================================
# TESTE 6: Permissões (Windows)
# ============================================================================

print("6️⃣  Testando permissões...")

try:
    import ctypes
    
    is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    
    if is_admin:
        print("   ✅ Executando como Administrador")
    else:
        print("   ⚠️  NÃO está executando como Administrador")
        print("   Hotkeys globais podem não funcionar")
        print("   Recomendado: Execute como Administrador")

except:
    print("   ⚠️  Não foi possível verificar permissões")

print()

# ============================================================================
# RESUMO
# ============================================================================

print("=" * 70)
print("  RESUMO")
print("=" * 70)
print()

if not missing_packages:
    print("✅ Sistema pronto para executar ScreenSolver AI!")
    print()
    print("Para iniciar:")
    print("   python main.py")
    print()
    print("Ou clique duas vezes em:")
    print("   run.bat")
else:
    print("❌ Sistema NÃO está pronto")
    print()
    print("Instale as dependências faltando:")
    print("   pip install -r requirements.txt")

print()
print("=" * 70)
