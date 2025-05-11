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


#%%
# Creamos Funciones para descargar los datos de la API de REE
# %%
def Balance_electrico(filtro_balance, URL, HEADERS, today, last_db_date):
    # Verificación de tipo de fechas
    if isinstance(today, str):
        today = datetime.fromisoformat(today)
    if isinstance(last_db_date, str):
        last_db_date = datetime.fromisoformat(last_db_date)

    if last_db_date >= today.date():
        print("Los datos ya están actualizados.")
        return pd.DataFrame()

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
        return pd.DataFrame()

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
        return pd.DataFrame()

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
        return pd.DataFrame()

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
        return pd.DataFrame()

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
        return pd.DataFrame()

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
# Creamos una funcion general que ejecute todas las funciones de extraccion
# obteninedo la ultima fecha de la base de datos y la fecha actual para decidir si se
# realiza la extraccion o los datos ya estan actualizados
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
def limpieza_balance(df):
    df_balance = df.copy()
    # Cambiamos el formato de fecha y en valor, trabajamos con MWh ya que se ven mejor
    df_balance['fecha'] = pd.to_datetime(df_balance['fecha'].astype(str).str.split('T').str[0])
    df_balance['valor'] = df_balance['valor']/1000

    # La columna de las regiones parece que está repitiendo los datos, con lo que eliminamos los duplicados que haya en 
    # el resto de columnas sin tener en cuenta esa

    df_balance_sin_duplicados = df_balance.drop_duplicates(subset=['fecha', 'valor', 'tipo', 'energia'])

    return df_balance_sin_duplicados

# %%
def limpieza_demanda(df1_demanda, df2_demanda, df3_demanda, df4_demanda):
    # Limpieza segura de fechas y columnas, solo si los DataFrames no están vacíos
    if not df1_demanda.empty and 'fecha' in df1_demanda.columns:
        df1_demanda['fecha'] = pd.to_datetime(df1_demanda['fecha'].astype(str).str.split('T').str[0])
        df1_demanda['valor'] = df1_demanda['valor'] / 1e3
        df1_demanda_sin_duplicados = df1_demanda.drop_duplicates(subset=['fecha', 'valor', 'indicador'])
        df1_demanda = df1_demanda_sin_duplicados.sort_values('fecha')
    else:
        df1_demanda = pd.DataFrame()

    ire_dfs = []
    for df in [df2_demanda, df3_demanda, df4_demanda]:
        if not df.empty and 'fecha' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'].astype(str).str.split('T').str[0])
            df = df.drop_duplicates(subset=['fecha', 'valor', 'porcentaje', 'indicador'])
            ire_dfs.append(df)

    if ire_dfs:
        df_ire = pd.concat(ire_dfs, ignore_index=True)
        df_ire = df_ire[~df_ire['indicador'].isin(['Variación mensual corregida', 'Variación mensual'])]
        df_ire = df_ire.sort_values('fecha')
    else:
        df_ire = pd.DataFrame()

    return df1_demanda, df_ire

# %%
def limpieza_generacion(df):

    df_generacion = df.copy()
    # Cambiamos el formato de fecha (nos quedamos con YYYY-MM-DD)
    df_generacion['fecha'] = pd.to_datetime(df_generacion['fecha'].astype(str).str.split('T').str[0])

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
def limpieza_fronteras(df):
    # Cambiamos el formato de fecha y en valor, trabajamos con kWh ya que se ven mejor

    df_fronteras = df.copy()

    df_fronteras['datetime'] = pd.to_datetime(df_fronteras['datetime'].str.split('T').str[0])
    df_fronteras['value'] = df_fronteras['value']/1e3

    # Cambiamos los nombres de las columnas que se entiende mejor

    df_fronteras.rename(columns={
        'datetime': 'fecha',
        'value': 'valor',
        'percentage': 'porcentaje'}, inplace=True)

    #Quitamos duplicados:
    df_fronteras_limpio = df_fronteras.drop_duplicates(
        subset=['fecha', 'pais', 'valor', 'porcentaje']
    )

    return df_fronteras_limpio

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
    print("Cargando datos...")
    # Creamos la conexion a la base de datos a traves del script
    # db_connect() que establece la conexion con dicha BD
    conn = db_connect()
    cursor = conn.cursor()
    # Ordenamos el df para que las columnas tengan el mismo orden
    # que en la base de datos
    nuevo_balance = ['fecha', 'tipo', 'energia', 'region', 'valor']
    df_balance_limpio = df_balance_limpio[nuevo_balance]

    # Insertar los datos en la tabla balance
    for i, row in df_balance_limpio.iterrows():
        cursor.execute("""
            INSERT INTO balance (fecha, tipo, energia, region, valor)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE valor = VALUES(valor)
        """, (row['fecha'], row['tipo'], row['energia'], row['region'], row['valor']))
    
    # Confirmamos la carga
    conn.commit()

    # Cerramos el cursor y la conexión
    cursor.close()
    conn.close()

    return True

# %%
def carga_ire(df_ire_limpio):
    print("Cargando datos...")
    # Creamos la conexion a la base de datos a traves del script
    # db_connect() que establece la conexion con dicha BD
    conn = db_connect()
    cursor = conn.cursor()
    # Ordenamos el df para que las columnas tengan el mismo orden
    # que en la base de datos
    nuevo_ire = ['fecha', 'indicador', 'region', 'valor', 'porcentaje']
    df_ire_limpio = df_ire_limpio[nuevo_ire]

    # Aqui cargamos los datos fila por fila a diferencia del archivo anterior
    # debido a que hay una cantidad menor de datos que subir a la base de datos
    for _, row in df_ire_limpio.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO demanda_ire_general (fecha, indicador, region, valor, porcentaje)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['fecha'], row['indicador'], row['region'], row['valor'], row['porcentaje']))
    # Confirmamos la sentencia
    conn.commit()
    # Cerramos el cursor y la conexion con la base de datos
    cursor.close()
    conn.close()

    return True

# %%
def carga_demanda(df_demanda_limpio):
    print("Cargando datos...")
    # Creamos la conexion a la base de datos a traves del script
    # db_connect() que establece la conexion con dicha BD
    conn = db_connect()
    cursor = conn.cursor()
    # Ordenamos el df para que las columnas tengan el mismo orden
    # que en la base de datos
    nuevo_demanda = ['fecha', 'indicador', 'region', 'valor']
    df_demanda_limpio = df_demanda_limpio[nuevo_demanda]
    
    # Dividir el dataframe en lotes para que se suba a la base de datos
    # con mayor facilidad
    batch_size = 1000
    num_batches = len(df_demanda_limpio) // batch_size + 1

    for i in range(num_batches):
        batch = df_demanda_limpio.iloc[i * batch_size: (i + 1) * batch_size]
        data_batch = [tuple(row) for row in batch.to_numpy()]
        # Ejecutamos la sentencia SQL con executemany para cargar los lotes de datos
        cursor.executemany("""
            INSERT IGNORE INTO demanda_evolucion (fecha, indicador, region, valor)
            VALUES (%s, %s, %s, %s)
        """, data_batch)
    # Confirmar la sentencia
    conn.commit()
    # Cerramos el curson y la conexion a la BD
    cursor.close()
    conn.close()
    
    return True

# %%
def carga_fronteras(df_fronteras_limpio):
    print("Cargando datos...")
    # Creamos la conexion a la base de datos a traves del script
    # db_connect() que establece la conexion con dicha BD
    conn = db_connect()
    cursor = conn.cursor()
    # Ordenamos el df para que las columnas tengan el mismo orden
    # que en la base de datos
    nuevo_fronteras = ['fecha', 'pais', 'valor', 'porcentaje']
    df_fronteras_limpio = df_fronteras_limpio[nuevo_fronteras]
    df_fronteras_limpio.head()

    # Aqui cargamos los datos fila por fila debido a que hay 
    # una cantidad menor de datos que subir a la base de datos
    for _, row in df_fronteras_limpio.iterrows():
        # Ejecutamos la sentencia
        cursor.execute("""
            INSERT IGNORE INTO fronteras (fecha, pais, valor, porcentaje)
            VALUES (%s, %s, %s, %s)
        """, (row['fecha'], row['pais'], row['valor'], row['porcentaje']))
    # Confirmamos la carga
    conn.commit()
    # Cerramos el cursor y la conexion con la BD
    cursor.close()
    conn.close()

    return True

# %%
def carga_generacion(df_generacion_limpio):
    print("Cargando datos...")
    # Creamos la conexion a la base de datos a traves del script
    # db_connect() que establece la conexion con dicha BD
    conn = db_connect()
    cursor = conn.cursor()
    # Ordenamos el df para que las columnas tengan el mismo orden
    # que en la base de datos
    nuevo_estructura = ['fecha', 'indicador', 'region', 'tipo', 'valor', 'porcentaje']
    df_generacion_limpio = df_generacion_limpio[nuevo_estructura]
    # Aqui cargamos los datos fila por fila debido a que hay 
    # una cantidad menor de datos que subir a la base de datos
    for _, row in df_generacion_limpio.iterrows():
        # Ejecutamos la sentencia
        cursor.execute("""
            INSERT IGNORE INTO estructura_generacion (fecha, indicador, region, tipo, valor, porcentaje)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['fecha'], row['indicador'], row['region'], row['tipo'], row['valor'], row['porcentaje']))
    # Confirmamos la carga
    conn.commit()
    # Cerramos el cursor y la conexion con la BD
    cursor.close()
    conn.close()

    return True

# %%
# Esta seria la funcion final, que ejecuta la funcion maestra de extraccion, las funciones de limpieza y finalmente
# las funciones de carga a la base de datos
def update():
    # EXTRACCIÓN
    dataframes = extraccion()

    # Copias individuales
    df_balance = dataframes['balance'].copy()
    df_demanda = dataframes['demanda'].copy()
    df_ire_general = dataframes['ire_general'].copy()
    df_ire_industria = dataframes['ire_industria'].copy()
    df_ire_servicios = dataframes['ire_servicios'].copy()
    df_generacion = dataframes['generacion'].copy()
    df_fronteras = dataframes['fronteras'].copy()

    print("Columnas de df_balance:", df_balance.columns)

    # LIMPIEZA
    dataframes_clean = {}

    if not df_balance.empty:
        dataframes_clean['balance'] = limpieza_balance(df_balance)
    else:
        print("df_balance está vacío, se omite limpieza.")
        dataframes_clean['balance'] = df_balance

    if not (df_demanda.empty and df_ire_general.empty and df_ire_industria.empty and df_ire_servicios.empty):
        df_demanda_limpio, df_ire_limpio = limpieza_demanda(df_demanda, df_ire_general, df_ire_industria, df_ire_servicios)
        dataframes_clean['demanda'] = df_demanda_limpio
        dataframes_clean['ire_general'] = df_ire_limpio
    else:
        print("Todos los DataFrames de demanda e IRE están vacíos, se omite limpieza.")
        dataframes_clean['demanda'] = pd.DataFrame()
        dataframes_clean['ire_general'] = pd.DataFrame()
        

    if not df_generacion.empty:
        dataframes_clean['generacion'] = limpieza_generacion(df_generacion)
    else:
        print("df_generacion está vacío, se omite limpieza.")
        dataframes_clean['generacion'] = df_generacion

    if not df_fronteras.empty:
        dataframes_clean['fronteras'] = limpieza_fronteras(df_fronteras)
    else:
        print("df_fronteras está vacío, se omite limpieza.")
        dataframes_clean['fronteras'] = df_fronteras

    # CARGA
    if not dataframes_clean['balance'].empty and carga_balance(dataframes_clean['balance']):
        print("Carga de balance completada.")
    elif dataframes_clean['balance'].empty:
        print("Balance ya actualizado.")
    else:
        print("Error en la carga de balance.")

    if not dataframes_clean['ire_general'].empty and carga_ire(dataframes_clean['ire_general']):
        print("Carga de IRE completada.")
    elif dataframes_clean['ire_general'].empty:
        print("IRE ya actualizado.")
    else:
        print("Error en la carga de IRE.")

    if not dataframes_clean['demanda'].empty and carga_demanda(dataframes_clean['demanda']):
        print("Carga de demanda completada.")
    elif dataframes_clean['demanda'].empty:
        print("Demanda ya actualizada.")
    else:
        print("Error en la carga de demanda.")

    if not dataframes_clean['fronteras'].empty and carga_fronteras(dataframes_clean['fronteras']):
        print("Carga de fronteras completada.")
    elif dataframes_clean['fronteras'].empty:
        print("Fronteras ya actualizadas.")
    else:
        print("Error en la carga de fronteras.")

    if not dataframes_clean['generacion'].empty and carga_generacion(dataframes_clean['generacion']):
        print("Carga de generación completada.")
    elif dataframes_clean['generacion'].empty:
        print("Generación ya actualizada.")
    else:
        print("Error en la carga de generación.")

    return True