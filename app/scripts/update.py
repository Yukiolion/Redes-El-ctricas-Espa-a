import requests
import pandas as pd
import numpy as np
from pprint import pprint
from datetime import datetime

from scripts.db_connect import db_connect
from scripts.download import download_balance, download_demanda, download_generacion, download_intercambio, download_ire

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
def Balance_electrico(filtro_balance, URL, HEADERS, today, last_db_date):
    # Verificación de tipo de fechas
    if isinstance(today, str):
        today = datetime.fromisoformat(today)
    if isinstance(last_db_date, str):
        last_db_date = datetime.fromisoformat(last_db_date)

    if last_db_date >= today.date():
        print("Los datos ya están actualizados.")
        return pd.DataFrame()  # O puedes retornar None o df vacío si prefieres

    print("Actualizando datos desde base de datos hasta hoy...")

    endpoint = f"{URL}/{filtro_balance}"
    df_balance = pd.DataFrame()

    start_year = last_db_date.year
    end_year = today.year

    for year in range(start_year, end_year + 1):
        # Establecer rango de fechas
        if year == start_year:
            start_date = last_db_date.strftime("%Y-%m-%dT%H:%M")
        else:
            start_date = f"{year}-01-01T00:00"

        if year == end_year:
            end_date = today.strftime("%Y-%m-%dT%H:%M")
        else:
            end_date = f"{year}-12-31T23:59"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": "day",
                "geo_id": geo_id
            }

            response = requests.get(endpoint, headers=HEADERS, params=params)
            if response.status_code != 200:
                print(f"Error al obtener datos para {region_name} en {year}")
                continue

            data = response.json()
            included = data.get('included', [])

            registros = []
            for grupo in included:
                group_name = grupo['attributes']['title']
                contenidos = grupo['attributes'].get('content', [])

                for item in contenidos:
                    indicador = item['attributes']['title']
                    valores = item['attributes'].get('values', [])

                    for punto in valores:
                        registros.append({
                            'fecha': punto['datetime'],
                            'valor': punto['value'],
                            'tipo': indicador,
                            'energia': group_name,
                            'region': region_name,
                        })

            df_balance_year = pd.DataFrame(registros)
            df_balance = pd.concat([df_balance, df_balance_year], ignore_index=True)

    print("Actualización completada.")
    return df_balance

# %%
def demanda_evolucion(filtro_demanda, URL, HEADERS, today, last_db_date):
# Verificación de tipo de fechas
    if isinstance(today, str):
        today = datetime.fromisoformat(today)
    if isinstance(last_db_date, str):
        last_db_date = datetime.fromisoformat(last_db_date)

    if last_db_date >= today.date():
        print("Los datos ya están actualizados.")
        return pd.DataFrame()  # O puedes retornar None o df vacío si prefieres

    print("Actualizando datos desde base de datos hasta hoy...")

    endpoint = f"{URL}/{filtro_demanda}"
    df_demanda = pd.DataFrame()

    start_year = last_db_date.year
    end_year = today.year

    for year in range(start_year, end_year + 1):
        # Establecer rango de fechas
        if year == start_year:
            start_date = last_db_date.strftime("%Y-%m-%dT%H:%M")
        else:
            start_date = f"{year}-01-01T00:00"

        if year == end_year:
            end_date = today.strftime("%Y-%m-%dT%H:%M")
        else:
            end_date = f"{year}-12-31T23:59"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": "month",
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
def demanda_ire_general(filtro_general, URL, HEADERS, today, last_db_date):
    # Verificación de tipo de fechas
    if isinstance(today, str):
        today = datetime.fromisoformat(today)
    if isinstance(last_db_date, str):
        last_db_date = datetime.fromisoformat(last_db_date)

    if last_db_date >= today.date():
        print("Los datos ya están actualizados.")
        return pd.DataFrame()  # O puedes retornar None o df vacío si prefieres

    print("Actualizando datos desde base de datos hasta hoy...")

    endpoint = f"{URL}/{filtro_general}"
    df_ire_general = pd.DataFrame()

    start_year = last_db_date.year
    end_year = today.year

    for year in range(start_year, end_year + 1):
        # Establecer rango de fechas
        if year == start_year:
            start_date = last_db_date.strftime("%Y-%m-%dT%H:%M")
        else:
            start_date = f"{year}-01-01T00:00"

        if year == end_year:
            end_date = today.strftime("%Y-%m-%dT%H:%M")
        else:
            end_date = f"{year}-12-31T23:59"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": "month",
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
def demanda_ire_industria(filtro_industria, URL, HEADERS, today, last_db_date):

    # Verificación de tipo de fechas
    if isinstance(today, str):
        today = datetime.fromisoformat(today)
    if isinstance(last_db_date, str):
        last_db_date = datetime.fromisoformat(last_db_date)

    if last_db_date >= today.date():
        print("Los datos ya están actualizados.")
        return pd.DataFrame()  # O puedes retornar None o df vacío si prefieres

    print("Actualizando datos desde base de datos hasta hoy...")

    endpoint = f"{URL}/{filtro_industria}"
    df_ire_industria = pd.DataFrame()

    start_year = last_db_date.year
    end_year = today.year

    for year in range(start_year, end_year + 1):
        # Establecer rango de fechas
        if year == start_year:
            start_date = last_db_date.strftime("%Y-%m-%dT%H:%M")
        else:
            start_date = f"{year}-01-01T00:00"

        if year == end_year:
            end_date = today.strftime("%Y-%m-%dT%H:%M")
        else:
            end_date = f"{year}-12-31T23:59"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": "month",
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

            df_ire_industria_year = pd.DataFrame(registros)
            df_ire_industria = pd.concat([df_ire_industria, df_ire_industria_year], ignore_index=True)

    return df_ire_industria

# %%
def demanda_ire_servicios(filtro_servicios, URL, HEADERS, today, last_db_date):

    # Verificación de tipo de fechas
    if isinstance(today, str):
        today = datetime.fromisoformat(today)
    if isinstance(last_db_date, str):
        last_db_date = datetime.fromisoformat(last_db_date)

    if last_db_date >= today.date():
        print("Los datos ya están actualizados.")
        return pd.DataFrame()  # O puedes retornar None o df vacío si prefieres

    print("Actualizando datos desde base de datos hasta hoy...")

    endpoint = f"{URL}/{filtro_servicios}"
    df_ire_servicios = pd.DataFrame()

    start_year = last_db_date.year
    end_year = today.year

    for year in range(start_year, end_year + 1):
        # Establecer rango de fechas
        if year == start_year:
            start_date = last_db_date.strftime("%Y-%m-%dT%H:%M")
        else:
            start_date = f"{year}-01-01T00:00"

        if year == end_year:
            end_date = today.strftime("%Y-%m-%dT%H:%M")
        else:
            end_date = f"{year}-12-31T23:59"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": "month",
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

            df_ire_servicios_year = pd.DataFrame(registros)
            df_ire_servicios = pd.concat([df_ire_servicios, df_ire_servicios_year], ignore_index=True)

    return df_ire_servicios

# %%
def generacion(filtro_generacion, URL, HEADERS, today, last_db_date):

    # Verificación de tipo de fechas
    if isinstance(today, str):
        today = datetime.fromisoformat(today)
    if isinstance(last_db_date, str):
        last_db_date = datetime.fromisoformat(last_db_date)

    if last_db_date >= today.date():
        print("Los datos ya están actualizados.")
        return pd.DataFrame()  # O puedes retornar None o df vacío si prefieres

    print("Actualizando datos desde base de datos hasta hoy...")

    endpoint = f"{URL}/{filtro_generacion}"
    df_generacion = pd.DataFrame()

    start_year = last_db_date.year
    end_year = today.year

    for year in range(start_year, end_year + 1):
        # Establecer rango de fechas
        if year == start_year:
            start_date = last_db_date.strftime("%Y-%m-%dT%H:%M")
        else:
            start_date = f"{year}-01-01T00:00"

        if year == end_year:
            end_date = today.strftime("%Y-%m-%dT%H:%M")
        else:
            end_date = f"{year}-12-31T23:59"

        for geo_id, region_name in region_ids.items():
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "time_trunc": "day",
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
                print(f"Error en la solicitud para {region_name} {year}. Código: {response.status_code}")

    return df_generacion

# %%
def fronteras(URL, HEADERS, today, last_db_date):

    # Lista de países
    lista_paises = ['francia-frontera', 'portugal-frontera', 'marruecos-frontera', 'andorra-frontera']

    datos_intercambios = []

    for pais in lista_paises:
        # Endpoint para intercambios
        # Verificación de tipo de fechas
        if isinstance(today, str):
            today = datetime.fromisoformat(today)
        if isinstance(last_db_date, str):
            last_db_date = datetime.fromisoformat(last_db_date)

        if last_db_date >= today.date():
            print("Los datos ya están actualizados.")
            return pd.DataFrame()  # O puedes retornar None o df vacío si prefieres

        print("Actualizando datos desde base de datos hasta hoy...")
        
        filtro_intercambio = f"/es/datos/intercambios/{pais}"
        endpoint = f"{URL}{filtro_intercambio}"
        # Iterar sobre los años y extraer datos de cada año
        # y cada país para el año 2015 al 2025

        start_year = last_db_date.year
        end_year = today.year

        for year in range(start_year, end_year + 1):
            # Establecer rango de fechas
            if year == start_year:
                start_date = last_db_date.strftime("%Y-%m-%dT%H:%M")
            else:
                start_date = f"{year}-01-01T00:00"

            if year == end_year:
                end_date = today.strftime("%Y-%m-%dT%H:%M")
            else:
                end_date = f"{year}-12-31T23:59"

            for geo_id, region_name in region_ids.items():
                params = {
                    "start_date": start_date,
                    "end_date": end_date,
                    "time_trunc": "day",
                    "geo_id": geo_id
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
                print(f"Error en la solicitud para {pais} en {year}. Código: {response.status_code}")

    # Unir todos los datos en un único DataFrame
    df_fronteras = pd.concat(datos_intercambios, ignore_index=True)

    return df_fronteras

# %%
def extraccion():

    conn = db_connect()

    df_database_balance = download_balance(conn)
    df_database_demanda = download_demanda(conn)
    df_database_generacion = download_generacion(conn)
    df_database_intercambio = download_intercambio(conn)
    df_database_ire = download_ire(conn)

    last_date_balance = df_database_balance['fecha'].max()
    last_date_demanda = df_database_demanda['fecha'].max()
    last_date_generacion = df_database_generacion['fecha'].max()
    last_date_intercambio = df_database_intercambio['fecha'].max()
    last_date_ire = df_database_ire['fecha'].max()


    today = datetime.now()
    

    # Función para extraer datos de la API de REE.
    print('Extrayendo datos del Balance Eléctrico...')
    df_balance = Balance_electrico(filtro_balance, URL, HEADERS, today, last_date_balance)
    
    print('Extrayendo datos de la Demanda Eléctrica...')
    df_demanda = demanda_evolucion(filtro_demanda, URL, HEADERS, today, last_date_demanda)
    print('Extrayendo datos de la IRE General...')
    df_ire_general = demanda_ire_general(filtro_general, URL, HEADERS, today, last_date_ire)
    print('Extrayendo datos de la IRE Industria...')
    df_ire_industria = demanda_ire_industria(filtro_industria, URL, HEADERS, today, last_date_ire)
    print('Extrayendo datos de la IRE Servicios...')
    df_ire_servicios = demanda_ire_servicios(filtro_servicios, URL, HEADERS, today, last_date_ire)

    print('Extrayendo datos de la Generación Eléctrica...')
    df_generacion = generacion(filtro_generacion, URL, HEADERS, today, last_date_generacion)

    print('Extrayendo datos de los intercambios entre países...')
    df_fronteras = fronteras(URL, HEADERS, today, last_date_intercambio)

    return {
        "balance": df_balance,
        "demanda": df_demanda,
        "ire_general": df_ire_general,
        "ire_industria": df_ire_industria,
        "ire_servicios": df_ire_servicios,
        "generacion": df_generacion,
        "fronteras": df_fronteras,
    }

# %% [markdown]
# ** LIMPIEZA DE DATOS **

# %%
def limpieza_balance(df_balance):
    # Cambiamos el formato de fecha y en valor, trabajamos con MWh ya que se ven mejor

    df_balance['fecha'] = pd.to_datetime(df_balance['fecha'].str.split('T').str[0])
    df_balance['valor'] = df_balance['valor']/1e3

    # La columna de las regiones parece que está repitiendo los datos, con lo que eliminamos los duplicados que haya en 
    # el resto de columnas sin tener en cuenta esa

    df_balance_sin_duplicados = df_balance.drop_duplicates(subset=['fecha', 'valor', 'tipo', 'energia'])

    return df_balance_sin_duplicados

# %%
def limpieza_demanda(df1_demanda, df2_demanda, df3_demanda, df4_demanda):

    df1_demanda['fecha'] = pd.to_datetime(df1_demanda['fecha'].astype(str).str.split('T').str[0])
    df2_demanda['fecha'] = pd.to_datetime(df2_demanda['fecha'].astype(str).str.split('T').str[0])
    df3_demanda['fecha'] = pd.to_datetime(df3_demanda['fecha'].astype(str).str.split('T').str[0])
    df4_demanda['fecha'] = pd.to_datetime(df4_demanda['fecha'].astype(str).str.split('T').str[0])

    print(df1_demanda.info())

    df1_demanda['valor'] = df1_demanda['valor']/1e3

    df1_demanda_sin_duplicados = df1_demanda.drop_duplicates(subset=['fecha', 'valor', 'indicador'])
    df2_demanda_sin_duplicados = df2_demanda.drop_duplicates(subset=['fecha', 'valor', 'porcentaje', 'indicador'])
    df3_demanda_sin_duplicados = df3_demanda.drop_duplicates(subset=['fecha', 'valor', 'porcentaje', 'indicador'])
    df4_demanda_sin_duplicados = df4_demanda.drop_duplicates(subset=['fecha', 'valor', 'porcentaje', 'indicador'])
    
    df_ire = pd.concat([df2_demanda_sin_duplicados, df3_demanda_sin_duplicados, df4_demanda_sin_duplicados], ignore_index=True)

    df_ire = df_ire[~df_ire['indicador'].isin(['Variación mensual corregida', 'Variación mensual'])]
    # Asegurar orden por fecha
    df1_demanda.sort_values('fecha', inplace=True)
    df_ire.sort_values('fecha', inplace=True)

    return df1_demanda, df_ire

# %%
def limpieza_generacion(df_generacion):
    # Cambiamos el formato de fecha (nos quedamos con YYYY-MM-DD)
    df_generacion['fecha'] = pd.to_datetime(df_generacion['fecha'].str.split('T').str[0])

    # Convertimos Wh a MWh
    df_generacion['valor'] = df_generacion['valor'] / 1e3

    # Quitamos las filas con tipo 'Generación total'
    df_generacion = df_generacion[df_generacion['tipo'] != 'Generación total']

    # Eliminamos duplicados ignorando la columna 'region'
    df_generacion_sin_duplicados = df_generacion.drop_duplicates(
        subset=['fecha', 'valor', 'porcentaje', 'indicador', 'tipo']
    )

    return df_generacion_sin_duplicados

# %%
def limpieza_fronteras(df_fronteras):
    # Cambiamos el formato de fecha y en valor, trabajamos con kWh ya que se ven mejor

    df_fronteras['datetime'] = pd.to_datetime(df_fronteras['datetime'].str.split('T').str[0])
    df_fronteras['value'] = df_fronteras['value']/1e3

    # Cambiamos los nombres de las columnas que se entiende mejor

    df_fronteras.rename(columns={
        'datetime': 'fecha',
        'value': 'valor',
        'percentage': 'porcentaje'}, inplace=True)
    
    #Quitamos duplicados:
    df_fronteras = df_fronteras.drop_duplicates(
        subset=['fecha', 'pais', 'valor', 'porcentaje']
    )

    return df_fronteras

# %%
def limpieza(df_balance, df_demanda, df_ire_general, df_ire_industria, df_ire_servicios, df_generacion, df_fronteras):
    df_balance_limpio = limpieza_balance(df_balance)
    df_demanda_limpia, df_ire_limpia = limpieza_demanda(df_demanda, df_ire_general, df_ire_industria, df_ire_servicios)
    df_generacion_limpia = limpieza_generacion(df_generacion)
    df_fronteras_limpias = limpieza_fronteras(df_fronteras)

    return {
        "balance": df_balance_limpio,
        "demanda": df_demanda_limpia,
        "ire_general": df_ire_limpia,
        "generacion": df_generacion_limpia,
        "fronteras": df_fronteras_limpias
    }

# %% [markdown]
# CARGAR A LA BASE DE DATOS

# %%
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

db_host = os.getenv("DATABASE_HOST")
db_user = os.getenv("DATABASE_USER")
db_psw = os.getenv("DATABASE_PASSWORD")
db_name = os.getenv("DATABASE_NAME")

def db_connect():
    # Conexión MySQL
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_psw,
        database=db_name
    )

    return conn

# %%
def carga_balance(df_balance_limpio):
    print("Cargando datos en la base de datos...")
    conn = db_connect()
    cursor = conn.cursor()

    nuevo_balance = ['fecha', 'tipo', 'energia', 'region', 'valor']
    df_balance_limpio = df_balance_limpio[nuevo_balance]

    # Dividir el dataframe en lotes
    batch_size = 2000
    num_batches = len(df_balance_limpio) // batch_size + 1

    for i in range(num_batches):
        batch = df_balance_limpio.iloc[i * batch_size: (i + 1) * batch_size]

        # Crear los datos para el lote
        data_batch = [tuple(row) for row in batch.to_numpy()]

        cursor.executemany("""
            INSERT IGNORE INTO balance (fecha, tipo, energia, region, valor)
            VALUES (%s, %s, %s, %s, %s)
        """, data_batch)

        conn.commit()

    cursor.close()
    conn.close()

    return True

# %%
def carga_ire(df_ire_limpio):
    print("Cargando datos en la base de datos...")
    conn = db_connect()
    cursor = conn.cursor()

    nuevo_ire = ['fecha', 'indicador', 'region', 'valor', 'porcentaje']
    df_ire_limpio = df_ire_limpio[nuevo_ire]

    df_ire_limpio.head()

    for _, row in df_ire_limpio.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO demanda_ire_general (fecha, indicador, region, valor, porcentaje)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['fecha'], row['indicador'], row['region'], row['valor'], row['porcentaje']))

        conn.commit()

    cursor.close()
    conn.close()

    return True

# %%
def carga_demanda(df_demanda_limpio):
    print("Cargando datos en la base de datos...")
    conn = db_connect()
    cursor = conn.cursor()

    nuevo_demanda = ['fecha', 'indicador', 'region', 'valor']
    df_demanda_limpio = df_demanda_limpio[nuevo_demanda]
    
    # Dividir el DataFrame en lotes
    batch_size = 1000  # Puedes ajustar este tamaño según lo que sea más eficiente para tu base de datos
    num_batches = len(df_demanda_limpio) // batch_size + 1

    for i in range(num_batches):
        # Extraer un lote de datos
        batch = df_demanda_limpio.iloc[i * batch_size: (i + 1) * batch_size]
        
        # Crear los datos para el batch
        data_batch = [tuple(row) for row in batch.to_numpy()]

        # Usar executemany() para insertar el lote de datos
        cursor.executemany("""
            INSERT IGNORE INTO demanda_evolucion (fecha, indicador, region, valor)
            VALUES (%s, %s, %s, %s)
        """, data_batch)

        # Confirmar la inserción del lote
        conn.commit()

    cursor.close()
    conn.close()

    print("Carga de datos completada.")
    return True

# %%
def carga_fronteras(df_fronteras_limpio):
    print("Cargando datos en la base de datos...")
    conn = db_connect()
    cursor = conn.cursor()

    nuevo_fronteras = ['fecha', 'pais', 'valor', 'porcentaje']
    df_fronteras_limpio = df_fronteras_limpio[nuevo_fronteras]
    df_fronteras_limpio.head()

    for _, row in df_fronteras_limpio.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO fronteras (fecha, pais, valor, porcentaje)
            VALUES (%s, %s, %s, %s)
        """, (row['fecha'], row['pais'], row['valor'], row['porcentaje']))

        conn.commit()
    cursor.close()
    conn.close()

    return True

# %%
def carga_generacion(df_generacion_limpio):
    print("Cargando datos en la base de datos...")
    conn = db_connect()
    cursor = conn.cursor()

    nuevo_estructura = ['fecha', 'indicador', 'region', 'tipo', 'valor', 'porcentaje']
    df_generacion_limpio = df_generacion_limpio[nuevo_estructura]
    df_generacion_limpio.head()

    for _, row in df_generacion_limpio.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO estructura_generacion (fecha, indicador, region, tipo, valor, porcentaje)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['fecha'], row['indicador'], row['region'], row['tipo'], row['valor'], row['porcentaje']))

        conn.commit()

    cursor.close()
    conn.close()

    return True

# %%
def update():

    # EXTRACCION
    dataframes = extraccion()  # Tarda aprox 17 minutos en hacer toda la extraccion de todos los datos

    # LIMPIEZA
    df_balance = dataframes['balance']

    df_demanda = dataframes['demanda']
    df_ire_general = dataframes['ire_general']
    df_ire_industria = dataframes['ire_industria']
    df_ire_servicios = dataframes['ire_servicios']

    df_generacion = dataframes['generacion']

    df_fronteras = dataframes['fronteras']


    dataframes_clean = limpieza(df_balance, df_demanda, df_ire_general, df_ire_industria, df_ire_servicios, df_generacion, df_fronteras)

    df_balance_limpio = dataframes_clean['balance']

    df_demanda_limpio = dataframes_clean['demanda']
    df_ire_limpio = dataframes_clean['ire_general']


    df_generacion_limpio = dataframes_clean['generacion']

    df_fronteras_limpio = dataframes_clean['fronteras']

    balance_new_data = carga_balance(df_balance_limpio)
    if balance_new_data == True:
        print("Carga de datos completada.")
    else:
        print("Error en la carga de datos.")
        print("Carga de datos fallida.")

    ire_new_data = carga_ire(df_ire_limpio)
    if ire_new_data == True:
        print("Carga de datos completada.")
    else:
        print("Error en la carga de datos.")
        print("Carga de datos fallida.")

    demanda_new_data = carga_demanda(df_demanda_limpio)
    if demanda_new_data == True:
        print("Carga de datos completada.")
    else:
        print("Error en la carga de datos.")
        print("Carga de datos fallida.")

    fronteras_new_data = carga_fronteras(df_fronteras_limpio)
    if fronteras_new_data == True:
        print("Carga de datos completada.")
    else:
        print("Error en la carga de datos.")
        print("Carga de datos fallida.")

    generacion_new_data = carga_generacion(df_generacion_limpio)
    if generacion_new_data == True:
        print("Carga de datos completada.")
    else:
        print("Error en la carga de datos.")
        print("Carga de datos fallida.")

    return True