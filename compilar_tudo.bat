@echo off
chcp 65001 >nul
echo ========================================
echo   COMPILANDO SISTEMA DE PRODUCAO
echo ========================================
echo.

echo [1/3] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo ✅ Limpeza concluída
echo.

echo [2/3] Compilando Sistema Principal...
pyinstaller --onefile --windowed --name="ColetorProducao" ^
  --hidden-import=pandas ^
  --hidden-import=openpyxl ^
  --hidden-import=psutil ^
  --hidden-import=tkinter ^
  main.py

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar sistema principal!
    pause
    exit /b 1
)
echo ✅ Sistema principal compilado
echo.

echo [3/3] Compilando Dashboard...
pyinstaller --onefile --name="Dashboard" ^
  --hidden-import=dash ^
  --hidden-import=plotly ^
  --hidden-import=pandas ^
  dashboard_standalone.py

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar dashboard!
    pause
    exit /b 1
)
echo ✅ Dashboard compilado
echo.

echo ========================================
echo   COMPILACAO CONCLUIDA COM SUCESSO!
echo ========================================
echo.
echo 📦 Arquivos gerados em: dist\
echo    ✅ ColetorProducao.exe
echo    ✅ Dashboard.exe
echo.
echo 📁 Tamanho dos arquivos:
dir dist\*.exe
echo.
echo ⚠️  IMPORTANTE: Teste os executáveis antes de distribuir!
echo.
pause
