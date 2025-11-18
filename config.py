"""
Configurazione per lo scraper meteo Regione Liguria
"""

# URL del servizio meteo
METEO_URL = "https://ambientepub.regione.liguria.it/SiraQualMeteo/script/PubAccessoDatiMeteo.asp"

# Percorsi file
STATIONS_CSV = "data/stazioni.csv"
OUTPUT_DIR = "data/output"
LOGS_DIR = "logs"

# Parametri scraping
DEFAULT_WAIT_TIME = 10  # secondi di attesa per caricamento pagina
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # secondi tra tentativi

# Fenomeni meteorologici da monitorare
FENOMENI = {
    "TEMPERATURA": "Temperatura",
    "PRECIPITAZIONE": "Precipitazione",
    "VENTO_VELOCITA": "Velocità Vento",
    "VENTO_DIREZIONE": "Direzione Vento",
    "UMIDITA": "Umidità Relativa",
    "PRESSIONE": "Pressione Atmosferica",
    "RADIAZIONE": "Radiazione Solare"
}

# Criteri di sicurezza per cantiere
# Basati su normative italiane e best practices ingegneristiche
SAFETY_THRESHOLDS = {
    # Precipitazioni (mm/h)
    "precipitazione_max": 5.0,  # Oltre 5mm/h lavori sospesi
    "precipitazione_warning": 2.0,  # Tra 2-5mm/h attenzione

    # Vento (m/s)
    "vento_max": 11.0,  # Oltre 11 m/s (~40 km/h) lavori in quota sospesi
    "vento_warning": 8.0,  # Tra 8-11 m/s attenzione lavori in quota

    # Temperatura (°C)
    "temperatura_min": -5.0,  # Sotto -5°C rischio gelo malte/calcestruzzi
    "temperatura_max": 35.0,  # Oltre 35°C rischio stress termico lavoratori
    "temperatura_warning_min": 0.0,
    "temperatura_warning_max": 32.0,

    # Umidità relativa (%)
    "umidita_min": 20.0,  # Troppo secco, rischio polveri
    "umidita_max": 95.0,  # Troppo umido, condensa

    # Visibilità (metri)
    "visibilita_min": 200.0,  # Sotto 200m visibilità insufficiente

    # Cumulo precipitazioni giornaliere (mm)
    "pioggia_24h_max": 30.0,  # Oltre 30mm/24h terreno saturo
}

# Pesi per calcolo score sicurezza (0-100)
SAFETY_WEIGHTS = {
    "precipitazione": 0.30,
    "vento": 0.25,
    "temperatura": 0.20,
    "umidita": 0.10,
    "visibilita": 0.15
}

# Categorie di idoneità cantiere
WORKSITE_CATEGORIES = {
    "OTTIMO": {"min": 80, "color": "green", "desc": "Condizioni ottime per lavorare"},
    "BUONO": {"min": 65, "color": "lightgreen", "desc": "Condizioni buone, nessuna restrizione"},
    "ACCETTABILE": {"min": 50, "color": "yellow", "desc": "Condizioni accettabili, attenzione a specifiche attività"},
    "LIMITATO": {"min": 35, "color": "orange", "desc": "Limitazioni per lavori in quota o esterni"},
    "SCONSIGLIATO": {"min": 20, "color": "red", "desc": "Lavori esterni sconsigliati"},
    "VIETATO": {"min": 0, "color": "darkred", "desc": "Lavori esterni vietati per sicurezza"}
}

# Tipo di lavori in cantiere
WORK_TYPES = {
    "SCAVI": ["precipitazione", "vento"],
    "OPERE_IN_QUOTA": ["vento", "precipitazione", "visibilita"],
    "GETTO_CLS": ["precipitazione", "temperatura"],
    "FACCIATE": ["precipitazione", "vento", "temperatura"],
    "COPERTURE": ["vento", "precipitazione"],
    "INTERNI": ["temperatura", "umidita"],
    "MOVIMENTI_TERRA": ["precipitazione"],
    "GRU_SOLLEVAMENTI": ["vento"]
}
