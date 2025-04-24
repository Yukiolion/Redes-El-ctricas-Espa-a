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
def Balance_electrico(filtro_balance, URL, HEADERS, start_date, end_date):

    filtro_balance

    endpoint = f"{URL}/{filtro_balance}"

    # Inicializamos un DataFrame vacío para almacenar los datos
    df_balance = pd.DataFrame()

    TIME_TRUNC = "day"


    for geo_id, region_name in region_ids.items():
        params = {
            "start_date": start_date.strftime("%Y-%m-%dT%H:%M"),
            "end_date": end_date.strftime("%Y-%m-%dT%H:%M"),
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
def demanda_evolucion(filtro_demanda, URL, HEADERS, start_date, end_date):

    filtro_demanda

    endpoint = f"{URL}/{filtro_demanda}"
    # Inicializamos un df vacío para almacenar los datos
    df_demanda = pd.DataFrame()

    TIME_TRUNC = "day"

    for geo_id, region_name in region_ids.items():
        params = {
            "start_date": start_date.strftime("%Y-%m-%dT%H:%M"),
            "end_date": end_date.strftime("%Y-%m-%dT%H:%M"),
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
                    })

        df_demanda_year = pd.DataFrame(registros)
        df_demanda = pd.concat([df_demanda, df_demanda_year], ignore_index=True)

    return df_demanda

# %%
def demanda_ire_general(filtro_general, URL, HEADERS, start_date, end_date):
    
    filtro_general

    endpoint = f"{URL}/{filtro_demanda}"

    # Inicializamos un DataFrame vacío
    df_ire_general = pd.DataFrame()

    TIME_TRUNC = "month"


    for geo_id, region_name in region_ids.items():
        params = {
            "start_date": start_date.strftime("%Y-%m-%dT%H:%M"),
            "end_date": end_date.strftime("%Y-%m-%dT%H:%M"),
            "time_trunc": TIME_TRUNC,
            "geo_id": geo_id
        }

        response = requests.get(endpoint, headers=HEADERS, params=params)

        if response.status_code != 200:
            print(f"Error {response.status_code} para región: {region_name} ({geo_id})")
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
def demanda_ire_industria(filtro_industria, URL, HEADERS, start_date, end_date):

    filtro_industria

    endpoint = f"{URL}/{filtro_demanda}"

    # Inicializamos un DataFrame vacío
    df_ire_industria = pd.DataFrame()

    TIME_TRUNC = "month"

    for geo_id, region_name in region_ids.items():
        params = {
            "start_date": start_date.strftime("%Y-%m-%dT%H:%M"),
            "end_date": end_date.strftime("%Y-%m-%dT%H:%M"),
            "time_trunc": TIME_TRUNC,
            "geo_id": geo_id
        }

        response = requests.get(endpoint, headers=HEADERS, params=params)

        if response.status_code != 200:
                print(f"Error {response.status_code} para región: {region_name} ({geo_id})")
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

        df_ire_industria_year = pd.DataFrame(registros)
        df_ire_industria = pd.concat([df_ire_industria, df_ire_industria_year], ignore_index=True)

    return df_ire_industria

# %%
def demanda_ire_servicios(filtro_servicios, URL, HEADERS, start_date, end_date):

    filtro_servicios

    endpoint = f"{URL}/{filtro_demanda}"

    # Inicializamos un DataFrame vacío
    df_ire_servicios = pd.DataFrame()

    TIME_TRUNC = "month"

    for geo_id, region_name in region_ids.items():
        params = {
            "start_date": start_date.strftime("%Y-%m-%dT%H:%M"),
            "end_date": end_date.strftime("%Y-%m-%dT%H:%M"),
            "time_trunc": TIME_TRUNC,
            "geo_id": geo_id
        }

        response = requests.get(endpoint, headers=HEADERS, params=params)

        if response.status_code != 200:
            print(f"Error {response.status_code} para región: {region_name} ({geo_id})")
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

        df_ire_servicios_year = pd.DataFrame(registros)
        df_ire_servicios = pd.concat([df_ire_servicios, df_ire_servicios_year], ignore_index=True)

    return df_ire_servicios

# %%
def generacion(filtro_generacion, URL, HEADERS, start_date, end_date):

    filtro_generacion

    endpoint = f"{URL}{filtro_generacion}"

    df_generacion = pd.DataFrame()

    TIME_TRUNC = "day"

    for geo_id, region_name in region_ids.items():
        params = {
        "start_date": start_date.strftime("%Y-%m-%dT%H:%M"),
        "end_date": end_date.strftime("%Y-%m-%dT%H:%M"),
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
                                })

                    df_generacion_year = pd.DataFrame(registros)
                    df_generacion = pd.concat([df_generacion, df_generacion_year], ignore_index=True)

            except Exception as e:
                print("Contenido de la respuesta:", response.text)

        else:
            print(f"Error en la solicitud para {region_name}. Código: {response.status_code}")

    return df_generacion

# %%
def renov_norenov(filtro_renovable, URL, HEADERS, start_date, end_date):

    filtro_renovable

    endpoint = f"{URL}{filtro_renovable}"

    df_renovable = pd.DataFrame()
    ## Iterar sobre los años
    # Iterar sobre los geo_ids y nombres de regiones
    # para cada año y geo_id
    for geo_id, region_name in region_ids.items():
        TIME_TRUNC = "day"

        params = {
            "start_date": start_date.strftime("%Y-%m-%dT%H:%M"),
            "end_date": end_date.strftime("%Y-%m-%dT%H:%M"),
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
                                })

                    df_renovable_year = pd.DataFrame(registros)
                    df_renovable = pd.concat([df_renovable, df_renovable_year], ignore_index=True)

            except Exception as e:
                print("Contenido de la respuesta:", response.text)

        else:
                print(f"Error en la solicitud para {region_name}. Código: {response.status_code}")

    return df_renovable

# %%
def fronteras(URL, HEADERS, start_date, end_date):

    # Lista de países
    lista_paises = ['francia-frontera', 'portugal-frontera', 'marruecos-frontera', 'andorra-frontera']

    datos_intercambios = []

    for pais in lista_paises:
        # Endpoint para intercambios
        filtro_intercambio = f"/es/datos/intercambios/{pais}"
        endpoint = f"{URL}{filtro_intercambio}"
        TIME_TRUNC = "day"

        params = {
        "start_date": start_date.strftime("%Y-%m-%dT%H:%M"),
        "end_date": end_date.strftime("%Y-%m-%dT%H:%M"),
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
                datos_intercambios.append(df)
            else:
                print(f"Error en la solicitud para {pais}. Código: {response.status_code}")

    # Unir todos los datos en un único DataFrame
    df_fronteras = pd.concat(datos_intercambios, ignore_index=True)

    return df_fronteras

# %%
def extraccion_update(start_date, end_date):
    """
    Función para extraer datos de la API de REE actualizados.
    """
    print('Extrayendo datos actualizados del Balance Eléctrico...')
    df_balance = Balance_electrico(filtro_balance, URL, HEADERS, start_date, end_date)
    
    print('Extrayendo datos actualizados de la Demanda Eléctrica...')
    df_demanda = demanda_evolucion(filtro_demanda, URL, HEADERS, start_date, end_date)
    print('Extrayendo datos actualizados de la IRE General...')
    df_ire_general = demanda_ire_general(filtro_general, URL, HEADERS, start_date, end_date)
    print('Extrayendo datos actualizados de la IRE Industria...')
    df_ire_industria = demanda_ire_industria(filtro_industria, URL, HEADERS, start_date, end_date)
    print('Extrayendo datos actualizados de la IRE Servicios...')
    df_ire_servicios = demanda_ire_servicios(filtro_servicios, URL, HEADERS, start_date, end_date)

    print('Extrayendo datos actualizados de la Generación Eléctrica...')
    df_generacion = generacion(filtro_generacion, URL, HEADERS, start_date, end_date)
    print('Extrayendo datos actualizados de la Generación Renovable y No Renovable...')
    df_renovable = renov_norenov(filtro_renovable, URL, HEADERS, start_date, end_date)

    print('Extrayendo datos actualizados de los intercambios entre países...')
    df_fronteras = fronteras(URL, HEADERS, start_date, end_date)

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