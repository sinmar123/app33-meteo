#!/usr/bin/env python3
"""
Demo del sistema di analisi meteo cantiere

Mostra le funzionalità principali senza bisogno di installare dipendenze
"""

import sys
import csv
from pathlib import Path

def show_stations():
    """Mostra l'elenco delle stazioni disponibili"""

    print("\n" + "="*70)
    print("STAZIONI METEO DISPONIBILI - REGIONE LIGURIA")
    print("="*70)

    stations_file = Path("data/stazioni.csv")

    if not stations_file.exists():
        print("❌ File stazioni non trovato!")
        return

    with open(stations_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        stations = list(reader)

    print(f"\nTotale: {len(stations)} stazioni\n")

    # Raggruppa per provincia
    by_province = {}
    for station in stations:
        prov = station['provincia']
        if prov not in by_province:
            by_province[prov] = []
        by_province[prov].append(station)

    for prov in sorted(by_province.keys()):
        stations_list = by_province[prov]
        print(f"\n📍 {prov} - {len(stations_list)} stazioni:")
        print("-" * 70)

        # Mostra prime 5 e ultime 2
        for station in stations_list[:5]:
            print(f"  {station['id']:8s} {station['nome']}")

        if len(stations_list) > 7:
            print(f"  ... (altre {len(stations_list) - 7} stazioni) ...")

            for station in stations_list[-2:]:
                print(f"  {station['id']:8s} {station['nome']}")


def show_usage_examples():
    """Mostra esempi di utilizzo"""

    print("\n" + "="*70)
    print("ESEMPI DI UTILIZZO")
    print("="*70)

    examples = [
        {
            "title": "1. Test dell'analizzatore (SENZA SCRAPING)",
            "desc": "Testa il sistema con dati di esempio",
            "cmd": "python test_analyzer.py"
        },
        {
            "title": "2. Analisi file esistente",
            "desc": "Analizza un file meteo già scaricato",
            "cmd": """python main.py \\
  --date 2024-01-15 \\
  --station GE036 \\
  --station-name "GENOVA - CENTRO FUNZIONALE" \\
  --skip-download \\
  --data-file data/esempio_dati_meteo.csv"""
        },
        {
            "title": "3. Download e analisi (RICHIEDE CONFIGURAZIONE SCRAPER)",
            "desc": "Scarica dati e analizza - dopo aver configurato lo scraper",
            "cmd": """python main.py \\
  --date 2024-01-15 \\
  --station GE036 \\
  --station-name "GENOVA - CENTRO FUNZIONALE\""""
        },
        {
            "title": "4. Analisi periodo",
            "desc": "Analizza più giorni con statistiche aggregate",
            "cmd": """python main.py \\
  --date-range 2024-01-01 2024-01-07 \\
  --station GE036 \\
  --station-name "GENOVA - CENTRO FUNZIONALE\""""
        },
        {
            "title": "5. Tutte le stazioni",
            "desc": "Analizza tutte le stazioni per una data",
            "cmd": """python main.py \\
  --date 2024-01-15 \\
  --all-stations"""
        }
    ]

    for example in examples:
        print(f"\n{example['title']}")
        print("-" * 70)
        print(f"Descrizione: {example['desc']}")
        print(f"\nComando:")
        print(f"  {example['cmd']}")
        print()


def show_config_info():
    """Mostra info su configurazione"""

    print("\n" + "="*70)
    print("CONFIGURAZIONE SISTEMA")
    print("="*70)

    print("""
⚠️  IMPORTANTE: Prima di usare lo scraper automatico devi:

1. Installare le dipendenze:
   pip install -r requirements.txt

2. Verificare gli ID delle stazioni:
   Gli ID generati (GE001, GE002, etc.) sono PROVVISORI.
   Devi verificare che corrispondano agli ID reali del sito web:

   a) Apri: https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo.asp
   b) Apri DevTools (F12) → Console
   c) Esegui:

      let select = document.querySelector('select');
      select.querySelectorAll('option').forEach(opt => {
          console.log(opt.value + ' → ' + opt.text);
      });

   d) Confronta gli output con data/stazioni.csv
   e) Se diversi, aggiorna il CSV con gli ID reali

3. Personalizzare lo scraper (scraper.py):
   Ispeziona la pagina web e aggiorna i selettori HTML reali:
   - ID campo select stazioni
   - ID campo data
   - ID campi ora inizio/fine
   - etc.

   Vedi GUIDA_RAPIDA.md per istruzioni dettagliate.

4. Personalizzare le soglie di sicurezza (config.py):
   Adatta i limiti meteo al tuo cantiere specifico.
    """)


def show_safety_criteria():
    """Mostra criteri di sicurezza"""

    print("\n" + "="*70)
    print("CRITERI DI SICUREZZA CANTIERE")
    print("="*70)

    print("""
Il sistema valuta 5 parametri meteorologici:

1. PRECIPITAZIONI (peso 30%)
   ⚠️  CRITICO: > 5 mm/h → Lavori esterni VIETATI
   ⚠️  Attenzione: 2-5 mm/h → Limitare lavori in quota
   ⚠️  Cumulo 24h: > 30 mm → Terreno saturo, evitare scavi

2. VENTO (peso 25%)
   ⚠️  CRITICO: > 11 m/s (~40 km/h) → Lavori in quota e gru VIETATI
   ⚠️  Attenzione: 8-11 m/s → Limitare lavori in quota

3. TEMPERATURA (peso 20%)
   ⚠️  Freddo: < -5°C → Gelo malte, STOP getti CLS
   ⚠️  Caldo: > 35°C → Stress termico, turni ridotti
   ⚠️  Attenzione: 0-5°C → Usare additivi antigelo per getti

4. UMIDITÀ (peso 10%)
   Range ottimale: 20-95%

5. VISIBILITÀ (peso 15%)
   ⚠️  CRITICO: < 200m → Nebbia, limitare movimentazione mezzi

CATEGORIE DI IDONEITÀ:
  • OTTIMO (80-100): Lavora tranquillo
  • BUONO (65-79): Nessuna restrizione
  • ACCETTABILE (50-64): Attenzione a specifiche attività
  • LIMITATO (35-49): Valutare sospensione lavori esterni
  • SCONSIGLIATO (20-34): Evitare lavori esterni
  • VIETATO (0-19): NON LAVORARE

TIPI DI LAVORO VALUTATI:
  • SCAVI: Critici precipitazione e vento
  • OPERE IN QUOTA: Critici vento, precipitazione, visibilità
  • GETTO CLS: Critici precipitazione e temperatura
  • FACCIATE: Critici precipitazione, vento, temperatura
  • COPERTURE: Critici vento e precipitazione
  • GRU/SOLLEVAMENTI: Critico vento
  • INTERNI: Critici temperatura e umidità
  • MOVIMENTI TERRA: Critica precipitazione
    """)


def main():
    """Menu principale"""

    print("\n" + "="*70)
    print("🏗️  SISTEMA ANALISI METEO E SICUREZZA CANTIERE")
    print("    Regione Liguria - Demo")
    print("="*70)

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()

        if cmd == "stations":
            show_stations()
        elif cmd == "examples":
            show_usage_examples()
        elif cmd == "config":
            show_config_info()
        elif cmd == "criteria":
            show_safety_criteria()
        else:
            print(f"\n❌ Comando sconosciuto: {cmd}")
            print("\nUsa: python demo.py [stations|examples|config|criteria]")
    else:
        # Mostra tutto
        show_stations()
        show_safety_criteria()
        show_usage_examples()
        show_config_info()

    print("\n" + "="*70)
    print("Per informazioni dettagliate vedi:")
    print("  • README.md - Documentazione completa")
    print("  • GUIDA_RAPIDA.md - Guida pratica in italiano")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
