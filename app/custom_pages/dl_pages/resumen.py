import numpy as np
import pandas as pd
import streamlit as st

def resumen(df):
    st.title('Resumen de las métricas de los modelos:')

    col, _ = st.columns([1, 2])
    with col:
        st.markdown("###### Métricas de Modelos Prophet")

        metricas_df = st.session_state["metricas_df"]
        st.dataframe(metricas_df)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("###### Métricas del Modelos GRU")
        df_metricas2 = st.session_state["df_metricas2"]
        st.dataframe(df_metricas2)
    with col2:
        st.markdown("###### Métricas del Modelos RNN")
        df_metricas1 = st.session_state["df_metricas1"]
        st.dataframe(df_metricas1)
    with col3:
        st.markdown("###### Métricas del Modelos LSTM")
        df_metricas = st.session_state["df_metricas"]
        st.dataframe(df_metricas)