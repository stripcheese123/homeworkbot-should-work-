@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo   Instalador Tesseract OCR para ScreenSolver AI
echo ============================================================
echo.

REM Verifica se ja esta instalado
tesseract --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Tesseract ja esta instalado!
    tesseract --version 2>&1 | find "tesseract"
    echo.
    echo Nenhuma acao necessaria.
    pause
    exit /b 0
)

echo [1/3] Baixando Tesseract OCR...
echo   URL: https://github.com/UB-Mannheim/tesseract/releases
echo   Isso pode levar alguns minutos...
echo.

REM Download usando PowerShell
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.1.20240701/tesseract-ocr-w64-setup-5.4.1.20240701.exe' -OutFile '%TEMP%\tesseract-installer.exe' -UseBasicParsing"

if %errorlevel% neq 0 (
    echo [ERRO] Falha no download
    echo.
    echo Solucao manual:
    echo   1. Acesse: https://github.com/UB-Mannheim/tesseract/wiki
    echo   2. Baixe o instalador
    echo   3. Execute e instale
    pause
    exit /b 1
)

echo [OK] Download concluido
echo.
echo [2/3] Instalando Tesseract OCR...
echo   Execute o instalador...
echo.

REM Executa instalador (nao silencioso para usuario ver progresso)
start /wait %TEMP%\tesseract-installer.exe

echo.
echo [3/3] Configurando...

REM Adiciona ao PATH da sessao atual
set "PATH=%PATH%;C:\Program Files\Tesseract-OCR"

echo.
echo ============================================================
echo   Verificando instalacao...
echo ============================================================
echo.

tesseract --version >nul 2>&1
if %errorlevel% == 0 (
    echo [SUCESSO] Tesseract OCR instalado!
    tesseract --version 2>&1 | find "tesseract"
    echo.
    echo Proximo passo:
    echo   Reinicie o ScreenSolver AI
    echo.
    echo Pressione qualquer tecla para sair...
) else (
    echo [AVISO] Instalacao concluida
    echo   Reinicie o computador e tente novamente
    echo.
    pause
)

REM Limpa arquivo
del %TEMP%\tesseract-installer.exe 2>nul
