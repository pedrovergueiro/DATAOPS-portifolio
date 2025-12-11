@echo off
echo ========================================
echo   COMPILACAO COM OPCOES DE DEBUG
echo ========================================
echo.

echo Escolha o tipo de compilacao:
echo   1. INTERFACE GRAFICA (sem terminal - para producao)
echo   2. COM CONSOLE (com terminal - para debug)
echo.
set /p opcao="Digite 1 ou 2: "

if "%opcao%"=="1" (
    set CONSOLE_MODE=--windowed
    set CONSOLE_TEXT=INTERFACE GRAFICA
) else (
    set CONSOLE_MODE=--console
    set CONSOLE_TEXT=COM CONSOLE DEBUG
)

echo.
echo Compilando no modo: %CONSOLE_TEXT%
echo.

echo [1/3] Verificando Python...
python --version
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)

echo [2/3] Instalando dependencias...
python -m pip install --upgrade pip pyinstaller pandas numpy psutil matplotlib plotly dash pyautogui Pillow tkinter-tooltip tkcalendar

echo [3/3] Compilando Sistema Principal...
python -m PyInstaller ^
  --onefile ^
  %CONSOLE_MODE% ^
  --name="ColetorProducao" ^
  --clean ^
  --noconfirm ^
  --add-data "config;config" ^
  --add-data "data;data" ^
  --add-data "models;models" ^
  --add-data "utils;utils" ^
  --add-data "gui;gui" ^
  --add-data "ml;ml" ^
  --hidden-import=pandas ^
  --hidden-import=numpy ^
  --hidden-import=psutil ^
  --hidden-import=matplotlib ^
  --hidden-import=plotly ^
  --hidden-import=dash ^
  --hidden-import=tkinter ^
  --hidden-import=tkinter.ttk ^
  --hidden-import=tkinter.messagebox ^
  --hidden-import=threading ^
  --hidden-import=json ^
  --hidden-import=datetime ^
  --hidden-import=uuid ^
  --hidden-import=socket ^
  --hidden-import=pyautogui ^
  --hidden-import=PIL ^
  main.py

if errorlevel 1 (
    echo ERRO na compilacao!
    pause
    exit /b 1
)

echo Copiando arquivos auxiliares...
copy "testar_comando_remoto.py" "dist\" >nul 2>&1
copy "monitorar_maquinas.py" "dist\" >nul 2>&1
copy "config_executavel.py" "dist\" >nul 2>&1

echo ========================================
echo   COMPILACAO CONCLUIDA!
echo ========================================
echo.
echo Modo: %CONSOLE_TEXT%
echo Arquivo: dist\ColetorProducao.exe
echo.
if "%opcao%"=="1" (
    echo ✅ Interface grafica limpa (sem terminal)
    echo ✅ Pronto para producao
) else (
    echo ✅ Console visivel para debug
    echo ✅ Pode ver erros e logs
)
echo.
echo Para testar: dist\ColetorProducao.exe
echo.
pause