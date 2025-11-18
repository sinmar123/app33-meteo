# Sistema Analisi Meteo e Sicurezza Cantiere - Regione Liguria

Sistema automatizzato per lo scaricamento di dati meteorologici dalla Regione Liguria e valutazione delle condizioni di sicurezza per lavori in cantiere.

## 🎯 Funzionalità

- **Web Scraping**: Download automatico dati meteo dal portale Regione Liguria
- **Analisi Sicurezza**: Valutazione automatica idoneità giornaliera per lavori in cantiere
- **Report Dettagliati**: Generazione report con raccomandazioni specifiche
- **Multi-stazione**: Gestione simultanea di multiple stazioni meteo
- **Analisi Periodi**: Valutazione su intervalli di date con statistiche aggregate
- **Valutazione per Tipo Lavoro**: Analisi specifica per diverse tipologie di lavoro

## 📋 Prerequisiti

- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver (installato automaticamente da webdriver-manager)

## 🚀 Installazione

1. **Clona il repository**
```bash
cd /home/user/app33-meteo
```

2. **Crea ambiente virtuale** (consigliato)
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate  # Windows
```

3. **Installa dipendenze**
```bash
pip install -r requirements.txt
```

4. **Configura le stazioni**

Edita il file `data/stazioni.csv` con le tue stazioni meteo:

```csv
id,nome,provincia,comune,quota,lat,lon
GE001,Genova Centro,GE,Genova,50,44.4056,8.9463
```

**IMPORTANTE**: Dovrai ottenere gli ID reali delle stazioni dal sito della Regione Liguria.

## 📖 Utilizzo

### Analisi Singolo Giorno

```bash
# Analizza una stazione per una data specifica
python main.py --date 2024-01-15 --station GE001 --station-name "Genova Centro"

# Analizza tutte le stazioni
python main.py --date 2024-01-15 --all-stations
```

### Analisi Intervallo Date

```bash
# Analizza un periodo
python main.py --date-range 2024-01-01 2024-01-31 --station GE001 --station-name "Genova Centro"
```

### Analisi da File Esistente

```bash
# Salta il download e analizza un file già scaricato
python main.py --date 2024-01-15 --station GE001 --skip-download --data-file data/output/meteo_GE001_20240115.csv
```

### Opzioni Aggiuntive

```bash
# Mostra il browser durante lo scraping (utile per debug)
python main.py --date 2024-01-15 --station GE001 --no-headless

# Valuta idoneità per specifico tipo di lavoro
python main.py --date 2024-01-15 --station GE001 --work-type OPERE_IN_QUOTA
```

## 🔧 Configurazione

### Personalizzazione Soglie Sicurezza

Modifica `config.py` per personalizzare le soglie di sicurezza:

```python
SAFETY_THRESHOLDS = {
    "precipitazione_max": 5.0,  # mm/h
    "vento_max": 11.0,  # m/s
    "temperatura_min": -5.0,  # °C
    "temperatura_max": 35.0,  # °C
    # ...
}
```

### Tipi di Lavoro

Tipi di lavoro supportati (configurabili in `config.py`):

- `SCAVI`: Scavi e sbancamenti
- `OPERE_IN_QUOTA`: Lavori oltre 2m di altezza
- `GETTO_CLS`: Getti di calcestruzzo
- `FACCIATE`: Lavori su facciate
- `COPERTURE`: Lavori su tetti e coperture
- `INTERNI`: Lavori interni
- `MOVIMENTI_TERRA`: Movimentazione terra
- `GRU_SOLLEVAMENTI`: Operazioni con gru e autogrù

## 📊 Categorie di Idoneità

Il sistema classifica le condizioni in 6 categorie:

| Categoria | Score | Descrizione |
|-----------|-------|-------------|
| **OTTIMO** | 80-100 | Condizioni ottime per lavorare |
| **BUONO** | 65-79 | Condizioni buone, nessuna restrizione |
| **ACCETTABILE** | 50-64 | Condizioni accettabili, attenzione a specifiche attività |
| **LIMITATO** | 35-49 | Limitazioni per lavori in quota o esterni |
| **SCONSIGLIATO** | 20-34 | Lavori esterni sconsigliati |
| **VIETATO** | 0-19 | Lavori esterni vietati per sicurezza |

## 🎯 Criteri di Valutazione

### Parametri Meteorologici

1. **Precipitazioni** (peso 30%)
   - ⚠️ CRITICO: > 5 mm/h
   - ⚠️ Attenzione: 2-5 mm/h
   - Cumulo 24h: > 30 mm (terreno saturo)

2. **Vento** (peso 25%)
   - ⚠️ CRITICO: > 11 m/s (~40 km/h)
   - ⚠️ Attenzione: 8-11 m/s
   - Limita lavori in quota e uso gru

3. **Temperatura** (peso 20%)
   - ⚠️ Freddo: < -5°C (gelo malte)
   - ⚠️ Caldo: > 35°C (stress termico)

4. **Umidità** (peso 10%)
   - Range ottimale: 20-95%

5. **Visibilità** (peso 15%)
   - ⚠️ CRITICO: < 200m (nebbia)

## 📁 Struttura Progetto

```
app33-meteo/
├── config.py              # Configurazione generale
├── scraper.py            # Scraper dati meteo
├── worksite_safety.py    # Algoritmo sicurezza cantiere
├── main.py               # Script principale
├── requirements.txt      # Dipendenze Python
├── README.md             # Documentazione
├── data/
│   ├── stazioni.csv      # Elenco stazioni meteo
│   └── output/           # Dati scaricati
├── reports/              # Report generati
└── logs/                 # Log applicazione
```

## 🛠️ Personalizzazione Scraper

**IMPORTANTE**: Il file `scraper.py` contiene un template che **deve essere adattato** al sito reale della Regione Liguria.

Dovrai:

1. Ispezionare la pagina web con gli strumenti sviluppatore del browser
2. Identificare gli ID/nomi reali dei campi del form:
   - Select stazione meteo
   - Input data
   - Select ora inizio/fine
   - Checkbox fenomeni
   - Select formato output
   - Button download

3. Aggiornare i selettori in `scraper.py`:

```python
# Esempio da adattare
station_select = Select(
    self.driver.find_element(By.ID, "ID_REALE_CAMPO_STAZIONE")
)
```

### Come Trovare i Selettori

1. Apri la pagina in Chrome
2. Premi F12 (DevTools)
3. Click su "Inspect Element"
4. Identifica gli elementi del form
5. Cerca attributi `id`, `name`, o `class`
6. Aggiorna `scraper.py` con i valori reali

## 📝 Esempio Output

```
======================================================================
REPORT SICUREZZA CANTIERE
Data: 15/01/2024
Stazione: Genova Centro
======================================================================

VALUTAZIONE COMPLESSIVA: 72.5/100
Categoria: BUONO
Descrizione: Condizioni buone, nessuna restrizione

✓ LAVORI IN CANTIERE: CONSENTITI

DETTAGLIO PARAMETRI:
----------------------------------------------------------------------
  precipitazione      :  85.0/100
  vento              :  70.0/100
  temperatura        :  65.0/100
  umidita            :  80.0/100
  visibilita         : 100.0/100

AVVISI E RACCOMANDAZIONI:
----------------------------------------------------------------------
  • Vento moderato: 6.2 m/s. Attenzione a ponteggi e materiali leggeri
  • Temperatura bassa 2.5°C. Attenzione getti e presa malte

IDONEITÀ PER TIPO DI LAVORO:
----------------------------------------------------------------------
  ✓ SCAVI: Condizioni buone, procedere normalmente
  ✓ OPERE_IN_QUOTA: Condizioni accettabili, aumentare supervisione
  ✓ GETTO_CLS: Condizioni accettabili, usare additivi antigelo
  ...
```

## 🔍 Debug

Per debug dello scraper, esegui in modalità visibile:

```bash
# Rimuovi --headless per vedere il browser
python scraper.py
```

Oppure modifica direttamente in `scraper.py`:

```python
scraper = LiguriaMeteoScraper(headless=False)
```

## ⚖️ Note Legali e Conformità

### Normative di Riferimento

L'algoritmo di sicurezza si basa su:

- **D.Lgs. 81/2008** (Testo Unico Sicurezza Lavoro)
- **Circolare Min. Lavoro 13/08/1998 n. 102** (Lavori in quota)
- **UNI EN 12811** (Ponteggi)
- **NTC 2018** (Norme Tecniche Costruzioni)
- Best practices ingegneristiche

### Responsabilità

⚠️ **IMPORTANTE**: Questo sistema è un **supporto decisionale** e NON sostituisce:

- La valutazione del Direttore dei Lavori
- La valutazione del Coordinatore per la Sicurezza
- Le disposizioni del Piano di Sicurezza e Coordinamento (PSC)
- Il giudizio professionale degli ingegneri e tecnici responsabili

La responsabilità finale sulla sicurezza del cantiere rimane del personale qualificato in loco.

### Uso dei Dati

Verifica i termini di utilizzo del portale Regione Liguria per l'uso dei dati meteo.

## 🤝 Contributi

Per miglioramenti o segnalazione bug, contatta il maintainer del progetto.

## 📧 Supporto

Per assistenza:
- Controlla i log in `logs/`
- Verifica la configurazione in `config.py`
- Testa lo scraper manualmente con `headless=False`

## 📜 Licenza

Uso interno - Verifica licenza con amministratore progetto.

---

**Sviluppato per supportare ingegneri e direttori lavori nella gestione sicura dei cantieri** 🏗️
