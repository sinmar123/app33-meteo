# 📋 STATO DEL PROGETTO - Sistema Meteo Cantiere

**Data ultimo aggiornamento**: 18 Novembre 2025

---

## ✅ COSA È STATO FATTO

### 1. Sistema Completo Sviluppato
- ✅ **250 stazioni meteo** Liguria caricate (Genova, Imperia, La Spezia, Savona)
- ✅ **Algoritmo di sicurezza cantiere** funzionante e testato
- ✅ **Scraper web** con Selenium (template da configurare)
- ✅ **Script principale** (`main.py`) per analisi complete
- ✅ **Configurazione soglie** personalizzabile (`config.py`)
- ✅ **Documentazione completa** in italiano

### 2. Test Eseguiti
- ✅ Test dell'algoritmo con dati di esempio: **FUNZIONA**
- ✅ Output: Score 83.5/100, categoria OTTIMO
- ✅ Valutazione per 8 tipi di lavoro (scavi, opere in quota, getti, ecc.)

### 3. Repository GitHub
- ✅ Codice pubblicato su: `https://github.com/sinmar123/app33-meteo`
- ✅ Branch: `claude/weather-scraper-worksite-safety-01MDSiDDhdNkbjTu7j3kcahh`
- ✅ Tutto committato e pushato

---

## ⏳ COSA MANCA DA FARE

### 1. PRIORITÀ ALTA - Per Usare il Sistema

#### A) Verificare ID Stazioni (OPZIONALE ma consigliato)
Gli ID attualmente nel CSV (GE001, GE002, etc.) sono **provvisori**.

**Come verificare:**
1. Apri: https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo.asp
2. DevTools (F12) → Console
3. Digita: `allow pasting` (per sicurezza Chrome)
4. Incolla:
```javascript
let select = document.querySelector('select');
select.querySelectorAll('option').forEach(opt => {
    console.log(opt.value + ',' + opt.text);
});
```
5. Confronta output con `data/stazioni.csv`
6. Se diversi, aggiorna il CSV con gli ID reali

#### B) Configurare lo Scraper (NECESSARIO per download automatico)

**File da modificare**: `scraper.py` (linee 140-250 circa)

**Cosa fare:**
1. Apri la pagina meteo Regione Liguria
2. Apri DevTools (F12) → Elements
3. Ispeziona ogni campo del form:
   - Select delle stazioni → trova `id` o `name`
   - Input data → trova `id` o `name`
   - Select ora inizio/fine → trova `id` o `name`
   - Checkbox fenomeni → trova valori
   - Select formato → trova `id` o `name`
   - Bottone scarica → trova selettore

4. Aggiorna `scraper.py` con i valori reali

**Dettagli in**: `GUIDA_RAPIDA.md` sezione "Adatta lo Scraper"

### 2. PRIORITÀ MEDIA - Personalizzazioni

#### A) Personalizzare Soglie Sicurezza
Edita `config.py` per adattare al tuo cantiere:
- Limiti precipitazione
- Limiti vento
- Limiti temperatura
- Pesi dei parametri

#### B) Aggiungere Coordinate GPS
Opzionale: aggiungi lat/lon nel CSV per visualizzazioni su mappa

---

## 🚀 COME RIPRENDERE

### Scenario 1: Usare il Sistema SUBITO (senza scraper)

**Download manuale dati + analisi**

1. Scarica manualmente dal sito Regione Liguria i dati meteo di un giorno
2. Salva il CSV
3. Esegui:
```bash
python main.py \
  --date 2024-11-10 \
  --station GE036 \
  --station-name "GENOVA - CENTRO FUNZIONALE" \
  --skip-download \
  --data-file tuo_file_scaricato.csv
```

### Scenario 2: Configurare Download Automatico

**Prima volta:**
1. Verifica ID stazioni (vedi sopra)
2. Configura scraper (vedi sopra)
3. Testa con:
```bash
python main.py \
  --date 2024-11-10 \
  --station GE036 \
  --station-name "GENOVA - CENTRO FUNZIONALE" \
  --headless=False
```
(così vedi il browser aprirsi)

### Scenario 3: Solo Testare l'Algoritmo

**Test rapido senza dati reali:**
```bash
python test_analyzer.py
```

Oppure con una data specifica:
```bash
python main.py \
  --date 2024-01-15 \
  --station GE036 \
  --station-name "GENOVA - CENTRO FUNZIONALE" \
  --skip-download \
  --data-file data/esempio_dati_meteo.csv
```

---

## 📂 STRUTTURA FILE PRINCIPALI

```
app33-meteo/
├── 📄 STATO_PROGETTO.md          ← QUESTO FILE (leggi sempre da qui!)
├── 📄 PROSSIMI_PASSI.md          ← Checklist operativa
├── 📄 README.md                  ← Documentazione completa
├── 📄 GUIDA_RAPIDA.md            ← Guida pratica italiano
│
├── 🐍 main.py                    ← Script principale
├── 🐍 test_analyzer.py           ← Test rapido
├── 🐍 demo.py                    ← Menu dimostrativo
├── 🐍 scraper.py                 ← Scraper (DA CONFIGURARE)
├── 🐍 worksite_safety.py         ← Algoritmo sicurezza
├── 🐍 config.py                  ← Configurazione soglie
│
└── data/
    ├── stazioni.csv              ← 250 stazioni Liguria
    └── esempio_dati_meteo.csv    ← Dati test
```

---

## 🎯 OBIETTIVO FINALE

**Analizzare automaticamente ogni giorno** se le condizioni meteo permettono di lavorare in cantiere:

```bash
# Esempio uso finale
python main.py --date 2024-11-18 --station GE036 --station-name "GENOVA"
```

**Output desiderato:**
```
======================================================================
REPORT SICUREZZA CANTIERE
Data: 18/11/2024
Stazione: GENOVA - CENTRO FUNZIONALE
======================================================================

VALUTAZIONE COMPLESSIVA: 75.0/100
Categoria: BUONO
✓ LAVORI IN CANTIERE: CONSENTITI

AVVISI:
  • Vento moderato 7.2 m/s - Attenzione ponteggi

IDONEITÀ LAVORI:
  ✓ SCAVI: OK
  ✓ OPERE IN QUOTA: Attenzione vento
  ✓ GETTO CLS: OK
  ...
```

---

## 💡 DOMANDE FREQUENTI

**Q: Posso usare il sistema senza configurare lo scraper?**
A: Sì! Scarica manualmente i dati e usa `--skip-download --data-file`

**Q: Gli ID delle stazioni sono corretti?**
A: Sono provvisori (GE001, GE002...). Verifica con il sito web.

**Q: Posso cambiare le soglie di sicurezza?**
A: Sì! Edita `config.py` sezione `SAFETY_THRESHOLDS`

**Q: Come faccio ad analizzare più giorni?**
A: Usa `--date-range`:
```bash
python main.py --date-range 2024-11-01 2024-11-30 --station GE036
```

---

## 📞 SUPPORTO

**File da consultare:**
1. `STATO_PROGETTO.md` (questo) - Panoramica generale
2. `PROSSIMI_PASSI.md` - Checklist operativa
3. `GUIDA_RAPIDA.md` - Istruzioni dettagliate
4. `README.md` - Documentazione tecnica completa

**Test rapido funzionamento:**
```bash
python demo.py        # Mostra tutto
python demo.py stations   # Mostra stazioni
python demo.py criteria   # Mostra criteri sicurezza
```

---

**Ultima modifica**: 18 Novembre 2025
**Prossima sessione**: Configurare scraper o testare con dati reali
