#!/usr/bin/env python3
"""
🏗️ APP WEB - Sistema Meteo e Sicurezza Cantiere
Interfaccia grafica semplice per analisi meteo cantiere
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Importa i moduli del progetto
from worksite_safety import WorksiteSafetyAnalyzer, load_weather_data
import config

# Configurazione pagina
st.set_page_config(
    page_title="Meteo Cantiere - Regione Liguria",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""
<style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stAlert {
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)


def load_stations():
    """Carica elenco stazioni"""
    try:
        stations_df = pd.read_csv('data/stazioni.csv')
        return stations_df
    except Exception as e:
        st.error(f"Errore caricamento stazioni: {e}")
        return None


def create_gauge_chart(score, title):
    """Crea grafico a gauge per lo score"""

    # Determina colore in base allo score
    if score >= 80:
        color = "green"
    elif score >= 65:
        color = "lightgreen"
    elif score >= 50:
        color = "yellow"
    elif score >= 35:
        color = "orange"
    else:
        color = "red"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 20], 'color': "darkred"},
                {'range': [20, 35], 'color': "red"},
                {'range': [35, 50], 'color': "orange"},
                {'range': [50, 65], 'color': "yellow"},
                {'range': [65, 80], 'color': "lightgreen"},
                {'range': [80, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(height=300)
    return fig


def create_parameters_chart(scores):
    """Crea grafico a barre per i parametri"""

    params = list(scores.keys())
    values = list(scores.values())

    colors = ['green' if v >= 70 else 'orange' if v >= 50 else 'red' for v in values]

    fig = go.Figure(data=[
        go.Bar(
            x=params,
            y=values,
            marker_color=colors,
            text=values,
            textposition='auto',
        )
    ])

    fig.update_layout(
        title="Dettaglio Parametri Meteo",
        xaxis_title="Parametro",
        yaxis_title="Score (0-100)",
        yaxis_range=[0, 100],
        height=400
    )

    return fig


def get_category_emoji(category):
    """Restituisce emoji per categoria"""
    emojis = {
        "OTTIMO": "✅",
        "BUONO": "👍",
        "ACCETTABILE": "⚠️",
        "LIMITATO": "⚠️",
        "SCONSIGLIATO": "❌",
        "VIETATO": "🚫"
    }
    return emojis.get(category, "❓")


def main():
    """Applicazione principale"""

    # Header
    st.title("🏗️ Sistema Meteo e Sicurezza Cantiere")
    st.markdown("**Regione Liguria** - Valutazione automatica condizioni lavoro")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configurazione")

        # Carica stazioni
        stations_df = load_stations()

        if stations_df is not None:
            # Selezione stazione
            station_names = [f"{row['id']} - {row['nome']}" for _, row in stations_df.iterrows()]
            selected_station = st.selectbox(
                "📍 Seleziona Stazione",
                options=station_names,
                index=35  # Genova Centro Funzionale
            )

            station_id = selected_station.split(" - ")[0]
            station_name = " - ".join(selected_station.split(" - ")[1:])
        else:
            station_id = "GE036"
            station_name = "GENOVA - CENTRO FUNZIONALE"

        st.markdown("---")

        # Selezione data
        st.subheader("📅 Data Analisi")
        selected_date = st.date_input(
            "Seleziona data",
            value=datetime.now(),
            max_value=datetime.now()
        )

        st.markdown("---")

        # Caricamento file
        st.subheader("📁 Carica Dati Meteo")

        use_example = st.checkbox("Usa dati di esempio", value=True)

        if use_example:
            data_file = "data/esempio_dati_meteo.csv"
            st.info("📊 Usando dati di esempio")
        else:
            uploaded_file = st.file_uploader(
                "Carica file CSV con dati meteo",
                type=['csv'],
                help="Scarica i dati dal sito Regione Liguria e caricali qui"
            )

            if uploaded_file:
                # Salva temporaneamente
                temp_path = Path("data/output") / f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                data_file = str(temp_path)
                st.success(f"✅ File caricato: {uploaded_file.name}")
            else:
                data_file = None
                st.warning("⚠️ Nessun file caricato")

        st.markdown("---")

        # Info
        with st.expander("ℹ️ Informazioni"):
            st.markdown("""
            **Come usare:**
            1. Seleziona una stazione meteo
            2. Scegli la data da analizzare
            3. Carica il file CSV (o usa l'esempio)
            4. Premi "Analizza"

            **Dati richiesti nel CSV:**
            - temperatura (°C)
            - precipitazione (mm/h)
            - vento_velocita (m/s)
            - umidita (%)
            - visibilita (m)
            """)

    # Main content
    if data_file and Path(data_file).exists():

        # Pulsante analisi
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_button = st.button(
                "🔍 ANALIZZA SICUREZZA CANTIERE",
                use_container_width=True,
                type="primary"
            )

        if analyze_button or 'last_analysis' in st.session_state:

            with st.spinner("🔄 Analisi in corso..."):
                try:
                    # Carica dati
                    weather_data = load_weather_data(data_file)

                    # Analizza
                    analyzer = WorksiteSafetyAnalyzer()
                    result = analyzer.calculate_overall_score(weather_data)

                    # Salva in sessione
                    st.session_state['last_analysis'] = {
                        'result': result,
                        'date': selected_date,
                        'station': station_name,
                        'data': weather_data
                    }

                except Exception as e:
                    st.error(f"❌ Errore durante l'analisi: {e}")
                    return

            # Recupera risultati
            analysis = st.session_state['last_analysis']
            result = analysis['result']

            # === RISULTATI ===

            st.markdown("---")
            st.markdown("## 📊 RISULTATI ANALISI")

            # Info analisi
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📅 **Data**: {selected_date.strftime('%d/%m/%Y')}")
            with col2:
                st.info(f"📍 **Stazione**: {station_name}")

            st.markdown("---")

            # Score complessivo
            col1, col2 = st.columns([1, 1])

            with col1:
                st.plotly_chart(
                    create_gauge_chart(result['overall_score'], "Score Sicurezza"),
                    use_container_width=True
                )

            with col2:
                st.markdown("### 🎯 Valutazione Complessiva")
                st.markdown(f"<p class='big-font'>{get_category_emoji(result['category'])} {result['category']}</p>", unsafe_allow_html=True)
                st.markdown(f"**{result['category_info']['desc']}**")

                st.markdown("")

                if result['can_work']:
                    st.success("✅ **LAVORI IN CANTIERE: CONSENTITI**", icon="✅")
                else:
                    st.error("❌ **LAVORI IN CANTIERE: SCONSIGLIATI/VIETATI**", icon="🚫")

            st.markdown("---")

            # Dettaglio parametri
            st.markdown("### 📈 Dettaglio Parametri Meteo")
            st.plotly_chart(
                create_parameters_chart(result['scores']),
                use_container_width=True
            )

            # Tabella parametri
            params_df = pd.DataFrame({
                'Parametro': [p.title() for p in result['scores'].keys()],
                'Score': [f"{v:.1f}/100" for v in result['scores'].values()],
                'Valutazione': [
                    '✅ Ottimo' if v >= 80 else
                    '👍 Buono' if v >= 65 else
                    '⚠️ Accettabile' if v >= 50 else
                    '❌ Critico'
                    for v in result['scores'].values()
                ]
            })
            st.dataframe(params_df, use_container_width=True, hide_index=True)

            st.markdown("---")

            # Avvisi e raccomandazioni
            if result['warnings']:
                st.markdown("### ⚠️ Avvisi e Raccomandazioni")

                for warning in result['warnings']:
                    if 'CRITICO' in warning:
                        st.error(warning, icon="🚫")
                    elif 'Attenzione' in warning or '⚠️' in warning:
                        st.warning(warning, icon="⚠️")
                    else:
                        st.info(warning, icon="ℹ️")

            st.markdown("---")

            # Idoneità per tipo lavoro
            st.markdown("### 🔨 Idoneità per Tipo di Lavoro")

            work_types = list(config.WORK_TYPES.keys())

            # Crea colonne
            cols = st.columns(2)

            for i, work_type in enumerate(work_types):
                work_eval = analyzer.evaluate_work_type(weather_data, work_type)

                with cols[i % 2]:
                    with st.expander(f"**{work_type.replace('_', ' ')}**"):
                        st.metric(
                            "Score Specifico",
                            f"{work_eval['specific_score']:.1f}/100"
                        )

                        if work_eval['can_perform']:
                            st.success(work_eval['recommendation'], icon="✅")
                        else:
                            st.error(work_eval['recommendation'], icon="❌")

                        st.caption(f"Parametri critici: {', '.join(work_eval['critical_parameters'])}")

            st.markdown("---")

            # Dati meteo raw
            with st.expander("📋 Visualizza Dati Meteo Completi"):
                st.dataframe(weather_data, use_container_width=True)

            # Download report
            st.markdown("---")
            st.markdown("### 💾 Esporta Report")

            # Genera report testuale
            report_text = analyzer.generate_daily_report(
                weather_data,
                selected_date,
                station_name
            )

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="📄 Scarica Report TXT",
                    data=report_text,
                    file_name=f"report_cantiere_{selected_date.strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )

            with col2:
                # Prepara CSV
                csv_data = weather_data.to_csv(index=False)
                st.download_button(
                    label="📊 Scarica Dati CSV",
                    data=csv_data,
                    file_name=f"dati_meteo_{selected_date.strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

    else:
        # Messaggio iniziale
        st.info("👈 Configura i parametri nella barra laterale e carica i dati meteo per iniziare l'analisi")

        # Mostra esempio
        st.markdown("### 💡 Esempio di Utilizzo")
        st.markdown("""
        1. **Seleziona** una stazione meteo dalla lista (es: GENOVA - CENTRO FUNZIONALE)
        2. **Scegli** la data da analizzare
        3. **Carica** il file CSV con i dati meteo oppure usa i dati di esempio
        4. **Premi** il pulsante "Analizza"
        5. **Ottieni** un report completo con:
           - Score di sicurezza (0-100)
           - Categoria di idoneità
           - Avvisi e raccomandazioni
           - Valutazione per tipo di lavoro
        """)

        st.markdown("---")

        # Mostra stazioni disponibili
        st.markdown("### 📍 Stazioni Meteo Disponibili")
        if stations_df is not None:
            # Raggruppa per provincia
            col1, col2, col3, col4 = st.columns(4)

            provinces = ['GE', 'IM', 'SP', 'SV']
            province_names = ['Genova', 'Imperia', 'La Spezia', 'Savona']
            cols = [col1, col2, col3, col4]

            for prov, prov_name, col in zip(provinces, province_names, cols):
                with col:
                    prov_stations = stations_df[stations_df['provincia'] == prov]
                    st.metric(prov_name, len(prov_stations))

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray;'>
        🏗️ Sistema Meteo e Sicurezza Cantiere - Regione Liguria<br>
        Basato su D.Lgs 81/2008 e NTC 2018<br>
        <small>Versione 1.0 - 2024</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
