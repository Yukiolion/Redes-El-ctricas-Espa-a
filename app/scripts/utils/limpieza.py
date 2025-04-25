# %%
import pandas as pd
import numpy as np
import pandas as pd

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

    df1_demanda['fecha'] = pd.to_datetime(df1_demanda['fecha'].astype(str).str.split(' ').str[0])
    df2_demanda['fecha'] = pd.to_datetime(df2_demanda['fecha'].astype(str).str.split(' ').str[0])
    df3_demanda['fecha'] = pd.to_datetime(df3_demanda['fecha'].astype(str).str.split(' ').str[0])
    df4_demanda['fecha'] = pd.to_datetime(df4_demanda['fecha'].astype(str).str.split(' ').str[0])

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

    return df_fronteras