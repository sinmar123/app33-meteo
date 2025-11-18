#!/usr/bin/env python3
"""
Script di test per l'analizzatore di sicurezza cantiere
Usa dati di esempio senza necessità di scraping
"""

from datetime import datetime
from pathlib import Path

from worksite_safety import WorksiteSafetyAnalyzer, load_weather_data
import config

def test_analyzer():
    """Test dell'analizzatore con dati di esempio"""

    print("="*70)
    print("TEST ANALIZZATORE SICUREZZA CANTIERE")
    print("="*70)
    print()

    # Carica dati di esempio
    example_file = "data/esempio_dati_meteo.csv"

    if not Path(example_file).exists():
        print(f"❌ File di esempio non trovato: {example_file}")
        print("Crea prima il file con dati meteo di esempio")
        return

    print(f"📊 Caricamento dati da: {example_file}")
    weather_data = load_weather_data(example_file)

    print(f"✓ Dati caricati: {len(weather_data)} record orari")
    print(f"✓ Colonne disponibili: {', '.join(weather_data.columns)}")
    print()

    # Crea analizzatore
    analyzer = WorksiteSafetyAnalyzer()

    # Genera report
    print("🔍 Generazione report...")
    print()

    report = analyzer.generate_daily_report(
        weather_data,
        datetime.now(),
        "Stazione Test"
    )

    print(report)

    # Test valutazione per tipo di lavoro
    print("\n" + "="*70)
    print("TEST VALUTAZIONE PER TIPO DI LAVORO")
    print("="*70)
    print()

    for work_type in ["OPERE_IN_QUOTA", "GETTO_CLS", "SCAVI"]:
        print(f"\n🔨 {work_type}:")
        result = analyzer.evaluate_work_type(weather_data, work_type)
        print(f"   Score specifico: {result['specific_score']}/100")
        print(f"   {result['recommendation']}")

    print("\n✓ Test completato con successo!")

if __name__ == "__main__":
    test_analyzer()
