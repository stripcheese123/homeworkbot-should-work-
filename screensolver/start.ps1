# ScreenSolver AI - Script de Inicializacao
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  ScreenSolver AI - Inicializando..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verifica Ollama
Write-Host "[1/3] Verificando Ollama..." -ForegroundColor Yellow
try {
    $null = Invoke-WebRequest -Uri "http://localhost:11434" -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
    Write-Host "  OK - Ollama esta rodando" -ForegroundColor Green
} catch {
    Write-Host "  AVISO - Ollama nao esta rodando" -ForegroundColor Yellow
    Write-Host "  Execute: ollama serve" -ForegroundColor Yellow
}

Write-Host ""

# Verifica modelo
Write-Host "[2/3] Verificando modelo qwen3.5:9b..." -ForegroundColor Yellow
try {
    $models = ollama list 2>$null | Out-String
    if ($models -match "qwen3.5") {
        Write-Host "  OK - Modelo encontrado" -ForegroundColor Green
    } else {
        Write-Host "  AVISO - Modelo nao encontrado" -ForegroundColor Yellow
        Write-Host "  Execute: ollama pull qwen3.5:9b" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  AVISO - Nao foi possivel verificar" -ForegroundColor Yellow
}

Write-Host ""

# Verifica Tesseract
Write-Host "[3/3] Verificando Tesseract (opcional)..." -ForegroundColor Yellow
try {
    $null = tesseract --version 2>$null
    Write-Host "  OK - Tesseract instalado" -ForegroundColor Green
} catch {
    Write-Host "  AVISO - Tesseract nao instalado (OCR nao funcionara)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Iniciando ScreenSolver AI..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Executa
python main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Erro ao executar!" -ForegroundColor Red
    Read-Host "Pressione Enter"
}
