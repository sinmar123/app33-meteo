#!/usr/bin/env python3
"""
Script per estrarre l'elenco delle stazioni meteo dalla pagina
"""

import requests
from bs4 import BeautifulSoup
import re

def extract_stations():
    """Estrae le stazioni dalla pagina"""

    url = "https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo.asp"

    # Simula un browser reale
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
    }

    session = requests.Session()

    try:
        print(f"Tentativo di connessione a: {url}")
        response = session.get(url, headers=headers, timeout=10)

        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            print(f"Lunghezza risposta: {len(response.text)} caratteri")

            # Salva la risposta per analisi
            with open('page_raw.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("Pagina salvata in page_raw.html")

            # Parse con BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Cerca select/option per le stazioni
            print("\nCerco campi SELECT nella pagina...")
            selects = soup.find_all('select')

            for i, select in enumerate(selects):
                print(f"\n--- SELECT #{i+1} ---")
                print(f"ID: {select.get('id', 'N/A')}")
                print(f"Name: {select.get('name', 'N/A')}")

                options = select.find_all('option')
                if options:
                    print(f"Numero opzioni: {len(options)}")
                    print("Prime 5 opzioni:")
                    for opt in options[:5]:
                        value = opt.get('value', '')
                        text = opt.text.strip()
                        print(f"  value='{value}' → {text}")

            # Cerca anche eventuali javascript/ajax
            scripts = soup.find_all('script')
            print(f"\nTrovati {len(scripts)} script tags")

            return True

        else:
            print(f"Errore: {response.status_code}")
            print(f"Risposta: {response.text[:500]}")
            return False

    except Exception as e:
        print(f"Errore: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    extract_stations()
