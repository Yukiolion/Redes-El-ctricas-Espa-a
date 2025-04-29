import pickle
import pandas as pd
import streamlit as st
from prophet.plot import plot_plotly, plot_components_plotly
from prophet import Prophet
from datetime import timedelta

def prophet(df):
    st.title("Meta Prophet")
    st.write('Aquí se mostrarán las predicciones del modelo Prophet para la región Peninsular.')

    rango = st.selectbox(
        "Selecciona un rango:",
        options=[1, 7, 14, 24],
        index=3
    )

    with open("../models/prophet_models/modelo_prophet_peninsular.pkl", "rb") as f:
        modelo = pickle.load(f)

    df.rename(columns={'fecha': 'ds', 'valor': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])
    ultima_fecha = df['ds'].max()

    modelo.history = df
    modelo.history_dates = pd.to_datetime(df['ds'])

    future = modelo.make_future_dataframe(periods=rango, freq='D')

    ultima_fecha = pd.to_datetime(ultima_fecha)
    future = future[future['ds'] > ultima_fecha]

    forecast = modelo.predict(future)

    df_futuro = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(rango)
    st.dataframe(df_futuro)

    # Gráficos
    fig1 = plot_plotly(modelo, forecast)
    start_date = df_futuro['ds'].min()
    end_date = df_futuro['ds'].max()
    fig1.update_layout(
        title='Predicción de demanda para Peninsular usando Prophet',
        xaxis_title='Fecha',
        yaxis_title='Demanda',
        xaxis=dict(
            range=[start_date, end_date],
            rangeselector=dict(visible=False),
            rangeslider=dict(visible=True, range=[start_date, end_date]),
            type="date"
        ),
        template='plotly_dark'
    )

    fig2 = plot_components_plotly(modelo, forecast)
    fig2.update_layout(
        title='Componentes de la predicción de demanda para Peninsular',
        template='plotly_dark'
    )

    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

    st.write('En la gráfica diaria observamos una curva plana; esto es debido a que Prophet, al no detectar'\
             ' una estacionalidad diaria significativa en los datos, genera predicciones sin mucha variación.')