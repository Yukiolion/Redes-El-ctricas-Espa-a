import streamlit as st

from scripts.db_connect import db_connect
from scripts.download import download_demanda
from custom_pages.dl_pages.gru import gru
from custom_pages.dl_pages.prophet import prophet
from custom_pages.dl_pages.rnn import rnn

def DL():

    conn = db_connect()

    df_demanda = download_demanda(conn)

    conn.close()

    st.title('🖥️ Modelos de prediccion')

    tabs = st.tabs(["GRU", "Prophet", "RNN"])

    with tabs[0]:
        gru(df_demanda)
    with tabs[1]:
        prophet(df_demanda)
    with tabs[2]:
        rnn(df_demanda)