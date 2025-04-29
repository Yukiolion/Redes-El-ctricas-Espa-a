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

    # Predecir
    y_pred_scaled = model.predict(X)
    y_pred = scaler.inverse_transform(y_pred_scaled)
    y_real = valores[window_size:]

    # Mostrar gráfico predicción vs real
    st.subheader("Predicción vs Valor Real")
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y_real.flatten(), mode='lines', name='Valor Real'))
    fig.add_trace(go.Scatter(y=y_pred.flatten(), mode='lines', name='Predicción'))
    fig.update_layout(title='Predicción de la demanda vs. real',
                    xaxis_title='Timestep',
                    yaxis_title='Demanda',
                    template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar gráfico de pérdida (si existe)
    st.subheader("Pérdida del Modelo (Loss por Epoch)")
    try:
        history = joblib.load(HISTORY_PATH)
        fig_loss = go.Figure()
        fig_loss.add_trace(go.Scatter(y=history['loss'], mode='lines', name='Train Loss'))
        fig_loss.add_trace(go.Scatter(y=history['val_loss'], mode='lines', name='Val Loss'))
        fig_loss.update_layout(title='Función de pérdida (MSE)',
                            xaxis_title='Epoch',
                            yaxis_title='Pérdida',
                            template='plotly_white')
        st.plotly_chart(fig_loss, use_container_width=True)
    except FileNotFoundError:
        st.info("No se encontró historial de entrenamiento para mostrar la pérdida.")