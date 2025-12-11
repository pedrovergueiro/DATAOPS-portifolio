@echo off
echo ========================================
echo   VISUALIZADOR DE LOGS - COLETOR
echo ========================================
echo.

echo Escolha uma opcao:
echo   1. Abrir logs no Notepad
echo   2. Abrir pasta de logs
echo   3. Mostrar logs no console
echo   4. Menu interativo completo
echo.
set /p opcao="Digite 1, 2, 3 ou 4: "

if "%opcao%"=="1" (
    python abrir_logs.py notepad
) else if "%opcao%"=="2" (
    python abrir_logs.py pasta
) else if "%opcao%"=="3" (
    python abrir_logs.py console
    pause
) else if "%opcao%"=="4" (
    python abrir_logs.py
) else (
    echo Opcao invalida!
    pause
)