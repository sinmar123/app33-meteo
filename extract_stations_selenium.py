#!/usr/bin/env python3
"""
Estrae stazioni meteo usando Selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import csv

def extract_stations_selenium():
    """Estrae le stazioni usando Selenium"""

    url = "https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo.asp"

    # Configura Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = None

    try:
        print("Inizializzo Chrome...")
        driver = webdriver.Chrome(options=chrome_options)

        print(f"Carico pagina: {url}")
        driver.get(url)

        # Attendi caricamento
        time.sleep(5)

        # Salva screenshot
        driver.save_screenshot("page_screenshot.png")
        print("Screenshot salvato: page_screenshot.png")

        # Salva HTML
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("HTML salvato: page_source.html")

        # Cerca tutti i select
        print("\nCerco elementi SELECT...")
        selects = driver.find_elements(By.TAG_NAME, "select")

        print(f"Trovati {len(selects)} elementi SELECT\n")

        all_stations = []

        for i, select in enumerate(selects):
            try:
                select_id = select.get_attribute("id") or "N/A"
                select_name = select.get_attribute("name") or "N/A"

                print(f"--- SELECT #{i+1} ---")
                print(f"ID: {select_id}")
                print(f"Name: {select_name}")

                # Trova le options
                options = select.find_elements(By.TAG_NAME, "option")

                if options:
                    print(f"Opzioni: {len(options)}")

                    # Mostra prime 5
                    print("Prime 5 opzioni:")
                    for j, opt in enumerate(options[:5]):
                        value = opt.get_attribute("value") or ""
                        text = opt.text.strip()
                        print(f"  [{j}] value='{value}' → {text}")

                    # Se sembra il select delle stazioni, salva tutte
                    if len(options) > 10:  # Probabilmente è il select delle stazioni
                        print(f"\n→ Questo sembra essere il select delle stazioni!")

                        for opt in options:
                            value = opt.get_attribute("value") or ""
                            text = opt.text.strip()

                            if value and text:  # Salta opzioni vuote
                                all_stations.append({
                                    'id': value,
                                    'nome': text,
                                    'select_id': select_id,
                                    'select_name': select_name
                                })

                print()

            except Exception as e:
                print(f"Errore su select #{i+1}: {e}")

        # Salva stazioni in CSV
        if all_stations:
            print(f"\n✓ Trovate {len(all_stations)} stazioni!")

            csv_file = "data/stazioni_estratte.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'nome', 'provincia', 'comune', 'quota', 'lat', 'lon'])
                writer.writeheader()

                for station in all_stations:
                    # Prova a parsare il nome per estrarre info
                    nome = station['nome']

                    # Formato comune: "NOME STAZIONE (COMUNE) - PROVINCIA"
                    # o semplicemente "NOME STAZIONE"

                    row = {
                        'id': station['id'],
                        'nome': nome,
                        'provincia': '',  # Da compilare manualmente
                        'comune': '',     # Da compilare manualmente
                        'quota': '',      # Da compilare manualmente
                        'lat': '',        # Da compilare manualmente
                        'lon': ''         # Da compilare manualmente
                    }
                    writer.writerow(row)

            print(f"Stazioni salvate in: {csv_file}")

            # Mostra sample
            print("\nPrime 10 stazioni:")
            for station in all_stations[:10]:
                print(f"  {station['id']:20s} → {station['nome']}")

        else:
            print("⚠ Nessuna stazione trovata")

        return len(all_stations) > 0

    except Exception as e:
        print(f"Errore: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if driver:
            driver.quit()
            print("\nBrowser chiuso")

if __name__ == "__main__":
    success = extract_stations_selenium()
    exit(0 if success else 1)
