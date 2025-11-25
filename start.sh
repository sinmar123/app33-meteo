#!/bin/bash
# 🚀 Avvio APP Meteo Cantiere - Linux/Mac/MSYS2

echo "========================================================================"
echo "🏗️  AVVIO APP METEO CANTIERE"
echo "========================================================================"
echo ""

# Verifica Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python non installato!"
    echo "Installa Python da: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python trovato: $($PYTHON_CMD --version)"
echo ""

# Crea ambiente virtuale se non esiste
if [ ! -d "venv" ]; then
    echo "📦 Creazione ambiente virtuale (prima volta)..."
    $PYTHON_CMD -m venv venv

    if [ $? -eq 0 ]; then
        echo "✅ Ambiente virtuale creato!"
    else
        echo "❌ Errore creazione ambiente virtuale"
        echo ""
        echo "Prova manualmente:"
        echo "  $PYTHON_CMD -m venv venv"
        exit 1
    fi
    echo ""
fi

# Attiva ambiente virtuale
echo "🔧 Attivazione ambiente virtuale..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "❌ Impossibile trovare script di attivazione venv"
    exit 1
fi

echo "✅ Ambiente virtuale attivo"
echo ""

# Controlla se streamlit è installato nell'ambiente virtuale
echo "📦 Controllo dipendenze..."
if python -c "import streamlit" 2>/dev/null; then
    echo "✅ Streamlit già installato"
else
    echo "📥 Installazione dipendenze in corso..."
    echo "   (potrebbe richiedere 1-2 minuti la prima volta)"
    echo ""
    pip install streamlit pandas numpy plotly python-dateutil

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Dipendenze installate con successo!"
    else
        echo ""
        echo "⚠️  Installazione completata con warning (potrebbe essere normale)"
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
python -m streamlit run app.py --server.headless true
