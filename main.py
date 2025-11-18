#!/usr/bin/env python3
"""
Script principale per analisi meteo e valutazione sicurezza cantiere
Regione Liguria

Uso:
    python main.py --date 2024-01-15 --station GE001
    python main.py --date 2024-01-15 --all-stations
    python main.py --date-range 2024-01-01 2024-01-31 --station GE001
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
import logging

import pandas as pd

from scraper import LiguriaMeteoScraper
from worksite_safety import WorksiteSafetyAnalyzer, load_weather_data
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{config.LOGS_DIR}/meteo_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_directories():
    """Crea le directory necessarie se non esistono"""
    Path(config.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(config.LOGS_DIR).mkdir(parents=True, exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)


def parse_date(date_str: str) -> datetime:
    """Parse data da stringa"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            raise ValueError(
                f"Formato data non valido: {date_str}. "
                "Usare YYYY-MM-DD o DD/MM/YYYY"
            )


def analyze_single_day(
    station_id: str,
    station_name: str,
    date: datetime,
    scraper: LiguriaMeteoScraper,
    analyzer: WorksiteSafetyAnalyzer,
    skip_download: bool = False,
    data_file: str = None
):
    """
    Analizza un singolo giorno per una stazione

    Args:
        station_id: ID stazione
        station_name: Nome stazione
        date: Data da analizzare
        scraper: Istanza scraper
        analyzer: Istanza analyzer
        skip_download: Se True, salta download (usa file esistente)
        data_file: Percorso file dati (se skip_download=True)
    """
    logger.info(f"\n{'='*70}")
    logger.info(f"Analisi per {station_name} del {date.strftime('%d/%m/%Y')}")
    logger.info(f"{'='*70}\n")

    # Download dati
    if not skip_download:
        logger.info("Download dati meteo...")
        data_file = scraper.get_station_data(
            station_id=station_id,
            station_name=station_name,
            date=date
        )

        if not data_file:
            logger.error("Impossibile scaricare i dati")
            return None

    if not data_file or not Path(data_file).exists():
        logger.error(f"File dati non trovato: {data_file}")
        return None

    # Carica e analizza dati
    logger.info("Analisi dati meteo...")
    try:
        weather_data = load_weather_data(data_file)

        # Genera analisi
        result = analyzer.calculate_overall_score(weather_data)

        # Genera report
        report = analyzer.generate_daily_report(
            weather_data,
            date,
            station_name
        )

        # Stampa report
        print(report)

        # Salva report su file
        report_dir = Path("reports")
        report_file = report_dir / f"report_{station_id}_{date.strftime('%Y%m%d')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"Report salvato in: {report_file}")

        return result

    except Exception as e:
        logger.error(f"Errore durante l'analisi: {e}")
        import traceback
        traceback.print_exc()
        return None


def analyze_date_range(
    station_id: str,
    station_name: str,
    start_date: datetime,
    end_date: datetime,
    scraper: LiguriaMeteoScraper,
    analyzer: WorksiteSafetyAnalyzer
):
    """
    Analizza un intervallo di date

    Args:
        station_id: ID stazione
        station_name: Nome stazione
        start_date: Data inizio
        end_date: Data fine
        scraper: Istanza scraper
        analyzer: Istanza analyzer
    """
    results = []
    current_date = start_date

    while current_date <= end_date:
        result = analyze_single_day(
            station_id,
            station_name,
            current_date,
            scraper,
            analyzer
        )

        if result:
            results.append({
                'date': current_date,
                'score': result['overall_score'],
                'category': result['category'],
                'can_work': result['can_work']
            })

        current_date += timedelta(days=1)

    # Genera report riassuntivo
    if results:
        print("\n" + "="*70)
        print("RIEPILOGO PERIODO")
        print("="*70)

        df_results = pd.DataFrame(results)

        workable_days = df_results['can_work'].sum()
        total_days = len(df_results)
        avg_score = df_results['score'].mean()

        print(f"\nPeriodo: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}")
        print(f"Giorni analizzati: {total_days}")
        print(f"Giorni lavorabili: {workable_days} ({workable_days/total_days*100:.1f}%)")
        print(f"Score medio: {avg_score:.1f}/100")
        print("\nDettaglio per categoria:")

        category_counts = df_results['category'].value_counts()
        for category, count in category_counts.items():
            print(f"  {category}: {count} giorni ({count/total_days*100:.1f}%)")

        # Salva riepilogo
        summary_file = Path("reports") / f"summary_{station_id}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
        df_results.to_csv(summary_file, index=False)
        print(f"\nRiepilogo salvato in: {summary_file}")


def main():
    """Funzione principale"""
    parser = argparse.ArgumentParser(
        description="Analisi meteo e valutazione sicurezza cantiere - Regione Liguria"
    )

    parser.add_argument(
        '--date',
        type=str,
        help='Data da analizzare (YYYY-MM-DD o DD/MM/YYYY)'
    )

    parser.add_argument(
        '--date-range',
        nargs=2,
        metavar=('START', 'END'),
        help='Intervallo date da analizzare (YYYY-MM-DD)'
    )

    parser.add_argument(
        '--station',
        type=str,
        help='ID stazione meteo'
    )

    parser.add_argument(
        '--station-name',
        type=str,
        default="Stazione",
        help='Nome stazione (per report)'
    )

    parser.add_argument(
        '--all-stations',
        action='store_true',
        help='Analizza tutte le stazioni dal CSV'
    )

    parser.add_argument(
        '--skip-download',
        action='store_true',
        help='Salta download, usa file esistente'
    )

    parser.add_argument(
        '--data-file',
        type=str,
        help='Percorso file dati (con --skip-download)'
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Esegui browser in modalità headless (default: True)'
    )

    parser.add_argument(
        '--work-type',
        type=str,
        choices=list(config.WORK_TYPES.keys()),
        help='Valuta idoneità per specifico tipo di lavoro'
    )

    args = parser.parse_args()

    # Validazione argomenti
    if not args.date and not args.date_range:
        parser.error("Specificare --date o --date-range")

    if not args.station and not args.all_stations and not args.skip_download:
        parser.error("Specificare --station o --all-stations")

    if args.skip_download and not args.data_file:
        parser.error("Con --skip-download specificare --data-file")

    # Setup
    setup_directories()

    # Inizializza componenti
    scraper = LiguriaMeteoScraper(headless=args.headless)
    analyzer = WorksiteSafetyAnalyzer()

    try:
        # Analisi singola data
        if args.date:
            date = parse_date(args.date)

            if args.skip_download:
                # Analisi da file
                analyze_single_day(
                    args.station or "UNKNOWN",
                    args.station_name,
                    date,
                    scraper,
                    analyzer,
                    skip_download=True,
                    data_file=args.data_file
                )
            elif args.all_stations:
                # Tutte le stazioni
                stations_df = scraper.load_stations()
                for _, station in stations_df.iterrows():
                    analyze_single_day(
                        station['id'],
                        station['nome'],
                        date,
                        scraper,
                        analyzer
                    )
            else:
                # Singola stazione
                analyze_single_day(
                    args.station,
                    args.station_name,
                    date,
                    scraper,
                    analyzer
                )

        # Analisi intervallo date
        elif args.date_range:
            start_date = parse_date(args.date_range[0])
            end_date = parse_date(args.date_range[1])

            if end_date < start_date:
                logger.error("Data fine precedente a data inizio")
                sys.exit(1)

            analyze_date_range(
                args.station,
                args.station_name,
                start_date,
                end_date,
                scraper,
                analyzer
            )

    except KeyboardInterrupt:
        logger.info("\nInterrotto dall'utente")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Errore: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        scraper._close_driver()


if __name__ == "__main__":
    main()
