# %%
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import mysql.connector
import os
from scripts.db_connect import db_connect

# %%
def carga_de_datos(df_balance_limpio, df_generacion_limpio, df_fronteras_limpio, df_demanda_limpio, df_ire_limpio):
    print("Cargando datos en la base de datos...")
    conn = db_connect()

    if conn.is_connected():
        print("Conexión exitosa a la base de datos.")
    else:
        print("Error: No se pudo conectar a la base de datos.")
        return False
    cursor = conn.cursor()

    nuevo_balance = ['fecha', 'tipo', 'energia', 'region', 'valor']
    df_balance_limpio = df_balance_limpio[nuevo_balance]

    df_balance_limpio.head()

    for _, row in df_balance_limpio.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO balance (fecha, tipo, energia, region, valor)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['fecha'], row['tipo'], row['energia'], row['region'], row['valor']))

    conn.commit()

    nuevo_ire = ['fecha', 'indicador', 'region', 'valor', 'porcentaje']
    df_ire_limpio = df_ire_limpio[nuevo_ire]

    df_ire_limpio.head()

    for _, row in df_ire_limpio.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO demanda_ire_general (fecha, indicador, region, valor, porcentaje)
            VALUES (%s, %s, %s, %s, %s)
        """, (row['fecha'], row['indicador'], row['region'], row['valor'], row['porcentaje']))

    conn.commit()

    nuevo_demanda = ['fecha', 'indicador', 'region', 'valor']
    df_demanda_limpio = df_demanda_limpio[nuevo_demanda]
    df_demanda_limpio.head()

    for _, row in df_demanda_limpio.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO demanda_evolucion (fecha, indicador, region, valor)
            VALUES (%s, %s, %s, %s)
        """, (row['fecha'], row['indicador'], row['region'], row['valor']))

    conn.commit()

    nuevo_fronteras = ['fecha', 'pais', 'valor', 'porcentaje']
    df_fronteras_limpio = df_fronteras_limpio[nuevo_fronteras]
    df_fronteras_limpio.head()

    for _, row in df_fronteras_limpio.iterrows():
        cursor.execute("""
            INSERT IGNORE INTO fronteras (fecha, pais, valor, porcentaje)
            VALUES (%s, %s, %s, %s)
        """, (row['fecha'], row['pais'], row['valor'], row['porcentaje']))

    conn.commit()

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