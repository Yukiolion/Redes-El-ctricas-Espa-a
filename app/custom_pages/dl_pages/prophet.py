import pickle
import streamlit as st
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.express as px

from scripts.prophet_model import prophet_model

def prophet(df):
    # Título de la aplicación
    st.title("Meta Prophet")
    st.write('Aquí se mostrarán las métricas del modelo.')

    # Selección de la región
    region = st.selectbox("Selecciona la región", df['region'].unique())

    # Selección del rango de días
    rango = st.radio(
        "Selecciona un rango:",
        options=[1, 7, 14, 24],
        index=3  # 24 días como valor por defecto
    )

    def predecir_region(region, rango):
        with open(f"../models/prophet_models/modelo_prophet_{region}.pkl", "rb") as f:
            modelo = pickle.load(f)
        future = modelo.make_future_dataframe(periods=rango, freq='D')
        forecast = modelo.predict(future)
        return forecast, modelo

    # Llamada a la función para predecir
    forecast, modelo = predecir_region(region, rango)

    # Preparar el DataFrame futuro
    df_futuro = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(rango)
    
    # Mostrar predicciones en tabla
    st.dataframe(df_futuro)

    # Gráficas
    fig1 = plot_plotly(modelo, forecast)
    fig1.update_layout(
        title=f'Predicción de demanda para {region} usando Prophet',
        xaxis_title='Fecha',
        yaxis_title='Demanda'
    )

    fig2 = plot_components_plotly(modelo, forecast)
    fig2.update_layout(
        title=f'Componentes de la predicción de demanda para {region}',
        xaxis_title='Fecha',
        yaxis_title='Demanda'
    )

    # Mostrar los gráficos interactivos
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)