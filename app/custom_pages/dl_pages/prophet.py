import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.metrics import mean_squared_error as mse
import streamlit as st
from prophet.plot import plot_plotly, plot_components_plotly

def prophet(df):
    st.title("Meta Prophet")
    st.write('Aquí se mostrarán las predicciones del modelo Prophet para la región Peninsular.')

    # Cargar el modelo entrenado
    with open('models/prophet_models/modelo_prophet_peninsular.pkl', "rb") as f:
        modelo = pickle.load(f)

    # Preparar datos
    df = df.copy()
    df.rename(columns={'fecha': 'ds', 'valor': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])

    rango = st.selectbox(
        "Selecciona un rango de días para predecir:",
        options=[1, 7, 14, 24],
        index=3
    )

    # Crear fechas futuras manualmente desde la última fecha en el DataFrame
    ultima_fecha = df['ds'].max()
    fechas_futuras = pd.date_range(start=ultima_fecha + pd.Timedelta(days=1), periods=rango, freq='D')
    future = pd.DataFrame({'ds': fechas_futuras})

    # Predecir
    forecast = modelo.predict(future)

    # Mostrar predicciones
    df_futuro = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    st.markdown("### Predicciones futuras")

    metricas = df_futuro.copy()

    metricas = metricas.rename(columns={"ds": "fecha", "yhat": "predicción", "yhat_lower": "mínimo", "yhat_upper": "máximo"})
    st.dataframe(metricas)

    # Gráficos
    fig1 = plot_plotly(modelo, forecast)
    fig1.update_layout(
        title='Predicción de demanda para Peninsular usando Prophet',
        xaxis_title='Fecha',
        yaxis_title='Demanda',
        xaxis=dict(
            range=[df_futuro['ds'].min(), df_futuro['ds'].max()],
            rangeselector=dict(visible=False),
            rangeslider=dict(visible=True, range=[df_futuro['ds'].min(), df_futuro['ds'].max()]),
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

    st.write(
        'En la gráfica diaria observamos una curva plana; esto es debido a que Prophet, '
        'al no detectar una estacionalidad diaria significativa en los datos, genera predicciones sin mucha variación.'
    )

    forecast_hist = modelo.predict(df[['ds']])

    # Unir valores reales con predicción
    df_hist_eval = df.copy()
    df_hist_eval = df_hist_eval.merge(forecast_hist[['ds', 'yhat']], on='ds')

    # Calcular métricas de entrenamiento
    mae = mean_absolute_error(df_hist_eval['y'], df_hist_eval['yhat'])
    rmse = np.sqrt(mse(df_hist_eval['y'], df_hist_eval['yhat']))
    r2 = r2_score(df_hist_eval['y'], df_hist_eval['yhat'])

    st.markdown("### Métricas del modelo sobre datos históricos")
    st.markdown(f"- **MAE**: {mae:.2f}")
    st.markdown(f"- **RMSE**: {rmse:.2f}")
    st.markdown(f"- **R²**: {r2:.2f}")