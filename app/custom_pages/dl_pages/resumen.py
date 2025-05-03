import numpy as np
import pandas as pd
import streamlit as st

def resumen(df):
    st.title('Resumen de las métricas de los modelos:')

    st.markdown("###### Métricas de Modelos Prophet")

    metricas_df = st.session_state["metricas_df"]
    st.dataframe(metricas_df)

    #st.markdown("###### Métricas del Modelos GRU")
    #df_futuro = st.session_state["df_futuro"]
    #st.dataframe(df_futuro)

    st.markdown("###### Métricas del Modelos RNN")
    df_metricas1 = st.session_state["df_metricas1"]
    st.dataframe(df_metricas1)

    st.markdown("###### Métricas del Modelos LSTM")
    df_metricas = st.session_state["df_metricas"]
    st.dataframe(df_metricas)