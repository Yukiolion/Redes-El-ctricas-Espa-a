import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# from lib.scripts.master import actualizacion_general
from lib.scripts.utils.db_connect import db_connect
from lib.scripts.utils.download import download_balance, download_demanda, download_ire, download_generacion, download_intercambio

import streamlit as st


from app.custom_pages.exploratory_pages.Balance import Balance
from app.custom_pages.exploratory_pages.Demanda import Demanda
from app.custom_pages.exploratory_pages.Generacion import Generacion
from app.custom_pages.exploratory_pages.Intercambio import Intercambio



def Exploratory():
    st.title("📊 Exploratory Data Analysis")

    conn = db_connect()

    df_balance = download_balance(conn)
    df_demanda = download_demanda(conn)
    df_ire = download_ire(conn)
    df_generacion = download_generacion(conn)
    df_fronteras = download_intercambio(conn)
    conn.close()

    # if st.button("🔄 Actualizar base de datos"):
    #     with st.spinner("Actualizando la base de datos..."):
    #         actualizacion  = actualizacion_general()
    #         if actualizacion:
    #             st.success("✅ Base de datos actualizada.")
    #         else:
    #             st.error("❌ Error al actualizar la base de datos.")

    tabs = st.tabs(["Balance", "Demanda", "Generación", "Intercambio"])

    with tabs[0]:
        Balance(df_balance)
    with tabs[1]:
        Demanda(df_demanda, df_ire)
    with tabs[2]:
        Generacion(df_generacion)
    with tabs[3]:
        Intercambio(df_fronteras)