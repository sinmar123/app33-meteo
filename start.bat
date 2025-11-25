@echo off
REM 🚀 Avvio APP Meteo Cantiere - Windows

echo ========================================================================
echo 🏗️  AVVIO APP METEO CANTIERE
echo ========================================================================
echo.

REM Verifica Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non installato!
    echo Installa Python da: https://www.python.org/downloads/
    echo IMPORTANTE: Spunta "Add Python to PATH" durante installazione
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python trovato: %PYTHON_VERSION%
echo.

REM Controlla streamlit
echo 📦 Controllo dipendenze...
python -c "import streamlit" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Streamlit già installato
) else (
    echo 📥 Installazione dipendenze in corso...
    echo    (potrebbe richiedere 1-2 minuti la prima volta^)
    echo.
    pip install streamlit pandas numpy plotly python-dateutil -q

    if %errorlevel% equ 0 (
        echo ✅ Dipendenze installate con successo!
    ) else (
        echo ⚠️  Possibili warning (normale^)
    )
)

echo.
echo ========================================================================
echo 🌐 Avvio applicazione web...
echo ========================================================================
echo.
echo L'app si aprirà automaticamente nel browser tra pochi secondi...
echo Se non si apre, vai su: http://localhost:8501
echo.
echo Per fermare l'app: chiudi questa finestra o premi Ctrl+C
echo ========================================================================
echo.

REM Avvia Streamlit
python -m streamlit run app.py

pause
