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

REM Crea ambiente virtuale se non esiste
if not exist "venv" (
    echo 📦 Creazione ambiente virtuale (prima volta^)...
    python -m venv venv

    if %errorlevel% equ 0 (
        echo ✅ Ambiente virtuale creato!
    ) else (
        echo ❌ Errore creazione ambiente virtuale
        echo.
        echo Prova manualmente:
        echo   python -m venv venv
        pause
        exit /b 1
    )
    echo.
)

REM Attiva ambiente virtuale
echo 🔧 Attivazione ambiente virtuale...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Ambiente virtuale attivo
) else (
    echo ❌ Impossibile trovare script di attivazione venv
    pause
    exit /b 1
)
echo.

REM Controlla streamlit nell'ambiente virtuale
echo 📦 Controllo dipendenze...
python -c "import streamlit" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Streamlit già installato
) else (
    echo 📥 Installazione dipendenze in corso...
    echo    (potrebbe richiedere 1-2 minuti la prima volta^)
    echo.
    pip install streamlit pandas numpy plotly python-dateutil

    if %errorlevel% equ 0 (
        echo.
        echo ✅ Dipendenze installate con successo!
    ) else (
        echo.
        echo ⚠️  Installazione completata con warning (potrebbe essere normale^)
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
