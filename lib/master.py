import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.extraccion_update import extraccion_update
from scripts.limpieza import limpieza_balance, limpieza_demanda, limpieza_generacion, limpieza_fronteras
# from scripts.carga import upload_data
from scripts.db_connect import db_connect
from scripts.last_date import get_last_date


def actualizacion_general():
    conn = db_connect()

    tablas = ['balance', 'demanda_evolucion', 'demanda_ire_general', 'estructura_generacion', 'fronteras']
    last_date = get_last_date(tablas)
    act_date = datetime.today()

    print(f"Última fecha en la base de datos: {last_date}")
    print(f"Fecha de actualización: {act_date}")
    if last_date is None:
        print("No hay datos en la base de datos.")
        return
    if last_date == act_date.date():
        print("Datos ya actualizados.")
        return

    start = last_date + timedelta(days=1)
    end = act_date
    print(f"Actualizando desde {start} hasta {end}")

    if upgrade_dataframes := extraccion_update(start, end):
        dfs_limpios = {}

        # Limpieza de los DataFrames simples (uno a uno)
        for nombre, df in upgrade_dataframes.items():
            try:
                if nombre == 'balance':
                    df_balance_limpio = limpieza_balance(df)
                elif nombre == 'generacion':
                    df_generacion_limpio = limpieza_generacion(df)
                elif nombre == 'fronteras':
                    df_fronteras_limpio = limpieza_fronteras(df)
                else:
                    print(f"Nombre de DataFrame no reconocido: {nombre}")
                    continue
            except Exception as e:
                print(f"Error limpiando el DataFrame {nombre}: {e}")
                continue

        # Limpieza de los DataFrames de demanda (se procesan juntos)
        try:
            df1_demanda = upgrade_dataframes['demanda']
            df2_demanda = upgrade_dataframes['ire_general']
            df3_demanda = upgrade_dataframes['ire_industria']
            df4_demanda = upgrade_dataframes['ire_servicios']

            df_demanda_evolucion_limpio, df_ire_limpio = limpieza_demanda(df1_demanda, df2_demanda, df3_demanda, df4_demanda)

            print("df_demanda_evolucion_limpio y df_ire_limpio generados")
        except Exception as e:
            print(f"Error limpiando los datos de demanda: {e}")

        carga_de_datos = carga_de_datos(df_balance_limpio, df_generacion_limpio, df_fronteras_limpio, df_demanda_evolucion_limpio, df_ire_limpio)
        if carga_de_datos:
            print("Datos cargados correctamente.")
        else:
            print("Error al cargar los datos.")

    conn.close()
    print("Actualización completa.")


if __name__ == "__main__":
    actualizacion_general()
    print("Conexión cerrada.")