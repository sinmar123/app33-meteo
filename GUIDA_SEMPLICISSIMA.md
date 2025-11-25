# 🎯 GUIDA SUPER SEMPLICE - App Meteo Cantiere

## ⚡ Avvio Veloce (2 click!)

### Windows:
1. **Doppio click** su `start.bat`
2. Aspetta che si apra il browser
3. **FATTO!** 🎉

### Mac/Linux:
1. **Doppio click** su `start.sh`
   (oppure da Terminale: `./start.sh`)
2. Aspetta che si apra il browser
3. **FATTO!** 🎉

---

## 📱 Come Usare l'App

### Quando si apre il browser vedrai:

```
┌─────────────────────────────────────────────────────────┐
│  🏗️ Sistema Meteo e Sicurezza Cantiere                 │
│                                                          │
│  Barra laterale sinistra:                               │
│  ├─ 📍 Seleziona Stazione (es: GENOVA)                  │
│  ├─ 📅 Seleziona Data                                   │
│  └─ 📁 Carica file CSV (o usa esempio)                  │
│                                                          │
│  Centro:                                                 │
│  └─ 🔍 Pulsante "ANALIZZA"                              │
│                                                          │
│  Risultati:                                              │
│  ├─ Score Sicurezza (0-100)                             │
│  ├─ Categoria (OTTIMO, BUONO, etc.)                     │
│  ├─ ✅/❌ Si può lavorare?                               │
│  ├─ 📊 Grafici                                          │
│  ├─ ⚠️ Avvisi                                           │
│  └─ 🔨 Idoneità per tipo lavoro                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎬 Passo-Passo con Screenshot Immaginari

### 1️⃣ Primo Avvio

**Cosa fare:**
- Doppio click su `start.bat` (Windows) o `start.sh` (Mac/Linux)

**Cosa vedrai:**
```
🏗️  AVVIO APP METEO CANTIERE
✅ Python trovato
📥 Installazione dipendenze...
🌐 Avvio applicazione web...
```

**Tempo:** 30 secondi (primo avvio) / 5 secondi (successivi)

---

### 2️⃣ Si Apre il Browser

**Automatico!** Si apre una scheda con: `http://localhost:8501`

**Se NON si apre:** Apri manualmente il browser e vai su:
```
http://localhost:8501
```

---

### 3️⃣ Configura l'Analisi (Barra Sinistra)

**a) Seleziona Stazione:**
```
📍 Seleziona Stazione
   [▼ GE036 - GENOVA - CENTRO FUNZIONALE]
```
Scegli dalla lista (250 stazioni disponibili)

**b) Seleziona Data:**
```
📅 Data Analisi
   [📅 18/11/2024]
```
Click sul calendario per scegliere

**c) Carica Dati:**
```
☑️ Usa dati di esempio    ← Per provare subito!

OPPURE

☐ Usa dati di esempio
📁 Carica file CSV
   [Trascina qui il file o click per selezionare]
```

---

### 4️⃣ Premi il Pulsante Magico

**Centro pagina:**
```
┌────────────────────────────────────┐
│  🔍 ANALIZZA SICUREZZA CANTIERE   │
└────────────────────────────────────┘
```

**Click!** → Analisi automatica in 2 secondi

---

### 5️⃣ Guarda i Risultati

**Vedrai:**

```
📊 RISULTATI ANALISI

📅 Data: 18/11/2024        📍 Stazione: GENOVA

┌─────────────────┐        🎯 Valutazione Complessiva
│                 │
│   Score: 83.5   │        ✅ OTTIMO
│                 │        Condizioni ottime per lavorare
│   [GAUGE]       │
└─────────────────┘        ✅ LAVORI IN CANTIERE: CONSENTITI

📈 Dettaglio Parametri Meteo
[GRAFICO A BARRE]
Precipitazione: 70/100
Vento: 70/100
Temperatura: 100/100
...

⚠️ Avvisi e Raccomandazioni
• Pioggia leggera: 0.8 mm/h
• Vento moderato: 6.8 m/s

🔨 Idoneità per Tipo di Lavoro
✅ SCAVI: Condizioni buone
✅ OPERE IN QUOTA: Ottime condizioni
✅ GETTO CLS: Ottime condizioni
...

💾 Esporta Report
[📄 Scarica Report TXT]  [📊 Scarica Dati CSV]
```

---

## 💡 Trucchi e Suggerimenti

### Primo test rapido (senza dati reali)
1. Lascia spuntato "Usa dati di esempio"
2. Premi "ANALIZZA"
3. Vedi come funziona!

### Uso con dati reali
1. Vai su sito Regione Liguria
2. Scarica CSV dati meteo del giorno
3. Togli spunta "Usa dati di esempio"
4. Carica il tuo file
5. Premi "ANALIZZA"

### Cambiare stazione
- Click sul menu a tendina
- Cerca digitando (es: "GENOVA")
- Seleziona quella che ti interessa

### Cambiare data
- Click sul calendario
- Scegli il giorno
- Premi "ANALIZZA" di nuovo

---

## 🔧 Problemi?

### "Python non installato"
→ Scarica da: https://www.python.org/downloads/
→ Windows: spunta "Add Python to PATH"!

### "L'app non si apre"
→ Apri browser manualmente: http://localhost:8501

### "Errore caricamento file"
→ Verifica che il CSV abbia le colonne:
  - temperatura
  - precipitazione
  - vento_velocita
  - umidita
  - visibilita

### "Il grafico è vuoto"
→ Ricarica la pagina (F5)

---

## 🎨 Cosa Vedi nell'App

### Colori Score:
- 🟢 **Verde** (80-100): OTTIMO
- 🟡 **Giallo** (50-79): ACCETTABILE
- 🔴 **Rosso** (0-49): CRITICO

### Icone:
- ✅ = Tutto OK, si può lavorare
- ⚠️ = Attenzione, fare cautela
- ❌ = Non lavorare, troppo pericoloso
- 🚫 = VIETATO

---

## 📞 Aiuto Veloce

**L'app non parte?**
```bash
# Prova da Terminale/CMD:
python -m streamlit run app.py
```

**Vuoi fermare l'app?**
- Chiudi la finestra del terminale
- Oppure: Ctrl+C nel terminale

**Vuoi riavviare?**
- Doppio click su `start.bat` / `start.sh` di nuovo

---

## 🎯 Ricapitolando

**Per usare l'app bastano 3 CLICK:**

1. **Doppio click** su `start.bat` / `start.sh`
2. **Click** sul pulsante "ANALIZZA"
3. **Click** su "Scarica Report" (se vuoi salvare)

**ZERO configurazione, ZERO linea di comando!**

---

## 🚀 Prossimi Passi (Opzionali)

- Personalizza soglie in `config.py`
- Scarica dati reali dal sito Regione Liguria
- Usa l'app ogni mattina per decidere se lavorare

---

**BUON LAVORO E CANTIERI SICURI!** 🏗️⛑️
