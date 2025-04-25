import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# from lib.scripts.master import actualizacion_general
from scripts.db_connect import db_connect
from scripts.download import download_balance, download_demanda, download_ire, download_generacion, download_intercambio

import streamlit as st


from custom_pages.exploratory_pages.Balance import Balance
from custom_pages.exploratory_pages.Demanda import Demanda
from custom_pages.exploratory_pages.Generacion import Generacion
from custom_pages.exploratory_pages.Intercambio import Intercambio

def Exploratory():



    st.markdown('<a name="top"></a>', unsafe_allow_html=True)

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

    st.markdown("""
    <style>
    .inicio_pagina {
        display: inline-block;
        padding: 0.5em 1em;
        margin-top: 1em;
        background-color: #b01923;
        color: white !important;
        text-decoration: none !important;
        border-radius: 10px;
        font-weight: bold;
        font-family: Verdana;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
        transition: background-color 0.3s ease;
        cursor: pointer;
    }
    .inicio_pagina:hover {
        background-color: #d11b27;
    }
    </style>

    <div style="text-align: right;">
        <a href="#top" class="inicio_pagina">⬆️ Volver al inicio</a>
    </div>
""", unsafe_allow_html=True)