"""
Scraper per dati meteorologici Regione Liguria
Gestisce l'interfaccia web ASP per il download dei dati
"""

import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import pandas as pd

import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LiguriaMeteoScraper:
    """Scraper per dati meteo Regione Liguria"""

    def __init__(self, headless: bool = True):
        """
        Inizializza lo scraper

        Args:
            headless: Se True, esegue browser in modalità headless
        """
        self.headless = headless
        self.driver = None
        self.wait = None

    def _init_driver(self):
        """Inizializza il webdriver Chrome"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

        # Imposta preferenze download
        prefs = {
            "download.default_directory": str(Path(config.OUTPUT_DIR).absolute()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, config.DEFAULT_WAIT_TIME)

        logger.info("WebDriver inizializzato")

    def _close_driver(self):
        """Chiude il webdriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver chiuso")

    def load_stations(self, csv_path: str = None) -> pd.DataFrame:
        """
        Carica l'elenco delle stazioni da CSV

        Args:
            csv_path: Percorso del file CSV (default: config.STATIONS_CSV)

        Returns:
            DataFrame con le stazioni
        """
        if csv_path is None:
            csv_path = config.STATIONS_CSV

        try:
            stations = pd.read_csv(csv_path)
            logger.info(f"Caricate {len(stations)} stazioni da {csv_path}")
            return stations
        except Exception as e:
            logger.error(f"Errore caricamento stazioni: {e}")
            raise

    def get_station_data(
        self,
        station_id: str,
        station_name: str,
        date: datetime,
        start_hour: int = 0,
        end_hour: int = 23,
        fenomeni: List[str] = None,
        formato: str = "CSV"
    ) -> Optional[str]:
        """
        Scarica i dati per una stazione specifica

        Args:
            station_id: ID della stazione meteo
            station_name: Nome della stazione
            date: Data da scaricare
            start_hour: Ora inizio (0-23)
            end_hour: Ora fine (0-23)
            fenomeni: Lista fenomeni da scaricare (default: tutti)
            formato: Formato output (CSV, XLS, TXT)

        Returns:
            Percorso file scaricato o None se errore
        """
        if fenomeni is None:
            fenomeni = list(config.FENOMENI.keys())

        try:
            if not self.driver:
                self._init_driver()

            logger.info(
                f"Scaricamento dati per {station_name} ({station_id}) "
                f"del {date.strftime('%d/%m/%Y')}"
            )

            # Carica la pagina
            self.driver.get(config.METEO_URL)
            time.sleep(2)

            # NOTA: Qui dovrai mappare i selettori HTML effettivi
            # Questo è un template che dovrai adattare ispezionando la pagina

            # Seleziona la stazione
            try:
                station_select = Select(
                    self.wait.until(
                        EC.presence_of_element_located((By.ID, "stazione"))
                        # O By.NAME, "stazione" se usa name invece di id
                    )
                )
                station_select.select_by_value(station_id)
                logger.info(f"Stazione selezionata: {station_name}")
            except Exception as e:
                logger.error(f"Errore selezione stazione: {e}")
                return None

            # Imposta la data
            try:
                # Esempio: campo data (il formato dipende dalla pagina)
                date_input = self.driver.find_element(By.ID, "data")
                date_input.clear()
                date_input.send_keys(date.strftime("%d/%m/%Y"))
                logger.info(f"Data impostata: {date.strftime('%d/%m/%Y')}")
            except Exception as e:
                logger.error(f"Errore impostazione data: {e}")
                return None

            # Imposta l'intervallo orario
            try:
                hour_start_select = Select(
                    self.driver.find_element(By.ID, "ora_inizio")
                )
                hour_start_select.select_by_value(str(start_hour))

                hour_end_select = Select(
                    self.driver.find_element(By.ID, "ora_fine")
                )
                hour_end_select.select_by_value(str(end_hour))
                logger.info(f"Intervallo orario: {start_hour}:00 - {end_hour}:00")
            except Exception as e:
                logger.error(f"Errore impostazione orario: {e}")
                return None

            # Seleziona i fenomeni
            # (potrebbe essere checkbox, multiselect, etc.)
            try:
                for fenomeno in fenomeni:
                    checkbox = self.driver.find_element(
                        By.XPATH,
                        f"//input[@type='checkbox'][@value='{fenomeno}']"
                    )
                    if not checkbox.is_selected():
                        checkbox.click()
                logger.info(f"Fenomeni selezionati: {', '.join(fenomeni)}")
            except Exception as e:
                logger.warning(f"Errore selezione fenomeni: {e}")

            # Seleziona formato
            try:
                format_select = Select(
                    self.driver.find_element(By.ID, "formato")
                )
                format_select.select_by_value(formato)
                logger.info(f"Formato: {formato}")
            except Exception as e:
                logger.warning(f"Errore selezione formato: {e}")

            # Click sul pulsante di download
            try:
                download_button = self.driver.find_element(
                    By.XPATH,
                    "//input[@type='submit'][@value='Scarica']"
                    # O il testo/id effettivo del bottone
                )
                download_button.click()
                logger.info("Download avviato...")

                # Attendi il download
                time.sleep(5)

                # Verifica che il file sia stato scaricato
                output_dir = Path(config.OUTPUT_DIR)
                files = list(output_dir.glob(f"*{station_id}*"))

                if files:
                    latest_file = max(files, key=lambda p: p.stat().st_mtime)
                    logger.info(f"File scaricato: {latest_file}")
                    return str(latest_file)
                else:
                    logger.warning("File non trovato dopo il download")
                    return None

            except Exception as e:
                logger.error(f"Errore durante il download: {e}")
                return None

        except Exception as e:
            logger.error(f"Errore generale: {e}")
            return None

    def get_multiple_stations_data(
        self,
        date: datetime,
        station_ids: List[str] = None,
        fenomeni: List[str] = None
    ) -> Dict[str, str]:
        """
        Scarica dati per multiple stazioni

        Args:
            date: Data da scaricare
            station_ids: Lista ID stazioni (None = tutte)
            fenomeni: Lista fenomeni (None = tutti)

        Returns:
            Dict con {station_id: file_path}
        """
        results = {}

        try:
            # Carica stazioni
            stations_df = self.load_stations()

            if station_ids:
                stations_df = stations_df[
                    stations_df['id'].isin(station_ids)
                ]

            # Scarica per ogni stazione
            for _, station in stations_df.iterrows():
                file_path = self.get_station_data(
                    station_id=station['id'],
                    station_name=station['nome'],
                    date=date,
                    fenomeni=fenomeni
                )

                if file_path:
                    results[station['id']] = file_path

                # Pausa tra richieste
                time.sleep(2)

            return results

        finally:
            self._close_driver()

    def __enter__(self):
        """Context manager entry"""
        self._init_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self._close_driver()


if __name__ == "__main__":
    # Test dello scraper
    scraper = LiguriaMeteoScraper(headless=False)

    # Esempio: scarica dati di ieri
    yesterday = datetime.now() - timedelta(days=1)

    # Nota: dovrai fornire un ID stazione valido
    # file_path = scraper.get_station_data(
    #     station_id="YOUR_STATION_ID",
    #     station_name="Nome Stazione",
    #     date=yesterday
    # )

    print("Scraper pronto. Configura gli ID delle stazioni per l'uso.")
