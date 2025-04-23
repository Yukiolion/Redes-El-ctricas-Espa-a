# %%
import requests
import pandas as pd
import numpy as np
from pprint import pprint
from datetime import datetime

# %%
# Versiones

print(f"numpy=={np.__version__}")
print(f"pandas=={pd.__version__}")
print(f"requests=={requests.__version__}")

# %%
# Constantes comunes
URL = "https://apidatos.ree.es" # URL base de la API
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Host": "apidatos.ree.es",
    "User-Agent": "Mozilla/5.0"
}

# Diccionario de geo_ids y nombres de regiones
region_ids = {
    "8741": "peninsular",
    "8742": "canarias",
    "8743": "baleares",
    "8744": "ceuta",
    "8745": "melilla",
    "4": "andalucia",
    "5": "aragon",
    "6": "cantabria",
    "7": "castilla la mancha",
    "8": "castilla y leon",
    "9": "cataluña",
    "10": "pais vasco",
    "11": "principado de asturias",
    "13": "comunidad de madrid",
    "14": "comunidad de navarra",
    "15": "comunidad de valenciana",
    "16": "extremadura",
    "17": "galicia",
    "20": "la rioja",
    "21": "region de murcia"
}

# %%
filtro_balance = '/es/datos/balance/balance-electrico'

filtro_demanda = '/es/datos/demanda/evolucion'
filtro_general = '/es/datos/demanda/ire-general'
filtro_industria = '/es/datos/demanda/ire-industria'
filtro_servicios = '/es/datos/demanda/ire-servicios'

filtro_generacion = "/es/datos/generacion/estructura-generacion"
filtro_renovable = "/es/datos/generacion/evolucion-renovable-no-renovable"

# %%
def Balance_electrico(filtro_balance, URL, HEADERS):

    filtro_balance

    endpoint = f"{URL}/{filtro_balance}"

    # Inicializamos un DataFrame vacío para almacenar los datos
    df_balance = pd.DataFrame()

    # Iteramos sobe los años de 2019 a 2024 y extraemos los datos de balance
    # de cada región para cada año
    for year in range(2015, 2026):

        if year < 2025:
            start_date = f"{year}-01-01T00:00"
            end_date = f"{year}-12-31T23:59"
            TIME_TRUNC = "day"
        else:
            start_date = f"{year}-01-01T00:00"
            end_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
            TIME_TRUNC = "day"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": TIME_TRUNC,
                "geo_id": geo_id
            }

            response = requests.get(endpoint, headers=HEADERS, params=params)

            data = response.json()
            included = data.get('included', [])

            registros = []
            # Extraemos los datos de balance
            # para cada grupo de energía
            # y cada indicador
            for grupo in included:
                group_name = grupo['attributes']['title']
                contenidos = grupo['attributes'].get('content', [])

                for item in contenidos:
                    indicador = item['attributes']['title']
                    valores = item['attributes'].get('values', [])
                    # Extraemos los valores para cada indicador
                    # y los almacenamos en el DataFrame
                    for punto in valores:
                        registros.append({
                            'fecha': punto['datetime'],
                            'valor': punto['value'],
                            'tipo': indicador,
                            'energia': group_name,
                            'region': region_name,
                        })
            # Convertimos los registros a un DataFrame
            # y lo concatenamos al DataFrame principal
            df_balance_year = pd.DataFrame(registros)
            df_balance = pd.concat([df_balance, df_balance_year], ignore_index=True)

    return df_balance


# %%
def demanda_evolucion(filtro_demanda, URL, HEADERS):

    filtro_demanda

    endpoint = f"{URL}/{filtro_demanda}"
    # Inicializamos un df vacío para almacenar los datos
    df_demanda = pd.DataFrame()
    # Iteramos sobre los años y regiones
    for year in range(2015, 2026):

        if year < 2025:
            start_date = f"{year}-01-01T00:00"
            end_date = f"{year}-12-31T23:59"
            TIME_TRUNC = "day"
        else:
            start_date = f"{year}-01-01T00:00"
            end_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
            TIME_TRUNC = "day"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": TIME_TRUNC,
                "geo_id": geo_id
            }

            response = requests.get(endpoint, headers=HEADERS, params=params)

            data = response.json()
            included = data.get('included', [])

            registros = []

            for serie in included:
                indicador = serie['attributes']['title']
                valores = serie['attributes'].get('values', [])
                # Extraer los valores de la serie
                for punto in valores:
                    registros.append({
                        'fecha': punto['datetime'],
                        'valor': punto['value'],
                        'indicador': indicador,
                        'region': region_name,
                        'año': year
                    })

            df_demanda_year = pd.DataFrame(registros)
            df_demanda = pd.concat([df_demanda, df_demanda_year], ignore_index=True)

    return df_demanda

# %%
def demanda_ire_general(filtro_general, URL, HEADERS):
    
    filtro_general

    endpoint = f"{URL}/{filtro_demanda}"

    # Inicializamos un DataFrame vacío
    df_ire_general = pd.DataFrame()

    # Iteramos sobre los años y regiones
    for year in range(2015, 2026):

        if year < 2025:
            start_date = f"{year}-01-01T00:00"
            end_date = f"{year}-12-31T23:59"
            TIME_TRUNC = "month"
        else:
            start_date = f"{year}-01-01T00:00"
            end_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
            TIME_TRUNC = "month"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": TIME_TRUNC,
                "geo_id": geo_id
            }

            response = requests.get(endpoint, headers=HEADERS, params=params)

            if response.status_code != 200:
                print(f"Error {response.status_code} para región: {region_name} ({geo_id}), año {year}")
                continue

            data = response.json()
            included = data.get('included', [])

            registros = []

            for serie in included:
                indicador = serie['attributes']['title']
                valores = serie['attributes'].get('values', [])
                for punto in valores:
                    registros.append({
                        'fecha': punto['datetime'],
                        'valor': punto['value'],
                        'porcentaje': punto.get('percentage'),
                        'indicador': indicador,
                        'region': region_name,
                        
                    })

            df_ire_year = pd.DataFrame(registros)
            df_ire_general = pd.concat([df_ire_general, df_ire_year], ignore_index=True)

    return df_ire_general

# %%
def demanda_ire_industria(filtro_industria, URL, HEADERS):

    filtro_industria

    endpoint = f"{URL}/{filtro_demanda}"

    # Inicializamos un DataFrame vacío
    df_ire_industria = pd.DataFrame()

    # Iteramos sobre los años y regiones
    for year in range(2015, 2026):

        if year < 2025:
            start_date = f"{year}-01-01T00:00"
            end_date = f"{year}-12-31T23:59"
            TIME_TRUNC = "month"
        else:
            start_date = f"{year}-01-01T00:00"
            end_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
            TIME_TRUNC = "month"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": TIME_TRUNC,
                "geo_id": geo_id
            }

            response = requests.get(endpoint, headers=HEADERS, params=params)

            if response.status_code != 200:
                print(f"Error {response.status_code} para región: {region_name} ({geo_id}), año {year}")
                continue

            data = response.json()
            included = data.get('included', [])

            registros = []

            for serie in included:
                indicador = serie['attributes']['title']
                valores = serie['attributes'].get('values', [])
                for punto in valores:
                    registros.append({
                        'fecha': punto['datetime'],
                        'valor': punto['value'],
                        'porcentaje': punto.get('percentage'),
                        'indicador': indicador,
                        'region': region_name,
                        'año': year
                    })

            df_ire_industria_year = pd.DataFrame(registros)
            df_ire_industria = pd.concat([df_ire_industria, df_ire_industria_year], ignore_index=True)

    return df_ire_industria

# %%
def demanda_ire_servicios(filtro_servicios, URL, HEADERS):

    filtro_servicios

    endpoint = f"{URL}/{filtro_demanda}"

    # Inicializamos un DataFrame vacío
    df_ire_servicios = pd.DataFrame()

    # Iteramos sobre los años y regiones
    for year in range(2015, 2026):

        if year < 2025:
            start_date = f"{year}-01-01T00:00"
            end_date = f"{year}-12-31T23:59"
            TIME_TRUNC = "month"
        else:
            start_date = f"{year}-01-01T00:00"
            end_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
            TIME_TRUNC = "month"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": TIME_TRUNC,
                "geo_id": geo_id
            }

            response = requests.get(endpoint, headers=HEADERS, params=params)

            if response.status_code != 200:
                print(f"Error {response.status_code} para región: {region_name} ({geo_id}), año {year}")
                continue

            data = response.json()
            included = data.get('included', [])

            registros = []

            for serie in included:
                indicador = serie['attributes']['title']
                valores = serie['attributes'].get('values', [])
                for punto in valores:
                    registros.append({
                        'fecha': punto['datetime'],
                        'valor': punto['value'],
                        'porcentaje': punto.get('percentage'),
                        'indicador': indicador,
                        'region': region_name,
                        'año': year
                    })

            df_ire_servicios_year = pd.DataFrame(registros)
            df_ire_servicios = pd.concat([df_ire_servicios, df_ire_servicios_year], ignore_index=True)

    return df_ire_servicios

# %%
def generacion(filtro_generacion, URL, HEADERS):

    filtro_generacion

    endpoint = f"{URL}{filtro_generacion}"

    df_generacion = pd.DataFrame()
    ## Iterar sobre los años
    for year in range(2015, 2026):

        if year < 2025:
            start_date = f"{year}-01-01T00:00"
            end_date = f"{year}-12-31T23:59"
            TIME_TRUNC = "day"
        else:
            start_date = f"{year}-01-01T00:00"
            end_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
            TIME_TRUNC = "day"

        # Iterar sobre los geo_ids y nombres de regiones
        # para cada año y geo_id
        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": TIME_TRUNC,
                "geo_id": geo_id
            }

            response = requests.get(endpoint, headers=HEADERS, params=params)

            if response.status_code == 200:
                try:
                    data = response.json()
                    included = data.get('included', [])

                    if included:
                        registros = []

                        # Iterar sobre los grupos de datos en 'included'
                        for grupo in included:
                            group_name = grupo['attributes'].get('title', 'Desconocido')
                            group_type = grupo['attributes'].get('type', 'Desconocido')
                            contenidos = grupo['attributes'].get('values', [])

                            # Iterar sobre los valores de generación
                            for punto in contenidos:
                                registros.append({
                                    'fecha': punto.get('datetime', 'Desconocido'),
                                    'valor': punto.get('value', 0),
                                    'porcentaje': punto.get('percentage', 0),
                                    'indicador': group_name,
                                    'region': region_name,
                                    'tipo': group_type,
                                    'año': year
                                })

                        df_generacion_year = pd.DataFrame(registros)
                        df_generacion = pd.concat([df_generacion, df_generacion_year], ignore_index=True)

                except Exception as e:
                    print("Contenido de la respuesta:", response.text)

            else:
                print(f"Error en la solicitud para {region_name} {year}. Código: {response.status_code}")

    return df_generacion

# %%
def renov_norenov(filtro_renovable, URL, HEADERS):

    filtro_renovable

    endpoint = f"{URL}{filtro_generacion}"

    df_renovable = pd.DataFrame()
    ## Iterar sobre los años
    for year in range(2015, 2026):

        if year < 2025:
            start_date = f"{year}-01-01T00:00"
            end_date = f"{year}-12-31T23:59"
            TIME_TRUNC = "day"
        else:
            start_date = f"{year}-01-01T00:00"
            end_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
            TIME_TRUNC = "day"

        # Iterar sobre los geo_ids y nombres de regiones
        # para cada año y geo_id
        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": TIME_TRUNC,
                "geo_id": geo_id
            }

            response = requests.get(endpoint, headers=HEADERS, params=params)

            if response.status_code == 200:
                try:
                    data = response.json()
                    included = data.get('included', [])

                    if included:
                        registros = []

                        # Iterar sobre los grupos de datos en 'included'
                        for grupo in included:
                            group_name = grupo['attributes'].get('title', 'Desconocido')
                            group_type = grupo['attributes'].get('type', 'Desconocido')
                            contenidos = grupo['attributes'].get('values', [])

                            # Iterar sobre los valores de generación
                            for punto in contenidos:
                                registros.append({
                                    'fecha': punto.get('datetime', 'Desconocido'),
                                    'valor': punto.get('value', 0),
                                    'porcentaje': punto.get('percentage', 0),
                                    'indicador': group_name,
                                    'region': region_name,
                                    'tipo': group_type,
                                    'año': year
                                })

                        df_renovable_year = pd.DataFrame(registros)
                        df_renovable = pd.concat([df_renovable, df_renovable_year], ignore_index=True)

                except Exception as e:
                    print("Contenido de la respuesta:", response.text)

            else:
                print(f"Error en la solicitud para {region_name} {year}. Código: {response.status_code}")

    return df_renovable

# %%
def fronteras(URL, HEADERS):

    # Lista de países
    lista_paises = ['francia-frontera', 'portugal-frontera', 'marruecos-frontera', 'andorra-frontera']

    datos_intercambios = []

    for pais in lista_paises:
        # Endpoint para intercambios
        filtro_intercambio = f"/es/datos/intercambios/{pais}"
        endpoint = f"{URL}{filtro_intercambio}"
        # Iterar sobre los años y extraer datos de cada año
        # y cada país para el año 2015 al 2025
        for year in range(2015, 2026):

            if year < 2025:
                start_date = f"{year}-01-01T00:00"
                end_date = f"{year}-12-31T23:59"
                TIME_TRUNC = "day"
            else:
                start_date = f"{year}-01-01T00:00"
                end_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
                TIME_TRUNC = "day"

            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": TIME_TRUNC,
            }

            response = requests.get(endpoint, headers=HEADERS, params=params)

            if response.status_code == 200:
                data = response.json()
                # Verificar si hay datos disponibles
                valores = data["included"][0]["attributes"].get("values", [])
                if valores:
                    df = pd.DataFrame(valores)
                    df["pais"] = pais
                    df["año"] = year
                    datos_intercambios.append(df)
            else:
                print(f"Error en la solicitud para {pais} en {year}. Código: {response.status_code}")

    # Unir todos los datos en un único DataFrame
    df_fronteras = pd.concat(datos_intercambios, ignore_index=True)

    return df_fronteras

# %%
def extraccion():
    """
    Función para extraer datos de la API de REE.
    """
    print('Extrayendo datos del Balance Eléctrico...')
    df_balance = Balance_electrico(filtro_balance, URL, HEADERS)
    
    print('Extrayendo datos de la Demanda Eléctrica...')
    df_demanda = demanda_evolucion(filtro_demanda, URL, HEADERS)
    print('Extrayendo datos de la IRE General...')
    df_ire_general = demanda_ire_general(filtro_general, URL, HEADERS)
    print('Extrayendo datos de la IRE Industria...')
    df_ire_industria = demanda_ire_industria(filtro_industria, URL, HEADERS)
    print('Extrayendo datos de la IRE Servicios...')
    df_ire_servicios = demanda_ire_servicios(filtro_servicios, URL, HEADERS)

    print('Extrayendo datos de la Generación Eléctrica...')
    df_generacion = generacion(filtro_generacion, URL, HEADERS)
    print('Extrayendo datos de la Generación Renovable y No Renovable...')
    df_renovable = renov_norenov(filtro_renovable, URL, HEADERS)

    print('Extrayendo datos de los intercambios entre países...')
    df_fronteras = fronteras(URL, HEADERS)

    return {
        "balance": df_balance,
        "demanda": df_demanda,
        "ire_general": df_ire_general,
        "ire_industria": df_ire_industria,
        "ire_servicios": df_ire_servicios,
        "generacion": df_generacion,
        "renovable": df_renovable,
        "fronteras": df_fronteras,
    }