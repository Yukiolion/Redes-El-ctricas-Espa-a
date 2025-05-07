import joblib
import numpy as np
import pandas as pd
import streamlit as st
from prophet.plot import plot_plotly, plot_components_plotly
from sklearn.metrics import mean_absolute_error, mean_squared_error as mse, r2_score

def prophet(df):
    st.title("Meta Prophet")

    # Selección de frecuencia
    frecuencia = st.selectbox(
        "Selecciona la frecuencia del modelo:",
        options=["Diario", "Semanal", "Mensual", "Trimestral", "Semestral", "Anual"],
        index=0
    )

    # Rango de predicción en días por frecuencia
    frecuencia_rango = {
        "Diario": 14,
        "Semanal": 56,
        "Mensual": 180,
        "Trimestral": 365,
        "Semestral": 730,
        "Anual": 1825
    }

    rango = frecuencia_rango.get(frecuencia, 14)
    st.markdown(f"Se realizarán predicciones para los próximos **{rango} días** según la frecuencia seleccionada.")
    
    # Cargar los modelos para todas las frecuencias
    modelos = {}
    for freq in frecuencia_rango.keys():
        archivo_modelo = f"models/prophet_models/modelo_prophet_{freq}.pkl"
        modelos[freq] = joblib.load(archivo_modelo)
    
    # Preparar los datos
    df = df.copy()
    df.rename(columns={'fecha': 'ds', 'valor': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])

    # Fechas futuras
    ultima_fecha = df['ds'].max()
    fechas_futuras = pd.date_range(start=ultima_fecha + pd.Timedelta(days=1), periods=rango, freq='D')
    future = pd.DataFrame({'ds': fechas_futuras})

    # Realizar las predicciones para la frecuencia seleccionada
    modelo = modelos[frecuencia]
    forecast = modelo.predict(future)
    df_futuro = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
        columns={"ds": "fecha", "yhat": "Demanda Predicha (kWh)", "yhat_lower": "mínimo", "yhat_upper": "máximo"}
    )


    st.markdown("###### Predicciones futuras")
    df_futuro['fecha'] = df_futuro['fecha'].dt.strftime('%d/%m/%Y')
    col, _ = st.columns([1, 2])
    with col:
        st.dataframe(df_futuro)

    # Gráficas
    fig1 = plot_plotly(modelo, forecast)
    fig1.update_traces(mode='lines')
    fig1.data[0].update(line=dict(color='red'))
    fig1.update_layout(
        title=f'Predicción de demanda ({frecuencia})',
        xaxis_title='Fecha',
        yaxis_title='Demanda',
        template='plotly_dark'
    )

    st.plotly_chart(fig1)

    fig2 = plot_components_plotly(modelo, forecast)
    fig2.update_layout(template='plotly_dark')

    st.plotly_chart(fig2)

    # Calcular métricas históricas para todos los modelos
    metricas = []
    for freq, model in modelos.items():
        y_true = model.history['y']
        y_pred = model.predict(model.history[['ds']])['yhat']

        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mse(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)

        metricas.append({
            "Frecuencia": freq,
            "MAE": mae,
            "RMSE": rmse,
            "R²": r2
        })

    # Mostrar todas las métricas
    metricas_df = pd.DataFrame(metricas)
    
    st.session_state["metricas_df"] = metricas_df

    st.markdown("###### Métricas de las diferentes frecuencias")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(metricas_df)
    with col2:
        st.write(
            'En las gráficas trimestrales, semestrales y anuales se puede observar una curva plana,  esto es debido a que Prophet, no detecta' \
            ' una estacionalidad significativa en los datos, y por lo tanto genera predicciones con una R² de 1 o cercana a 1.')
