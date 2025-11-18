# 🚀 Guida Rapida - Sistema Meteo Cantiere

## Installazione Veloce

```bash
# 1. Installa dipendenze
pip install -r requirements.txt

# 2. Testa il sistema con dati di esempio
python test_analyzer.py
```

## 🎯 Prossimi Passi

### 1. Configura le Tue Stazioni Meteo

Edita `data/stazioni.csv` con i dati reali delle stazioni che vuoi monitorare.

**Come trovare gli ID delle stazioni:**
1. Vai su https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo.asp
2. Apri gli strumenti sviluppatore (F12)
3. Ispeziona il menu a tendina delle stazioni
4. Trova i valori degli `<option>` (es: `<option value="GE001">Genova Centro</option>`)
5. Aggiungili al CSV

### 2. Adatta lo Scraper alla Pagina Reale

Il file `scraper.py` è un **TEMPLATE** che devi personalizzare:

**Passi da seguire:**

1. Apri la pagina web in Chrome
2. Apri DevTools (F12) → tab "Elements"
3. Ispeziona ogni campo del form e annota:
   - ID o NAME del select stazione
   - ID o NAME del campo data
   - ID o NAME dei select ora inizio/fine
   - ID o NAME/VALUE dei checkbox fenomeni
   - ID o NAME del select formato
   - ID o VALUE del bottone scarica

4. Aggiorna `scraper.py` linee 140-250 circa con i valori reali

**Esempio:**
```python
# PRIMA (template)
station_select = Select(
    self.driver.find_element(By.ID, "stazione")
)

# DOPO (con valore reale trovato)
station_select = Select(
    self.driver.find_element(By.NAME, "cmbStazioni")  # valore reale
)
```

### 3. Test dello Scraper

```bash
# Test in modalità visibile (per vedere cosa fa)
python -c "from scraper import LiguriaMeteoScraper; s = LiguriaMeteoScraper(headless=False)"
```

Osserva il browser aprirsi e individua eventuali errori.

### 4. Personalizza i Criteri di Sicurezza

Modifica `config.py` secondo le tue esigenze:

```python
SAFETY_THRESHOLDS = {
    "precipitazione_max": 5.0,     # Modifica in base alla tua zona
    "vento_max": 11.0,             # Modifica in base ai tuoi lavori
    "temperatura_min": -5.0,       # ...
    # etc.
}
```

## 📝 Esempi di Utilizzo

### Test con Dati di Esempio (SENZA SCRAPING)

```bash
# Testa l'algoritmo di sicurezza
python test_analyzer.py

# Analizza il file di esempio
python main.py --date 2024-01-15 --station TEST --station-name "Stazione Test" \
    --skip-download --data-file data/esempio_dati_meteo.csv
```

### Uso Reale (CON SCRAPING)

```bash
# Singolo giorno, singola stazione
python main.py --date 2024-01-15 --station GE001 --station-name "Genova Centro"

# Ultimi 7 giorni
python main.py --date-range 2024-01-08 2024-01-15 --station GE001 --station-name "Genova Centro"

# Tutte le stazioni di oggi
python main.py --date 2024-01-15 --all-stations
```

## 🔧 Risoluzione Problemi

### Errore: "No module named 'selenium'"
```bash
pip install -r requirements.txt
```

### Errore: "ChromeDriver not found"
Il sistema usa `webdriver-manager` che scarica automaticamente ChromeDriver.
Assicurati di avere Chrome/Chromium installato.

### Lo scraper non trova gli elementi
1. Verifica che gli ID nel `scraper.py` corrispondano alla pagina reale
2. Esegui in modalità visibile: `headless=False`
3. Controlla se la pagina ha CAPTCHA o protezioni anti-bot

### Il sito blocca le richieste (403/Access Denied)
- Il sito potrebbe avere protezioni anti-scraping
- Potrebbe richiedere cookies o sessioni
- Potrebbe bloccare user-agent automatici
- Valuta di contattare Regione Liguria per API ufficiali

## 📊 Interpretazione Risultati

### Score di Sicurezza
- **80-100**: OTTIMO - Lavora tranquillo
- **65-79**: BUONO - Tutto ok
- **50-64**: ACCETTABILE - Fai attenzione
- **35-49**: LIMITATO - Valuta bene
- **20-34**: SCONSIGLIATO - Evita lavori esterni
- **0-19**: VIETATO - Non lavorare

### Parametri Critici per Tipo Lavoro

**OPERE IN QUOTA**: Vento, Precipitazioni, Visibilità
- Vento > 11 m/s → STOP lavori in quota
- Pioggia → STOP lavori in quota

**GETTO CLS**: Precipitazioni, Temperatura
- Pioggia → STOP getti
- Temp < 0°C → Usare additivi antigelo o STOP

**SCAVI**: Precipitazioni, Cumulo 24h
- Pioggia intensa → STOP scavi
- Terreno saturo → STOP scavi

**GRU E SOLLEVAMENTI**: Vento
- Vento > 11 m/s → STOP uso gru

## 💡 Consigli per Direttore Lavori

1. **Controllo Giornaliero**: Esegui l'analisi ogni mattina prima dell'inizio lavori
2. **Pianificazione Settimanale**: Usa `--date-range` per pianificare la settimana
3. **Decisioni Integrate**: Usa questo tool come supporto, non come unica fonte decisionale
4. **Documenta**: Salva i report in `reports/` per documentare le decisioni
5. **Personalizza**: Adatta le soglie al tuo cantiere specifico

## 📞 Supporto

Per problemi o domande:
1. Controlla i log in `logs/`
2. Esegui `test_analyzer.py` per verificare il sistema
3. Controlla la configurazione in `config.py`

---

**Buon lavoro e cantieri sicuri!** 🏗️⛑️
