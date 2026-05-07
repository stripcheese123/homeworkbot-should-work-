@echo off
REM ============================================================================
REM ScreenSolver AI - Script de Execução para Windows
REM ============================================================================
REM 
REM Este script facilita a execução do ScreenSolver AI no Windows.
REM Basta clicar duas vezes neste arquivo para iniciar o programa.
REM
REM ============================================================================

echo.
echo ============================================================
echo   ScreenSolver AI - Iniciando...
echo ============================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.11+ e adicione ao PATH.
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Verifica se Tesseract está instalado
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Tesseract OCR nao encontrado!
    echo.
    echo O programa pode nao funcionar corretamente.
    echo Download: https://github.com/UB-Mannheim/tesseract/wiki
    echo.
)

REM Verifica se Ollama está rodando
curl -s http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Ollama nao esta rodando!
    echo.
    echo Iniciando Ollama...
    start /B ollama serve
    timeout /t 3 >nul
    echo.
)

echo [OK] Ollama rodando
echo.

REM Navega para o diretório do script
cd /d "%~dp0"

echo Iniciando ScreenSolver AI...
echo.
echo Instrucoes:
echo   - Pressione F8 para capturar tela
echo   - Pressione ESC para cancelar selecao
echo   - Feche a janela para sair
echo.
echo ============================================================
echo.

REM Executa o programa
python main.py

REM Se houver erro
if errorlevel 1 (
    echo.
    echo ============================================================
    echo [ERRO] O programa encerrou com erro!
    echo.
    echo Verifique:
    echo   1. Todas as dependencias estao instaladas
    echo   2. Ollama esta rodando
    echo   3. Modelo qwen3:59b esta baixado
    echo.
    echo Consulte README.md para mais informacoes.
    echo ============================================================
    echo.
    pause
)
