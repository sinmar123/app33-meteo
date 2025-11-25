#!/bin/bash
# 🚀 Avvio APP Meteo Cantiere - Linux/Mac

echo "========================================================================"
echo "🏗️  AVVIO APP METEO CANTIERE"
echo "========================================================================"
echo ""

# Verifica Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "❌ Python non installato!"
    echo "Installa Python da: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python trovato: $($PYTHON_CMD --version)"
echo ""

# Controlla se streamlit è installato
echo "📦 Controllo dipendenze..."
if $PYTHON_CMD -c "import streamlit" 2>/dev/null; then
    echo "✅ Streamlit già installato"
else
    echo "📥 Installazione dipendenze in corso..."
    echo "   (potrebbe richiedere 1-2 minuti la prima volta)"
    echo ""
    $PIP_CMD install streamlit pandas numpy plotly python-dateutil -q

    if [ $? -eq 0 ]; then
        echo "✅ Dipendenze installate con successo!"
    else
        echo "⚠️  Possibili warning (normale)"
    fi
fi

echo ""
echo "========================================================================"
echo "🌐 Avvio applicazione web..."
echo "========================================================================"
echo ""
echo "L'app si aprirà automaticamente nel browser tra pochi secondi..."
echo "Se non si apre, vai su: http://localhost:8501"
echo ""
echo "Per fermare l'app: premi Ctrl+C"
echo "========================================================================"
echo ""

# Avvia Streamlit
$PYTHON_CMD -m streamlit run app.py --server.headless true
