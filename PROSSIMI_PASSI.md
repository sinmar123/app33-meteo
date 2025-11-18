# ✅ PROSSIMI PASSI - Checklist Operativa

**Usa questa checklist per riprendere il lavoro**

---

## 🎯 OBIETTIVO IMMEDIATO
Rendere il sistema operativo per analisi meteo giornaliere

---

## 📋 CHECKLIST ATTIVITÀ

### ⭐ PRIORITÀ 1 - Test Sistema (5 minuti)

- [ ] **Clonare repository sul PC locale**
  ```bash
  cd Desktop
  git clone https://github.com/sinmar123/app33-meteo.git
  cd app33-meteo
  ```

- [ ] **Installare dipendenze Python**
  ```bash
  pip install pandas numpy
  ```

- [ ] **Testare l'algoritmo**
  ```bash
  python test_analyzer.py
  ```
  ✅ Se funziona → Sistema operativo per analisi base!

---

### ⭐ PRIORITÀ 2 - Verificare ID Stazioni (15 minuti)

**OPZIONALE** ma consigliato per evitare errori futuri

- [ ] Aprire: https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo.asp

- [ ] Aprire DevTools (F12) → Console

- [ ] Digitare: `allow pasting`

- [ ] Eseguire script:
  ```javascript
  let select = document.querySelector('select');
  select.querySelectorAll('option').forEach(opt => {
      console.log(opt.value + ',' + opt.text);
  });
  ```

- [ ] Copiare output in un file temporaneo

- [ ] Confrontare con `data/stazioni.csv`

- [ ] Se ID diversi → Aggiornare CSV con ID reali

**Nota**: Se gli ID sono troppo diversi dai nostri (GE001, GE002...),
chiedi aiuto per creare script di aggiornamento automatico.

---

### ⭐ PRIORITÀ 3 - Configurare Scraper (30-60 minuti)

**NECESSARIO** per download automatico dati dal sito

#### Passo A: Ispezionare Form Web

- [ ] Aprire: https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo.asp

- [ ] DevTools (F12) → Elements

- [ ] Ispezionare campo SELECT stazioni:
  ```
  Click destro sul menu stazioni → Inspect
  Annotare: id="___" oppure name="___"
  ```
  Valore trovato: `_____________________`

- [ ] Ispezionare campo DATA:
  ```
  Click destro sul campo data → Inspect
  Annotare: id="___" oppure name="___"
  Annotare: formato data richiesto (gg/mm/aaaa o altro)
  ```
  Valore trovato: `_____________________`

- [ ] Ispezionare SELECT ora inizio:
  ```
  Annotare: id="___" oppure name="___"
  ```
  Valore trovato: `_____________________`

- [ ] Ispezionare SELECT ora fine:
  ```
  Annotare: id="___" oppure name="___"
  ```
  Valore trovato: `_____________________`

- [ ] Ispezionare CHECKBOX/SELECT fenomeni:
  ```
  Annotare come sono chiamati i fenomeni
  (Temperatura, Precipitazione, Vento, etc.)
  ```
  Trovati: `_____________________`

- [ ] Ispezionare SELECT formato:
  ```
  Annotare: id="___" oppure name="___"
  Annotare valori disponibili (CSV, XLS, TXT)
  ```
  Valore trovato: `_____________________`

- [ ] Ispezionare BOTTONE download/scarica:
  ```
  Annotare: id="___" oppure value="___" oppure testo bottone
  ```
  Valore trovato: `_____________________`

#### Passo B: Aggiornare scraper.py

- [ ] Aprire `scraper.py` in un editor di testo

- [ ] Cercare riga ~140: `station_select = Select(`

- [ ] Sostituire `By.ID, "stazione"` con il valore reale trovato

- [ ] Cercare riga ~150: `date_input = self.driver.find_element(`

- [ ] Sostituire con il valore reale trovato

- [ ] Ripetere per tutti i campi annotati sopra

- [ ] Salvare il file

#### Passo C: Testare Scraper

- [ ] Eseguire test con browser visibile:
  ```bash
  python -c "from scraper import LiguriaMeteoScraper;
  s = LiguriaMeteoScraper(headless=False);
  s.get_station_data('GE036', 'GENOVA', datetime(2024,11,10))"
  ```

- [ ] Osservare se il browser:
  - ✅ Apre la pagina
  - ✅ Seleziona la stazione
  - ✅ Inserisce la data
  - ✅ Scarica il file

- [ ] Se ci sono errori → Annotarli e chiedere aiuto

---

### ⭐ PRIORITÀ 4 - Personalizzare Soglie (10 minuti)

**OPZIONALE** - Adatta alle esigenze del tuo cantiere specifico

- [ ] Aprire `config.py`

- [ ] Sezione `SAFETY_THRESHOLDS`:
  - [ ] Verificare limite precipitazione (attuale: 5 mm/h)
  - [ ] Verificare limite vento (attuale: 11 m/s = 40 km/h)
  - [ ] Verificare limite temperatura min (attuale: -5°C)
  - [ ] Verificare limite temperatura max (attuale: 35°C)

- [ ] Sezione `SAFETY_WEIGHTS`:
  - [ ] Verificare pesi parametri (somma deve essere 1.0)
  - [ ] Modificare se necessario per il tuo cantiere

- [ ] Salvare modifiche

- [ ] Testare di nuovo:
  ```bash
  python test_analyzer.py
  ```

---

## 🎓 QUANDO TUTTO È PRONTO

### Uso Quotidiano - Opzione A (Con Scraper Configurato)

```bash
# Analizza oggi
python main.py \
  --date $(date +%Y-%m-%d) \
  --station GE036 \
  --station-name "GENOVA - CENTRO FUNZIONALE"

# Analizza ieri
python main.py \
  --date $(date -d "yesterday" +%Y-%m-%d) \
  --station GE036 \
  --station-name "GENOVA - CENTRO FUNZIONALE"

# Analizza ultima settimana
python main.py \
  --date-range $(date -d "7 days ago" +%Y-%m-%d) $(date +%Y-%m-%d) \
  --station GE036 \
  --station-name "GENOVA - CENTRO FUNZIONALE"
```

### Uso Quotidiano - Opzione B (Download Manuale)

```bash
# 1. Scarica manualmente CSV dal sito
# 2. Salva come: dati_meteo_20241110.csv
# 3. Esegui:

python main.py \
  --date 2024-11-10 \
  --station GE036 \
  --station-name "GENOVA - CENTRO FUNZIONALE" \
  --skip-download \
  --data-file dati_meteo_20241110.csv
```

---

## 📊 OUTPUT ATTESO

Quando tutto funziona, dovresti vedere:

```
======================================================================
REPORT SICUREZZA CANTIERE
Data: 10/11/2024
Stazione: GENOVA - CENTRO FUNZIONALE
======================================================================

VALUTAZIONE COMPLESSIVA: 72.5/100
Categoria: BUONO

✓ LAVORI IN CANTIERE: CONSENTITI

DETTAGLIO PARAMETRI:
  Precipitazione  : 85.0/100
  Vento           : 70.0/100
  Temperatura     : 65.0/100
  Umidità         : 80.0/100
  Visibilità      : 100.0/100

AVVISI E RACCOMANDAZIONI:
  • Vento moderato: 6.2 m/s
  • Temperatura bassa: 3.5°C - Attenzione getti

IDONEITÀ PER TIPO DI LAVORO:
  ✓ SCAVI: Condizioni buone
  ✓ OPERE IN QUOTA: Condizioni accettabili - Supervisione
  ✓ GETTO CLS: Attenzione temperatura - Usare additivi
  ✓ FACCIATE: Condizioni buone
  ✓ COPERTURE: Condizioni accettabili
  ✓ INTERNI: Condizioni ottime
  ✓ MOVIMENTI TERRA: Condizioni buone
  ✓ GRU/SOLLEVAMENTI: Condizioni buone
======================================================================
```

---

## ❓ PROBLEMI COMUNI

### "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas numpy
```

### "git: command not found"
Scarica come ZIP da GitHub o installa Git

### Scraper non funziona (403 Forbidden)
Il sito ha protezioni anti-bot. Opzioni:
1. Download manuale + `--skip-download`
2. Configurare meglio lo scraper con delays/cookies
3. Contattare Regione Liguria per API ufficiali

### Non capisco come configurare lo scraper
Chiedi aiuto mostrando:
1. Screenshot della pagina web
2. HTML del form (DevTools → Elements → Copy outer HTML)

---

## 📁 FILE DA CONSULTARE

1. **Questo file** (`PROSSIMI_PASSI.md`) - Checklist operativa
2. `STATO_PROGETTO.md` - Panoramica generale
3. `GUIDA_RAPIDA.md` - Guida pratica dettagliata
4. `README.md` - Documentazione tecnica completa

---

## ✅ QUANDO HAI FINITO

- [ ] Sistema testato in locale
- [ ] ID stazioni verificati (opzionale)
- [ ] Scraper configurato OPPURE uso download manuale
- [ ] Soglie personalizzate (opzionale)
- [ ] Primo report generato con successo

**SISTEMA OPERATIVO!** 🎉

---

**Prossima sessione**: Automazione quotidiana con cron/scheduler
