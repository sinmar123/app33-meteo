#!/usr/bin/env python3
"""
Parsing delle stazioni meteo fornite dall'utente
"""

import csv

# Mapping province -> sigla
PROVINCE_SIGLA = {
    'Genova': 'GE',
    'Imperia': 'IM',
    'La Spezia': 'SP',
    'Savona': 'SV'
}

def parse_stations(input_text):
    """Parse delle stazioni dal testo fornito"""

    lines = input_text.strip().split('\n')

    # Rimuovi header se presente
    if lines[0].startswith('Stazione'):
        lines = lines[1:]

    stations = []
    province_counters = {'GE': 0, 'IM': 0, 'SP': 0, 'SV': 0}

    for line in lines:
        if ',' not in line:
            continue

        parts = line.split(',')
        if len(parts) < 2:
            continue

        nome = parts[0].strip()
        provincia = parts[1].strip()

        if not nome or not provincia:
            continue

        # Genera ID
        sigla = PROVINCE_SIGLA.get(provincia, 'XX')
        province_counters[sigla] += 1
        station_id = f"{sigla}{province_counters[sigla]:03d}"

        # Prova a estrarre il comune dal nome
        # Formato comune: "NOME - DETTAGLIO" o "NOME COMUNE"
        comune = ""
        if ' - ' in nome:
            # Es: "GENOVA - PORTO ANTICO" -> comune = "GENOVA"
            comune = nome.split(' - ')[0].strip()
        else:
            # Prendi la prima parola come comune
            comune = nome.split()[0].strip()

        stations.append({
            'id': station_id,
            'nome': nome,
            'provincia': sigla,
            'comune': comune,
            'quota': '',
            'lat': '',
            'lon': ''
        })

    return stations

def main():
    # Leggi il file con i dati grezzi (lo creo prima)
    raw_data = """Stazione,Provincia
ALPE GORRETO,Genova
ALPE VOBBIA,Genova
AMBORZASCO,Genova
ARENZANO,Genova
ARENZANO-PORTO,Genova
BARBAGELATA,Genova
BARGAGLI,Genova
BARGONE,Genova
BAVARI,Genova
BORZONE,Genova
BRUGNETO DIGA,Genova
BUSALLA,Genova
CABANNE,Genova
CAMINATA,Genova
CAMOGLI,Genova
CAMPO LIGURE,Genova
CARASCO,Genova
CASSAGNA,Genova
CAVI DI LAVAGNA,Genova
CHIAVARI,Genova
CHIAVARI - CAPERANA,Genova
CICHERO,Genova
COLONIA ARNALDI,Genova
CRETO,Genova
CROCE ORERO,Genova
CROCEFIESCHI - SANTUARIO,Genova
CROCETTA DI ORERO,Genova
DAVAGNA,Genova
DIGA VAL NOCI,Genova
FALLAROSA,Genova
FIORINO,Genova
FONTANA FRESCA,Genova
GENOVA - BOLZANETO,Genova
GENOVA - BORGO INCROCIATI,Genova
GENOVA - CASTELLACCIO,Genova
GENOVA - CENTRO FUNZIONALE,Genova
GENOVA - CERTOSA,Genova
GENOVA - DIPARTIMENTO DI FISICA,Genova
GENOVA - FEREGGIANO,Genova
GENOVA - FIRPO,Genova
GENOVA - FIUMARA,Genova
GENOVA - GAVETTE,Genova
GENOVA - GEIRATO,Genova
GENOVA - GRANARA,Genova
GENOVA - MOLASSANA,Genova
GENOVA - PEGLI,Genova
GENOVA - PONTEDECIMO,Genova
GENOVA - PORTO ANTICO,Genova
GENOVA - PRATO,Genova
GENOVA - PUNTA VAGNO,Genova
GENOVA - QUEZZI,Genova
GENOVA - RIVAROLO,Genova
GENOVA - ROSATA,Genova
GENOVA - S.ILARIO,Genova
GENOVA - STURLA,Genova
GENOVA - UNIVERSITA',Genova
GIACOPIANE - DIGA,Genova
GIACOPIANE - LAGO,Genova
ISOVERDE,Genova
LA PRESA,Genova
LAVAGNA - PORTO,Genova
LAVEZZE - LAGO,Genova
LERCA,Genova
LOCO CARCHELLI,Genova
MADONNA DELLE GRAZIE,Genova
MELE,Genova
MIGNANEGO,Genova
MOLINETTO,Genova
MONTE CAPPELLINO,Genova
MONTE DI MEZZO,Genova
MONTE DOMENICO,Genova
MONTE PENNELLO,Genova
MONTE PORTOFINO,Genova
MONTOGGIO,Genova
NEIRONE,Genova
OGNIO,Genova
PANESI,Genova
PASSO DEL TURCHINO,Genova
PIAN DEI RATTI,Genova
PIANA DI SOGLIO,Genova
POLANESI,Genova
PRAI,Genova
PRATOMOLLO,Genova
PREMANICO,Genova
RAPALLO,Genova
REPPIA,Genova
ROSSIGLIONE,Genova
ROVEGNO,Genova
S. ALBERTO,Genova
S. MARGHERITA LIGURE,Genova
S. MARTINO,Genova
S. MICHELE,Genova
S. STEFANO D'AVETO,Genova
SANTUARIO MONTE GAZZO,Genova
SCIARBORASCA,Genova
SCOFFERA,Genova
SELLA GIASSINA,Genova
SESTRI LEVANTE,Genova
SESTRI LEVANTE - PONTESS1,Genova
SESTRI LEVANTE - SARA,Genova
STATALE,Genova
TANADORSO,Genova
TASSANI,Genova
TIGLIETO,Genova
TIGLIOLO,Genova
TORRIGLIA,Genova
TORRIGLIA - GARAVENTA,Genova
VALBREVENNA - GORRA,Genova
VALLEREGIA,Genova
VICOMORASSO,Genova
VIGANEGO,Genova
VIGNOLO,Genova
VOBBIETTA,Genova
AIROLE,Imperia
BARCHEO,Imperia
BESTAGNO,Imperia
BORGOMARO,Imperia
BORGONUOVO,Imperia
BUGGIO,Imperia
CERIANA,Imperia
CIPRESSA,Imperia
COLLA ROSSA,Imperia
COLLE BELENDA,Imperia
COLLE D'OGGIA,Imperia
COLLE DI NAVA,Imperia
DIANO CASTELLO,Imperia
DIANO CASTELLO - VARCAVELLO,Imperia
DOLCEACQUA - MOLINETTI,Imperia
DOLCEDO,Imperia
IMPERIA - OSS. METEOSISMICO,Imperia
ISOLABONA,Imperia
MERELLI,Imperia
MONTALTO LIGURE,Imperia
MONTE MAURE,Imperia
PACIALLA,Imperia
PASSO GHIMBEGNA,Imperia
PIEVE DI TECO (IDRO),Imperia
PIEVE DI TECO,Imperia
PIGNA,Imperia
PIZZEGLIO,Imperia
POGGIO FEARZA,Imperia
PORNASSIO,Imperia
RANZO,Imperia
ROCCHETTA NERVINA,Imperia
RUGGE DI PONTEDASSIO,Imperia
SANREMO,Imperia
SEBORGA,Imperia
SELLA DI GOUTA,Imperia
TORRI,Imperia
TRIORA,Imperia
VALLE ARMEA - PONTE,Imperia
VALLE TANE,Imperia
VENTIMIGLIA,Imperia
VERDEGGIA,Imperia
AMEGLIA FOCE MAGRA,La Spezia
BRUGNATO,La Spezia
CALICE AL C. - MOLUNGHI,La Spezia
CALICE AL CORNOVIGLIO,La Spezia
CARRO,La Spezia
CASALE DI PIGNONE,La Spezia
CASONI DI SUVERO,La Spezia
CASTELNUOVO MAGRA,La Spezia
CEMBRANO,La Spezia
CHIUSOLA,La Spezia
CORNIOLO,La Spezia
CUCCARELLO,La Spezia
FORNOLA,La Spezia
FRAMURA,La Spezia
LA FOCE,La Spezia
LA FOCE - MTE VISEGGI,La Spezia
LA MACCHIA,La Spezia
LA SPEZIA,La Spezia
LA SPEZIA - FABIANO,La Spezia
LEVANTO,La Spezia
LEVANTO - SAN GOTTARDO,La Spezia
LUNI - PROVASCO,La Spezia
MARINELLA DI SARZANA,La Spezia
MATTARANA,La Spezia
MATTARANA - DATI DAL 2010.03.30,La Spezia
MONTALBANO,La Spezia
MONTE BEVERONE,La Spezia
MONTE ROCCHETTA,La Spezia
MONTEROSSO,La Spezia
NASCETO,La Spezia
PADIVARMA,La Spezia
PIANA BATTOLLA - PONTE,La Spezia
PITELLI,La Spezia
PONTE COLOMBIERA,La Spezia
PORTOVENERE - COMUNE,La Spezia
RICCO' DEL GOLFO,La Spezia
ROMITO MAGRA,La Spezia
S. MARGHERITA VARA,La Spezia
SARZANA,La Spezia
SCURTABO',La Spezia
SERO' DI ZIGNAGO,La Spezia
SESTA GODANO,La Spezia
TAGLIETO,La Spezia
TAVARONE,La Spezia
VARESE LIGURE,La Spezia
VERNAZZA,La Spezia
ALASSIO,Savona
ALBENGA - ISOLABELLA,Savona
ALBENGA - MOLINO BRANCA,Savona
ALBISOLA,Savona
ALPICELLA,Savona
ALTARE,Savona
BOLSINE,Savona
CAIRO MONTENOTTE,Savona
CALICE LIGURE,Savona
CALIZZANO,Savona
CAPO VADO,Savona
CARCARE,Savona
CASTELVECCHIO DI R. B.,Savona
CENESI,Savona
CENGIO,Savona
CISANO SUL NEVA (METEO),Savona
COLLE DEL MELOGNO,Savona
COLLE DI CADIBONA,Savona
CONNA,Savona
DEGO - GIRINI,Savona
ELLERA - FOGLIETTO,Savona
FEGLINO,Savona
FERRANIA,Savona
IL PERO,Savona
LAVAGNOLA,Savona
MALLARE,Savona
MANIE,Savona
MARINA LOANO,Savona
MONTAGNA,Savona
MONTE SETTEPANI,Savona
MONTENOTTE INFERIORE,Savona
MURIALDO,Savona
ONZO - PONTEROTTO,Savona
OSIGLIA,Savona
PIAMPALUDO,Savona
PIANA CRIXIA,Savona
POGLI D'ORTOVERO,Savona
PONTE POGGI,Savona
SANDA,Savona
SANTUARIO DI SAVONA,Savona
SASSELLO,Savona
SAVONA - ISTITUTO NAUTICO,Savona
STELLA - BURDONE,Savona
STELLA S. GIUSTINA,Savona
STELLANELLO,Savona
TESTICO,Savona
URBE - VARA SUP.,Savona
VALZEMOLA,Savona
VERZI LOANO,Savona
VILLA PONZA,Savona"""

    print("Parsing stazioni meteo...")
    stations = parse_stations(raw_data)

    print(f"\n✓ Trovate {len(stations)} stazioni")
    print(f"  - Genova: {sum(1 for s in stations if s['provincia'] == 'GE')}")
    print(f"  - Imperia: {sum(1 for s in stations if s['provincia'] == 'IM')}")
    print(f"  - La Spezia: {sum(1 for s in stations if s['provincia'] == 'SP')}")
    print(f"  - Savona: {sum(1 for s in stations if s['provincia'] == 'SV')}")

    # Salva CSV
    output_file = 'data/stazioni.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'nome', 'provincia', 'comune', 'quota', 'lat', 'lon'])
        writer.writeheader()
        writer.writerows(stations)

    print(f"\n✓ Salvato in: {output_file}")

    # Mostra sample
    print("\nPrime 10 stazioni:")
    for i, station in enumerate(stations[:10], 1):
        print(f"  {i:2d}. {station['id']} - {station['nome']:40s} [{station['provincia']}]")

    print("\nUltime 5 stazioni:")
    for station in stations[-5:]:
        print(f"      {station['id']} - {station['nome']:40s} [{station['provincia']}]")

if __name__ == "__main__":
    main()
