@echo off
REM Setup rapido per Windows

echo ========================================================================
echo 🏗️  SISTEMA METEO CANTIERE - Setup Rapido (Windows)
echo ========================================================================
echo.

REM Verifica Python
echo 📌 PASSO 1: Verifica Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ Python installato
    set PYTHON_CMD=python
) else (
    echo    ❌ Python NON installato!
    echo    Installa Python da: https://www.python.org/downloads/
    echo    IMPORTANTE: Spunta "Add Python to PATH" durante installazione
    pause
    exit /b 1
)
echo.

REM Verifica pip
echo 📌 PASSO 2: Verifica pip...
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ pip installato
) else (
    echo    ❌ pip NON installato!
    pause
    exit /b 1
)
echo.

REM Installa dipendenze
echo 📌 PASSO 3: Installa dipendenze...
echo    Installazione pandas e numpy in corso...
pip install pandas numpy -q
if %errorlevel% equ 0 (
    echo    ✅ Dipendenze installate
) else (
    echo    ⚠️  Possibili warning durante installazione (normale)
)
echo.

REM Test sistema
echo 📌 PASSO 4: Test sistema...
echo    Esecuzione test_analyzer.py...
echo.
python test_analyzer.py
set TEST_RESULT=%errorlevel%
echo.

if %TEST_RESULT% equ 0 (
    echo ========================================================================
    echo ✅ SISTEMA FUNZIONANTE!
    echo ========================================================================
    echo.
    echo 📚 Prossimi passi:
    echo    1. Leggi: STATO_PROGETTO.md (panoramica generale^)
    echo    2. Leggi: PROSSIMI_PASSI.md (checklist operativa^)
    echo    3. Esegui: python demo.py (menu interattivo^)
    echo.
    echo 🎯 Comandi utili:
    echo    python demo.py stations      # Mostra stazioni disponibili
    echo    python demo.py criteria      # Mostra criteri sicurezza
    echo    python demo.py examples      # Mostra esempi utilizzo
    echo.
) else (
    echo ========================================================================
    echo ❌ ERRORE NEL TEST
    echo ========================================================================
    echo.
    echo Possibili cause:
    echo    - Dipendenze mancanti: prova 'pip install pandas numpy'
    echo    - File mancanti: verifica di essere nella cartella giusta
    echo.
    echo Consulta: PROSSIMI_PASSI.md sezione 'Problemi Comuni'
)

echo ========================================================================
pause
