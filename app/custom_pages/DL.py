import streamlit as st

from scripts.update import update
from scripts.db_connect import db_connect
from scripts.download import download_demanda
from custom_pages.dl_pages.gru import gru
from custom_pages.dl_pages.prophet import prophet
from custom_pages.dl_pages.rnn import rnn
from custom_pages.dl_pages.lstm import lstm

def DL():

    conn = db_connect()

    df_demanda = download_demanda(conn)

    conn.close()
    st.markdown('<a name="top"></a>', unsafe_allow_html=True)
    st.title('🖥️ Modelos de prediccion')

    # Botón para actualizar la base de datos
    if st.button("🔄 Actualizar base de datos"):
        with st.spinner("Actualizando la base de datos..."):
            actualizacion = update()
            if actualizacion:
                st.success("✅ Base de datos actualizada.")
            else:
                st.error("❌ Error al actualizar la base de datos.")

    tabs = st.tabs(["Prophet", "GRU", "RNN", "LSTM"])

    with tabs[0]:
        prophet(df_demanda)
    with tabs[1]:
        gru(df_demanda)
    with tabs[2]:
        rnn(df_demanda)
    with tabs[3]:
        lstm(df_demanda)

    st.markdown("""
        <style>
        .inicio_pagina {
            display: inline-block;
            padding: 0.5em 1em;
            margin-top: 1em;
            background-color: #1c188c;
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
            background-color: #2c25db;
        }
        </style>

        <div style="text-align: right;">
            <a href="#top" class="inicio_pagina">⬆️ Volver al inicio</a>
        </div>
    """, unsafe_allow_html=True)