import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from scripts.extraccion_update import extraccion_update
# from scripts.limpieza import clean_data
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

    # Aquí ya no necesitas el `.date()`, ya que `start` y `end` son objetos `date`
    print(f"Actualizando desde {start} hasta {end}")

    if upgrade_dataframes := extraccion_update(start, end):
        for nombre, df in upgrade_dataframes.items():
            print(f"DataFrame {nombre}:\n{df.head()}")
            # df_limpio = clean_data(df)
            # if df_limpio:
            #     print(f"DataFrame limpio {nombre}:\n{df_limpio.head()}")
            #     upload_data(df_limpio, nombre)
            # else:
            #     print(f"No se pudo limpiar el DataFrame {nombre}.")
        print("Datos actualizados en la base de datos correctamente.")
    else:
        print("No se han podido actualizar los datos.")

    conn.close()
    print("Actualización completa.")


if __name__ == "__main__":
    actualizacion_general()
    print("Conexión cerrada.")