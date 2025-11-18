"""
Algoritmo per valutazione sicurezza cantiere basato su dati meteorologici
Conforme a normative italiane e best practices ingegneristiche
"""

import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime

import pandas as pd
import numpy as np

import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorksiteSafetyAnalyzer:
    """Analizzatore sicurezza cantiere basato su condizioni meteo"""

    def __init__(self):
        self.thresholds = config.SAFETY_THRESHOLDS
        self.weights = config.SAFETY_WEIGHTS
        self.categories = config.WORKSITE_CATEGORIES

    def _calculate_precipitation_score(self, data: pd.DataFrame) -> Tuple[float, List[str]]:
        """
        Calcola score per precipitazioni

        Args:
            data: DataFrame con colonna 'precipitazione' (mm/h)

        Returns:
            (score 0-100, lista warnings)
        """
        warnings = []

        if 'precipitazione' not in data.columns:
            return 50.0, ["Dati precipitazione non disponibili"]

        # Precipitazione massima oraria
        max_precip = data['precipitazione'].max()
        mean_precip = data['precipitazione'].mean()
        total_precip = data['precipitazione'].sum()

        # Score basato su precipitazione massima
        if max_precip > self.thresholds['precipitazione_max']:
            score = 0.0
            warnings.append(
                f"⚠️ CRITICO: Precipitazione massima {max_precip:.1f} mm/h "
                f"(limite {self.thresholds['precipitazione_max']} mm/h). "
                "LAVORI ESTERNI VIETATI"
            )
        elif max_precip > self.thresholds['precipitazione_warning']:
            score = 40.0
            warnings.append(
                f"⚠️ Attenzione: Precipitazione {max_precip:.1f} mm/h. "
                "Limitare lavori in quota e scavi"
            )
        elif max_precip > 0:
            score = 70.0
            warnings.append(f"Pioggia leggera: {max_precip:.1f} mm/h")
        else:
            score = 100.0

        # Penalizzazione per cumulo giornaliero
        if total_precip > self.thresholds['pioggia_24h_max']:
            score *= 0.5
            warnings.append(
                f"⚠️ Cumulo 24h: {total_precip:.1f} mm. Terreno saturo, "
                "evitare scavi e movimenti terra"
            )

        return score, warnings

    def _calculate_wind_score(self, data: pd.DataFrame) -> Tuple[float, List[str]]:
        """
        Calcola score per vento

        Args:
            data: DataFrame con colonna 'vento_velocita' (m/s)

        Returns:
            (score 0-100, lista warnings)
        """
        warnings = []

        if 'vento_velocita' not in data.columns:
            return 50.0, ["Dati vento non disponibili"]

        max_wind = data['vento_velocita'].max()
        mean_wind = data['vento_velocita'].mean()

        # Score basato su velocità massima vento
        if max_wind > self.thresholds['vento_max']:
            score = 0.0
            warnings.append(
                f"⚠️ CRITICO: Vento {max_wind:.1f} m/s "
                f"({max_wind * 3.6:.1f} km/h). "
                "LAVORI IN QUOTA E CON GRU VIETATI"
            )
        elif max_wind > self.thresholds['vento_warning']:
            score = 30.0
            warnings.append(
                f"⚠️ Attenzione: Vento {max_wind:.1f} m/s "
                f"({max_wind * 3.6:.1f} km/h). "
                "Limitare lavori in quota oltre 2m"
            )
        elif max_wind > 5.0:
            score = 70.0
            warnings.append(
                f"Vento moderato: {max_wind:.1f} m/s. "
                "Attenzione a ponteggi e materiali leggeri"
            )
        else:
            score = 100.0

        return score, warnings

    def _calculate_temperature_score(self, data: pd.DataFrame) -> Tuple[float, List[str]]:
        """
        Calcola score per temperatura

        Args:
            data: DataFrame con colonna 'temperatura' (°C)

        Returns:
            (score 0-100, lista warnings)
        """
        warnings = []

        if 'temperatura' not in data.columns:
            return 50.0, ["Dati temperatura non disponibili"]

        max_temp = data['temperatura'].max()
        min_temp = data['temperatura'].min()
        mean_temp = data['temperatura'].mean()

        score = 100.0

        # Temperatura troppo bassa
        if min_temp < self.thresholds['temperatura_min']:
            score = 20.0
            warnings.append(
                f"⚠️ CRITICO: Temperatura minima {min_temp:.1f}°C. "
                "Gelo: vietato getto CLS, rischio malte. "
                "Proteggere tubazioni"
            )
        elif min_temp < self.thresholds['temperatura_warning_min']:
            score = min(score, 60.0)
            warnings.append(
                f"⚠️ Temperatura bassa {min_temp:.1f}°C. "
                "Attenzione getti e presa malte. Usare additivi antigelo"
            )

        # Temperatura troppo alta
        if max_temp > self.thresholds['temperatura_max']:
            score = min(score, 30.0)
            warnings.append(
                f"⚠️ CRITICO: Temperatura massima {max_temp:.1f}°C. "
                "Rischio stress termico lavoratori. "
                "Turni ridotti e pause frequenti obbligatorie"
            )
        elif max_temp > self.thresholds['temperatura_warning_max']:
            score = min(score, 60.0)
            warnings.append(
                f"⚠️ Caldo intenso {max_temp:.1f}°C. "
                "Aumentare idratazione, ridurre carichi di lavoro"
            )

        return score, warnings

    def _calculate_humidity_score(self, data: pd.DataFrame) -> Tuple[float, List[str]]:
        """
        Calcola score per umidità

        Args:
            data: DataFrame con colonna 'umidita' (%)

        Returns:
            (score 0-100, lista warnings)
        """
        warnings = []

        if 'umidita' not in data.columns:
            return 70.0, ["Dati umidità non disponibili"]

        max_humidity = data['umidita'].max()
        min_humidity = data['umidita'].min()

        score = 100.0

        if max_humidity > self.thresholds['umidita_max']:
            score = 60.0
            warnings.append(
                f"Umidità molto alta {max_humidity:.1f}%. "
                "Difficoltà essiccazione malte e vernici"
            )

        if min_humidity < self.thresholds['umidita_min']:
            score = min(score, 60.0)
            warnings.append(
                f"Umidità molto bassa {min_humidity:.1f}%. "
                "Rischio polveri, bagnare frequentemente"
            )

        return score, warnings

    def _calculate_visibility_score(self, data: pd.DataFrame) -> Tuple[float, List[str]]:
        """
        Calcola score per visibilità

        Args:
            data: DataFrame con colonna 'visibilita' (m)

        Returns:
            (score 0-100, lista warnings)
        """
        warnings = []

        if 'visibilita' not in data.columns:
            return 70.0, ["Dati visibilità non disponibili"]

        min_visibility = data['visibilita'].min()

        if min_visibility < self.thresholds['visibilita_min']:
            score = 20.0
            warnings.append(
                f"⚠️ CRITICO: Visibilità ridotta {min_visibility:.0f}m. "
                "Nebbia fitta: limitare movimentazione mezzi"
            )
        elif min_visibility < 500:
            score = 60.0
            warnings.append(
                f"Visibilità limitata {min_visibility:.0f}m. "
                "Attenzione movimentazione mezzi"
            )
        else:
            score = 100.0

        return score, warnings

    def calculate_overall_score(self, data: pd.DataFrame) -> Dict:
        """
        Calcola score complessivo di sicurezza

        Args:
            data: DataFrame con dati meteo orari

        Returns:
            Dict con score, categoria, warnings e dettagli
        """
        logger.info("Calcolo score di sicurezza cantiere...")

        # Calcola score per ogni parametro
        precip_score, precip_warnings = self._calculate_precipitation_score(data)
        wind_score, wind_warnings = self._calculate_wind_score(data)
        temp_score, temp_warnings = self._calculate_temperature_score(data)
        humidity_score, humidity_warnings = self._calculate_humidity_score(data)
        visibility_score, visibility_warnings = self._calculate_visibility_score(data)

        # Score complessivo pesato
        overall_score = (
            precip_score * self.weights['precipitazione'] +
            wind_score * self.weights['vento'] +
            temp_score * self.weights['temperatura'] +
            humidity_score * self.weights['umidita'] +
            visibility_score * self.weights['visibilita']
        )

        # Determina categoria
        category = None
        for cat_name, cat_info in sorted(
            self.categories.items(),
            key=lambda x: x[1]['min'],
            reverse=True
        ):
            if overall_score >= cat_info['min']:
                category = cat_name
                break

        # Raccogli tutti i warnings
        all_warnings = (
            precip_warnings + wind_warnings + temp_warnings +
            humidity_warnings + visibility_warnings
        )

        result = {
            'overall_score': round(overall_score, 1),
            'category': category,
            'category_info': self.categories[category],
            'scores': {
                'precipitazione': round(precip_score, 1),
                'vento': round(wind_score, 1),
                'temperatura': round(temp_score, 1),
                'umidita': round(humidity_score, 1),
                'visibilita': round(visibility_score, 1)
            },
            'warnings': all_warnings,
            'can_work': overall_score >= self.categories['ACCETTABILE']['min']
        }

        logger.info(
            f"Score calcolato: {overall_score:.1f}/100 - "
            f"Categoria: {category}"
        )

        return result

    def evaluate_work_type(
        self,
        data: pd.DataFrame,
        work_type: str
    ) -> Dict:
        """
        Valuta idoneità per specifico tipo di lavoro

        Args:
            data: DataFrame con dati meteo
            work_type: Tipo di lavoro (es. "OPERE_IN_QUOTA")

        Returns:
            Dict con valutazione specifica
        """
        if work_type not in config.WORK_TYPES:
            raise ValueError(
                f"Tipo lavoro non valido. "
                f"Scegliere tra: {', '.join(config.WORK_TYPES.keys())}"
            )

        # Calcola score generale
        general_result = self.calculate_overall_score(data)

        # Parametri critici per questo tipo di lavoro
        critical_params = config.WORK_TYPES[work_type]

        # Score specifico per questo lavoro (media parametri critici)
        specific_scores = [
            general_result['scores'][param]
            for param in critical_params
            if param in general_result['scores']
        ]

        if specific_scores:
            specific_score = np.mean(specific_scores)
        else:
            specific_score = general_result['overall_score']

        # Determina idoneità specifica
        can_perform = specific_score >= 50.0

        result = {
            'work_type': work_type,
            'specific_score': round(specific_score, 1),
            'can_perform': can_perform,
            'critical_parameters': critical_params,
            'general_assessment': general_result,
            'recommendation': self._get_work_recommendation(
                work_type, specific_score, general_result
            )
        }

        return result

    def _get_work_recommendation(
        self,
        work_type: str,
        specific_score: float,
        general_result: Dict
    ) -> str:
        """Genera raccomandazione per tipo di lavoro"""

        if specific_score >= 80:
            return f"✓ {work_type}: Condizioni ottime, nessuna limitazione"
        elif specific_score >= 65:
            return f"✓ {work_type}: Condizioni buone, procedere normalmente"
        elif specific_score >= 50:
            return (
                f"⚠ {work_type}: Condizioni accettabili, "
                "aumentare supervisione e precauzioni"
            )
        elif specific_score >= 35:
            return (
                f"⚠ {work_type}: Condizioni limitate, "
                "valutare sospensione attività"
            )
        else:
            return f"✗ {work_type}: ATTIVITÀ NON SICURA, sospendere lavori"

    def generate_daily_report(
        self,
        data: pd.DataFrame,
        date: datetime,
        station_name: str
    ) -> str:
        """
        Genera report giornaliero leggibile

        Args:
            data: DataFrame con dati meteo
            date: Data del report
            station_name: Nome stazione meteo

        Returns:
            String con report formattato
        """
        result = self.calculate_overall_score(data)

        report = []
        report.append("=" * 70)
        report.append(f"REPORT SICUREZZA CANTIERE")
        report.append(f"Data: {date.strftime('%d/%m/%Y')}")
        report.append(f"Stazione: {station_name}")
        report.append("=" * 70)
        report.append("")

        # Score generale
        report.append(f"VALUTAZIONE COMPLESSIVA: {result['overall_score']}/100")
        report.append(f"Categoria: {result['category']}")
        report.append(f"Descrizione: {result['category_info']['desc']}")
        report.append("")

        # Idoneità
        if result['can_work']:
            report.append("✓ LAVORI IN CANTIERE: CONSENTITI")
        else:
            report.append("✗ LAVORI IN CANTIERE: SCONSIGLIATI/VIETATI")
        report.append("")

        # Dettaglio score
        report.append("DETTAGLIO PARAMETRI:")
        report.append("-" * 70)
        for param, score in result['scores'].items():
            report.append(f"  {param.title():20s}: {score:5.1f}/100")
        report.append("")

        # Warnings
        if result['warnings']:
            report.append("AVVISI E RACCOMANDAZIONI:")
            report.append("-" * 70)
            for warning in result['warnings']:
                report.append(f"  • {warning}")
            report.append("")

        # Raccomandazioni per tipo lavoro
        report.append("IDONEITÀ PER TIPO DI LAVORO:")
        report.append("-" * 70)
        for work_type in config.WORK_TYPES.keys():
            work_eval = self.evaluate_work_type(data, work_type)
            report.append(f"  {work_eval['recommendation']}")
        report.append("")

        report.append("=" * 70)

        return "\n".join(report)


def load_weather_data(file_path: str) -> pd.DataFrame:
    """
    Carica dati meteo da file CSV

    Args:
        file_path: Percorso file CSV

    Returns:
        DataFrame con dati normalizzati
    """
    try:
        # Prova diversi delimitatori
        for delimiter in [',', ';', '\t']:
            try:
                data = pd.read_csv(file_path, delimiter=delimiter)
                if len(data.columns) > 1:
                    break
            except:
                continue

        logger.info(f"Dati caricati da {file_path}: {len(data)} record")

        # Normalizza nomi colonne (converti in lowercase e rimuovi spazi)
        data.columns = [col.lower().strip().replace(' ', '_') for col in data.columns]

        return data

    except Exception as e:
        logger.error(f"Errore caricamento dati: {e}")
        raise


if __name__ == "__main__":
    # Test dell'analizzatore
    print("WorksiteSafetyAnalyzer pronto per l'uso")
    print("\nCategorie di idoneità:")
    for cat_name, cat_info in config.WORKSITE_CATEGORIES.items():
        print(f"  {cat_name}: {cat_info['desc']}")
