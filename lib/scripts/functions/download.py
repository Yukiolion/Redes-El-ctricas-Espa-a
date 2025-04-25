# %%
import pandas as pd
import mysql.connector

# %%
def download_balance(conn):
    print('Iniciando descarga...')
    cursor = conn.cursor()
    ### BALANCE ###
    query = "SELECT * FROM balance ORDER BY fecha DESC"
    cursor.execute(query)
    datos_balance = cursor.fetchall()
    cursor.execute(query)
    resultados = cursor.fetchall()

    df = pd.DataFrame(resultados)

    print('Datos descargados.')

    return df

# %%
def download_demanda(conn):
    print('Iniciando descarga...')
    cursor = conn.cursor()
    ### DEMANDA ###
    query = "SELECT * FROM demanda_evolucion ORDER BY fecha DESC"
    cursor.execute(query)
    datos_demanda_evolucion = cursor.fetchall()

    df = pd.DataFrame(datos_demanda_evolucion)

    print('Datos descargados.')

    return df

# %%
def download_ire(conn):
    print('Iniciando descarga...')
    cursor = conn.cursor()
    ### IRE ###
    query = "SELECT * FROM demanda_ire_general ORDER BY fecha DESC"
    cursor.execute(query)
    datos_ire_general = cursor.fetchall()

    df = pd.DataFrame(datos_ire_general)

    print('Datos descargados.')

    return df

# %%
def download_generacion(conn):
    print('Iniciando descarga...')
    cursor = conn.cursor()
    ### GENERACION ###
    query = "SELECT * FROM estructura_generacion ORDER BY fecha DESC"
    cursor.execute(query)
    datos_estructura = cursor.fetchall()

    df = pd.DataFrame(datos_estructura)

    print('Datos descargados.')

    return df

# %%
def download_intercambio(conn):
    print('Iniciando descarga...')
    cursor = conn.Cursor()
    ### INTERCAMBIO ###
    query = "SELECT * FROM fronteras ORDER BY fecha DESC"
    cursor.execute(query)
    datos_fronteras = cursor.fetchall()

    df = pd.DataFrame(datos_fronteras)

    print('Datos descargados.')

    return df


