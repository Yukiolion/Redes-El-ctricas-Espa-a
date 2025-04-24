import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.db_connect import db_connect

def get_last_date(tablas):
    conn = db_connect()
    cursor = conn.cursor()
    max_dates = []
    for tabla in tablas:
        query = f"SELECT MAX(fecha) FROM {tabla};"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        if result:
            max_dates.append(result)
            print(f"Tabla: {tabla}, Fecha máxima: {result}")
    cursor.close()
    if max_dates:
        return max(max_dates)
    print ('funciona')
    return None