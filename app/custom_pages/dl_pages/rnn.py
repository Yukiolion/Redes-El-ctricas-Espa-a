import streamlit as st
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import plotly.graph_objects as go
import os
from scripts.db_connect import db_connect

def rnn(_):
    st.title("RNN (Recurrent Neural Network)")

    # Definir rutas
    BASE_DIR = os.path.dirname(__file__)
    MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "..", "models", "RNN_models"))
    MODEL_PATH = os.path.join(MODEL_DIR, "modelo_rnn.keras")
    SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
    HISTORY_PATH = os.path.join(MODEL_DIR, "historial_entrenamiento.pkl")

    # Cargar modelo y scaler
    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    # Cargar datos desde la base de datos
    @st.cache_data
    def cargar_datos():
        conn = db_connect()
        query = "SELECT fecha, indicador, valor FROM demanda_evolucion WHERE indicador = 'Demanda'"
        df = pd.read_sql(query, conn)
        conn.close()
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df.sort_values('fecha')

    df = cargar_datos()

    # Preprocesar datos
    valores = df['valor'].values.reshape(-1, 1)
    valores_scaled = scaler.transform(valores)

    # Crear secuencias
    def crear_secuencias(data, window_size):
        X = []
        for i in range(len(data) - window_size):
            X.append(data[i:i+window_size])
        return np.array(X)

    window_size = 30
    X = crear_secuencias(valores_scaled, window_size)

    # Predicción One-Step
    y_pred_scaled = model.predict(X)
    y_pred = scaler.inverse_transform(y_pred_scaled)
    y_real = valores[window_size:]

    fechas = df['fecha'].iloc[window_size:].values

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=fechas, y=y_real.flatten(),
        mode='lines',
        name='Valor Real',
        line=dict(width=1)
    ))
    fig.add_trace(go.Scatter(
        x=fechas, y=y_pred.flatten(),
        mode='lines',
        name='Predicción',
        line=dict(width=1)
    ))
    fig.update_layout(
        title='Predicción de la demanda vs. real',
        xaxis_title='Fecha',
        yaxis_title='Demanda',
        template='plotly_white',
        xaxis=dict(type='date')
    )
    st.plotly_chart(fig, use_container_width=True)


    # Gráfico de pérdida
    history = joblib.load(HISTORY_PATH)
    fig_loss = go.Figure()
    fig_loss.add_trace(go.Scatter(y=history['loss'], mode='lines', name='Train Loss'))
    fig_loss.add_trace(go.Scatter(y=history['val_loss'], mode='lines', name='Val Loss'))
    fig_loss.update_layout(title='Función de pérdida (MSE)',
                        xaxis_title='Epoch',
                        yaxis_title='Pérdida',
                        template='plotly_white')
    st.plotly_chart(fig_loss, use_container_width=True)


    # Predicción Multi-Step
    rango = st.selectbox(
        "Selecciona un rango (días a predecir):",
        options=[1, 7, 14, 24],
        index=1
    )

    def predecir_multiple_pasos(modelo, secuencia_inicial, pasos, scaler):
        predicciones = []
        secuencia_actual = secuencia_inicial.copy()
        for _ in range(pasos):
            input_modelo = secuencia_actual.reshape(1, -1, 1)
            pred = modelo.predict(input_modelo, verbose=0)[0]
            predicciones.append(pred)
            secuencia_actual = np.append(secuencia_actual[1:], [pred], axis=0)
        predicciones_inv = scaler.inverse_transform(np.array(predicciones).reshape(-1, 1))
        return predicciones_inv.flatten()

    secuencia_inicial = valores_scaled[-window_size:]
    predicciones_futuras = predecir_multiple_pasos(model, secuencia_inicial, rango, scaler)

    # Gráfico multi-step
    last_date = df['fecha'].max()
    fecha_inicio = last_date - pd.DateOffset(months=6)

    df_ultimos_meses = df[df['fecha'] >= fecha_inicio]
    valores_historicos = df_ultimos_meses['valor'].values
    fechas_historicas = df_ultimos_meses['fecha'].values

    fechas_futuras = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=rango)

    fig_multi = go.Figure()

    fig_multi.add_trace(go.Scatter(
        x=fechas_historicas,
        y=valores_historicos,
        mode='lines',
        name='Últimos 6 meses',
        line=dict(color='blue', width=1)
    ))

    fig_multi.add_trace(go.Scatter(
        x=fechas_futuras,
        y=predicciones_futuras,
        mode='lines',
        name='Predicción futura',
        line=dict(color='red', width=1)
    ))

    fig_multi.update_layout(
        title=f'Predicción Multi-Step ({rango} días)',
        xaxis_title='Fecha',
        yaxis_title='Demanda',
        template='plotly_white',
        xaxis=dict(type='date')
    )

    st.plotly_chart(fig_multi, use_container_width=True)

    df_pred = pd.DataFrame({
        "Fecha": fechas_futuras.strftime('%d/%m/%Y'),
        "Demanda predicha": predicciones_futuras})

    st.dataframe(df_pred)