import pandas as pd

# %%
def download_balance(conn):
    print('Iniciando descarga...')
    cursor = conn.cursor()
    ### BALANCE ###
    query = "SELECT * FROM balance ORDER BY fecha DESC"
    cursor.execute(query)
    
    # Obtener nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]

    # Obtener los datos
    resultados = cursor.fetchall()

    # Crear el DataFrame con los nombres de las columnas
    df = pd.DataFrame(resultados, columns=columnas)

    print('Datos descargados.')

    return df

# %%
def download_demanda(conn):
    print('Iniciando descarga...')
    cursor = conn.cursor()
    ### DEMANDA ###
    query = "SELECT * FROM demanda_evolucion ORDER BY fecha DESC"
    cursor.execute(query)
    
    # Obtener nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]

    # Obtener los datos
    datos_demanda_evolucion = cursor.fetchall()

    # Crear el DataFrame con los nombres de las columnas
    df = pd.DataFrame(datos_demanda_evolucion, columns=columnas)

    print('Datos descargados.')

    return df

# %%
def download_ire(conn):
    print('Iniciando descarga...')
    cursor = conn.cursor()
    ### IRE ###
    query = "SELECT * FROM demanda_ire_general ORDER BY fecha DESC"
    cursor.execute(query)
    
    # Obtener nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]

    # Obtener los datos
    datos_ire_general = cursor.fetchall()

    # Crear el DataFrame con los nombres de las columnas
    df = pd.DataFrame(datos_ire_general, columns=columnas)

    print('Datos descargados.')

    return df

# %%
def download_generacion(conn):
    print('Iniciando descarga...')
    cursor = conn.cursor()
    ### GENERACION ###
    query = "SELECT * FROM estructura_generacion ORDER BY fecha DESC"
    cursor.execute(query)
    
    # Obtener nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]

    # Obtener los datos
    datos_estructura = cursor.fetchall()

    # Crear el DataFrame con los nombres de las columnas
    df = pd.DataFrame(datos_estructura, columns=columnas)

    print('Datos descargados.')

    return df

# %%
def download_intercambio(conn):
    print('Iniciando descarga...')
    cursor = conn.cursor()
    ### INTERCAMBIO ###
    query = "SELECT * FROM fronteras ORDER BY fecha DESC"
    cursor.execute(query)
    
    # Obtener nombres de las columnas
    columnas = [desc[0] for desc in cursor.description]

    # Obtener los datos
    datos_fronteras = cursor.fetchall()

    # Crear el DataFrame con los nombres de las columnas
    df = pd.DataFrame(datos_fronteras, columns=columnas)

    print('Datos descargados.')

    return df