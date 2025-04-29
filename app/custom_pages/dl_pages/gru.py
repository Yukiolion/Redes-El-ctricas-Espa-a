import streamlit as st
import pandas as pd
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import plotly.graph_objects as go
import os
from scripts.db_connect import db_connect

def gru(_):
    st.title("GRU (Gated Recurrent Unit)")

    # Definir rutas
    BASE_DIR = os.path.dirname(__file__)
    MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "..", "models", "GRU_models"))
    MODEL_PATH = os.path.join(MODEL_DIR, "modelo_gru.keras")
    SCALER_PATH = os.path.join(MODEL_DIR, "scaler_gru.pkl")
    HISTORY_PATH = os.path.join(MODEL_DIR, "historial_entrenamiento_gru.pkl")

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

    # Preprocesamiento de los datos
    le_indicador = LabelEncoder()
    df['indicador_encoded'] = le_indicador.fit_transform(df['indicador'])

    features = ['valor', 'indicador_encoded']
    df_scaled = scaler.transform(df[features])

    # Crear secuencias de entrenamiento y prueba
    window_size = 24
    X, y = create_sequences(df_scaled, window_size)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    # Graficar la función de pérdida (si tienes historial de entrenamiento)
    st.subheader("Pérdida durante el entrenamiento")
    history = joblib.load(HISTORY_PATH)
    fig_loss = go.Figure()
    fig_loss.add_trace(go.Scatter(x=np.arange(len(history['loss'])), y=history['loss'], mode='lines', name='Train Loss'))
    fig_loss.add_trace(go.Scatter(x=np.arange(len(history['val_loss'])), y=history['val_loss'], mode='lines', name='Val Loss'))
    fig_loss.update_layout(
        title='Función de pérdida durante el entrenamiento',
        xaxis_title='Epoch',
        yaxis_title='Loss',
        template='plotly_dark'
    )
    st.plotly_chart(fig_loss)

    # Predicción one-step
    one_step_preds = one_step_prediction(model, X_test, scaler)
    valor_scaler = MinMaxScaler()
    valor_scaler.min_, valor_scaler.scale_ = scaler.min_[0], scaler.scale_[0]
    y_test_invert = valor_scaler.inverse_transform(y_test.reshape(-1, 1))

    st.subheader("Predicciones One-Step vs Valores Reales")
    fig_one_step = go.Figure()
    fig_one_step.add_trace(go.Scatter(x=np.arange(len(y_test_invert)), y=y_test_invert.flatten(), mode='lines', name='Real'))
    fig_one_step.add_trace(go.Scatter(x=np.arange(len(one_step_preds)), y=one_step_preds.flatten(), mode='lines', name='Predicción One-Step'))
    fig_one_step.update_layout(
        title='Predicción One-Step vs Valores Reales',
        xaxis_title='Índice de muestra',
        yaxis_title='Demanda',
        template='plotly_dark'
    )
    st.plotly_chart(fig_one_step)

    # Predicciones de múltiples pasos
    future_steps = 24
    last_seq = X_test[-1]  
    predicciones_futuras = multiple_step_prediction(model, last_seq, steps=future_steps, scaler=scaler)

    last_date = df['fecha'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=future_steps)

    df_futuro = pd.DataFrame({
        'fecha': future_dates,
        'demanda_predicha': predicciones_futuras.flatten()
    })

    st.subheader("Predicciones Futuras")
    st.write(df_futuro)

    # Graficar las predicciones futuras
    fig_future = go.Figure()
    fig_future.add_trace(go.Scatter(x=df_futuro['fecha'], y=df_futuro['demanda_predicha'], mode='lines+markers', name='Predicción Futuro'))
    fig_future.update_layout(
        title='Predicción múltiple hacia el futuro',
        xaxis_title='Fecha',
        yaxis_title='Demanda predicha',
        template='plotly_dark'
    )
    st.plotly_chart(fig_future)

# Función para crear secuencias de datos
def create_sequences(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size, 0])  # Predicción del primer valor
    return np.array(X), np.array(y)

# Función para predicción de un paso
def one_step_prediction(model, X, scaler):
    preds = model.predict(X)
    valor_scaler = MinMaxScaler()
    valor_scaler.min_, valor_scaler.scale_ = scaler.min_[0], scaler.scale_[0]
    return valor_scaler.inverse_transform(preds)

# Función para predicción de múltiples pasos
def multiple_step_prediction(model, input_seq, steps, scaler):
    preds = []
    current_seq = input_seq.copy()
    
    for _ in range(steps):
        pred = model.predict(current_seq[np.newaxis])[0][0]
        preds.append(pred)
        
        # Actualizar secuencia deslizante
        next_input = np.roll(current_seq, -1, axis=0)
        next_input[-1] = np.copy(current_seq[-1])
        next_input[-1][0] = pred  

        current_seq = next_input

    valor_scaler = MinMaxScaler()
    valor_scaler.min_, valor_scaler.scale_ = scaler.min_[0], scaler.scale_[0]
    return valor_scaler.inverse_transform(np.array(preds).reshape(-1, 1))