# Script de Instalacao Automatica do Tesseract OCR
# Executa download e instalacao silenciosa

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Instalador Tesseract OCR para ScreenSolver AI" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# URL do instalador Tesseract (versao 5.4.1.20240701 - mais recente estavel)
$downloadUrl = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.1.20240701/tesseract-ocr-w64-setup-5.4.1.20240701.exe"
$installerPath = "$env:TEMP\tesseract-installer.exe"

# Verifica se ja esta instalado
try {
    $existingVersion = tesseract --version 2>$null
    if ($existingVersion) {
        Write-Host "✓ Tesseract ja esta instalado!" -ForegroundColor Green
        Write-Host "  Versao: $existingVersion" -ForegroundColor Green
        Write-Host ""
        Write-Host "Nenhuma acao necessaria." -ForegroundColor Yellow
        Read-Host "Pressione Enter para sair"
        exit 0
    }
} catch {
    # Nao instalado, continuar
}

Write-Host "[1/4] Preparando download..." -ForegroundColor Yellow
Write-Host "  URL: $downloadUrl" -ForegroundColor Gray

# Download do instalador
Write-Host ""
Write-Host "[2/4] Baixando Tesseract OCR (~40MB)..." -ForegroundColor Yellow
Write-Host "  Isso pode levar alguns minutos..." -ForegroundColor Gray

try {
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing -ErrorAction Stop
    Write-Host "  ✓ Download concluido" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Erro no download" -ForegroundColor Red
    Write-Host "  Erro: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solucao manual:" -ForegroundColor Yellow
    Write-Host "  1. Acesse: https://github.com/UB-Mannheim/tesseract/wiki" -ForegroundColor Yellow
    Write-Host "  2. Baixe o instalador" -ForegroundColor Yellow
    Write-Host "  3. Execute e instale" -ForegroundColor Yellow
    Read-Host "Pressione Enter"
    exit 1
}

Write-Host ""
Write-Host "[3/4] Instalando Tesseract OCR..." -ForegroundColor Yellow
Write-Host "  Executando instalador..." -ForegroundColor Gray

# Executa instalador silenciosamente com idiomas Portugues e Ingles
$installArgs = @(
    "/S",                    # Modo silencioso
    "/D=C:\Program Files\Tesseract-OCR"  # Diretorio de instalacao
)

try {
    $process = Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait -PassThru -ErrorAction Stop
    
    if ($process.ExitCode -eq 0) {
        Write-Host "  ✓ Instalacao concluida" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Instalacao retornou codigo: $($process.ExitCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ✗ Erro na instalacao: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Tente instalar manualmente:" -ForegroundColor Yellow
    Write-Host "  Execute: $installerPath" -ForegroundColor Yellow
    Read-Host "Pressione Enter"
    exit 1
}

# Adiciona ao PATH
Write-Host ""
Write-Host "[4/4] Configurando PATH do sistema..." -ForegroundColor Yellow

$tesseractPath = "C:\Program Files\Tesseract-OCR"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")

if ($currentPath -notlike "*$tesseractPath*") {
    try {
        $newPath = $currentPath + ";" + $tesseractPath
        [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
        Write-Host "  ✓ PATH atualizado" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ Nao foi possivel atualizar PATH automaticamente" -ForegroundColor Yellow
        Write-Host "  Adicione manualmente: $tesseractPath" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✓ PATH ja configurado" -ForegroundColor Green
}

# Verifica instalacao
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Verificando instalacao..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Atualiza PATH na sessao atual
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine")

try {
    $version = tesseract --version 2>$null
    if ($version) {
        Write-Host "✓✓✓ SUCESSO! ✓✓✓" -ForegroundColor Green
        Write-Host ""
        Write-Host "Tesseract OCR instalado com sucesso!" -ForegroundColor Green
        Write-Host "  Versao: $version" -ForegroundColor Green
        Write-Host ""
        Write-Host "Pronto para usar ScreenSolver AI!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Proximo passo:" -ForegroundColor Yellow
        Write-Host "  Reinicie o ScreenSolver AI (python main.py)" -ForegroundColor Yellow
    } else {
        Write-Host "⚠ Tesseract instalado mas nao encontrado no PATH" -ForegroundColor Yellow
        Write-Host "  Reinicie o terminal/computador e tente novamente" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ Instalacao concluida mas Tesseract nao encontrado" -ForegroundColor Yellow
    Write-Host "  Reinicie o computador e tente novamente" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Pressione Enter para sair"

# Limpa instalador
Remove-Item $installerPath -ErrorAction SilentlyContinue
