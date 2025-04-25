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
def limpieza_demanda(df_demanda, df_ire_general, df_ire_industria, df_ire_servicios):
    # Asegurar que la columna fecha es tipo datetime
    df_demanda['fecha'] = pd.to_datetime(df_demanda['fecha'], utc=True)
    df_ire_general['fecha'] = pd.to_datetime(df_ire_general['fecha'], utc=True)
    df_ire_industria['fecha'] = pd.to_datetime(df_ire_industria['fecha'], utc=True)
    df_ire_servicios['fecha'] = pd.to_datetime(df_ire_servicios['fecha'], utc=True)

    # Aquí puedes realizar más transformaciones si hace falta (ordenar, filtrar, renombrar, etc.)
    df_demanda_limpio = df_demanda.copy()
    
    # Juntar IRE en uno solo
    df_ire_limpio = pd.concat([
        df_ire_general.assign(tipo='general'),
        df_ire_industria.assign(tipo='industria'),
        df_ire_servicios.assign(tipo='servicios')
    ])
    
    # Asegurar orden por fecha
    df_demanda_limpio.sort_values('fecha', inplace=True)
    df_ire_limpio.sort_values('fecha', inplace=True)

    return df_demanda_limpio, df_ire_limpio

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