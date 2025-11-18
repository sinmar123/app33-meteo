#!/bin/bash
# Setup rapido per riprendere il lavoro

echo "========================================================================"
echo "🏗️  SISTEMA METEO CANTIERE - Setup Rapido"
echo "========================================================================"
echo ""

# Verifica Python
echo "📌 PASSO 1: Verifica Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ Python installato: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "   ✅ Python installato: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    echo "   ❌ Python NON installato!"
    echo "   Installa Python da: https://www.python.org/downloads/"
    exit 1
fi
echo ""

# Verifica pip
echo "📌 PASSO 2: Verifica pip..."
if command -v pip3 &> /dev/null; then
    echo "   ✅ pip installato"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo "   ✅ pip installato"
    PIP_CMD="pip"
else
    echo "   ❌ pip NON installato!"
    exit 1
fi
echo ""

# Installa dipendenze
echo "📌 PASSO 3: Installa dipendenze..."
echo "   Installazione pandas e numpy in corso..."
$PIP_CMD install pandas numpy -q 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ Dipendenze installate"
else
    echo "   ⚠️  Possibili warning durante installazione (normale)"
fi
echo ""

# Test sistema
echo "📌 PASSO 4: Test sistema..."
echo "   Esecuzione test_analyzer.py..."
echo ""
$PYTHON_CMD test_analyzer.py
TEST_RESULT=$?
echo ""

if [ $TEST_RESULT -eq 0 ]; then
    echo "========================================================================"
    echo "✅ SISTEMA FUNZIONANTE!"
    echo "========================================================================"
    echo ""
    echo "📚 Prossimi passi:"
    echo "   1. Leggi: STATO_PROGETTO.md (panoramica generale)"
    echo "   2. Leggi: PROSSIMI_PASSI.md (checklist operativa)"
    echo "   3. Esegui: $PYTHON_CMD demo.py (menu interattivo)"
    echo ""
    echo "🎯 Comandi utili:"
    echo "   $PYTHON_CMD demo.py stations      # Mostra stazioni disponibili"
    echo "   $PYTHON_CMD demo.py criteria      # Mostra criteri sicurezza"
    echo "   $PYTHON_CMD demo.py examples      # Mostra esempi utilizzo"
    echo ""
else
    echo "========================================================================"
    echo "❌ ERRORE NEL TEST"
    echo "========================================================================"
    echo ""
    echo "Possibili cause:"
    echo "   - Dipendenze mancanti: prova 'pip install pandas numpy'"
    echo "   - File mancanti: verifica di essere nella cartella giusta"
    echo ""
    echo "Consulta: PROSSIMI_PASSI.md sezione 'Problemi Comuni'"
fi

echo "========================================================================"
