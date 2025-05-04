import numpy as np
import pandas as pd
import streamlit as st

def conclusiones(df):
    st.markdown('##### Conclusiones de modelos:')
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

    data = {
        "Modelo": ["GRU", "LSTM", "RNN"],
        "MAE": [17.04, 18.88, 26.25],
        "RMSE": [25.58, 28.33, 35.23],
        "R²": [0.851, 0.818, 0.718]
    }
    df = pd.DataFrame(data)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("###### Métricas modelos Redes Neuronales")
        st.dataframe(df.set_index("Modelo"))

    with col2:
        st.markdown("###### Métricas modelos Prophet")

        metricas_df = st.session_state["metricas_df"]
        st.dataframe(metricas_df)


    st.markdown("""
    ###### Modelos de Redes Neuronales
    - **GRU** sigue siendo el mejor entre los modelos neuronales, con mejor balance entre error y capacidad explicativa.
    - **LSTM** es competitivo, aunque un poco menos preciso.
    - **RNN** tiene peor desempeño, como se esperaba por su arquitectura más simple.

    ###### Prophet
    - A **frecuencias bajas (trimestral, semestral, anual)**, Prophet muestra métricas casi perfectas, pero esto se debe a que **no detecta adecuadamente estacionalidades a esa resolución**, y simplemente ajusta una línea casi plana (riesgo de sobreajuste aparente).
    - A **frecuencias más altas (diaria, semanal)**, el rendimiento de Prophet es comparable al de LSTM y GRU, aunque tiende a no capturar bien dinámicas no lineales complejas.

    ###### Conclusiones:
    - Para series temporales con patrones complejos y resolución diaria/semanal, **GRU es el modelo más robusto**.
    - Prophet es útil en contextos donde la frecuencia es baja y se prioriza interpretabilidad o velocidad de entrenamiento, pero sus resultados pueden ser engañosamente buenos si la estacionalidad no está presente.
    """)

