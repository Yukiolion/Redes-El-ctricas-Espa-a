import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
import plotly.graph_objects as go
import os
from scripts.db_connect import db_connect
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def lstm(_):
    st.title("LSTM")

    # Definir rutas
    BASE_DIR = os.path.dirname(__file__)
    MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "..", "models", "LSTM_models"))
    MODEL_PATH = os.path.join(MODEL_DIR, "modelo_lstm.keras")
    TEST_PATH = os.path.join(MODEL_DIR, "X_y_test_lstm.npz")
    SCALER_PATH = os.path.join(MODEL_DIR, "scaler_lstm.pkl")
    HISTORY_PATH = os.path.join(MODEL_DIR, "historial_entrenamiento_lstm.pkl")

    # Cargar modelo y scaler
    model = tf.keras.models.load_model(MODEL_PATH)
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

    st.markdown('###### Predicción de la demanda vs. real:')

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
        xaxis_title='Fecha',
        yaxis_title='Demanda (kWh)',
        template='plotly_white',
        xaxis=dict(type='date')
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("En esta gráfica podemos ver los datos de la demanda en azul frente a los datos predichos en rojo. " \
        "Al analizar las métricas de evaluación, podemos ver con este modelo se han mejorado la precisión, llegando a alcanzar casi un 82% de precisión, " \
        "lo que indica que tiene un buen nivel de ajuste.")


    # Métricas
    data_test = np.load(TEST_PATH)
    X_test = data_test["X_test"]
    y_test = data_test["y_test"]

    y_pred_test = model.predict(X_test)
    y_pred_inv = scaler.inverse_transform(y_pred_test)
    y_test_inv = scaler.inverse_transform(y_test)

    mae_test = mean_absolute_error(y_test_inv, y_pred_inv)
    rmse_test = np.sqrt(mean_squared_error(y_test_inv, y_pred_inv))
    r2_test = r2_score(y_test_inv, y_pred_inv)

    df_metricas = pd.DataFrame([{
        "MAE": mae_test,
        "RMSE": rmse_test,
        "R²": r2_test
    }])

    st.markdown('###### Rendimiento del modelo:')
    col2, _ = st.columns([1, 2])
    with col2:
        st.dataframe(df_metricas.style.format({
            "MAE": "{:.2f}",
            "RMSE": "{:.2f}",
            "R²": "{:.4f}"
        }), use_container_width=True)

    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

    # Gráfico de pérdida
    st.markdown('###### Función de pérdida (MSE):')
    history = joblib.load(HISTORY_PATH)
    fig_loss = go.Figure()
    fig_loss.add_trace(go.Scatter(y=history['loss'], mode='lines', name='Train Loss'))
    fig_loss.add_trace(go.Scatter(y=history['val_loss'], mode='lines', name='Val Loss'))
    fig_loss.update_layout(xaxis_title='Epoch',
                        yaxis_title='Pérdida',
                        template='plotly_white')
    st.plotly_chart(fig_loss, use_container_width=True)

    st.write("Esta gráfica muestra la evolución de la pérdida durante el entrenamiento. Se puede ver que el modelo va aprendiendo " \
    "a lo largo de las 25 epocas.")

    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

    # Predicción Multi-Step
    st.markdown('###### Predicción Multi-Step:')
    rango = st.selectbox(
        "Selecciona un rango (días a predecir):",
        options=[1, 7, 14, 24],
        index=1,
        key='multistep_lstm'
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
        xaxis_title='Fecha',
        yaxis_title='Demanda (kWh)',
        template='plotly_white',
        xaxis=dict(type='date')
    )

    st.plotly_chart(fig_multi, use_container_width=True)

    st.write("Esta gráfica muestra la evolución de la demanda de los últimos 6 meses y la predicción a 1, 7, 14 y 24 días. Se puede ver que conforme " \
    "aumentan los días a predecir el modelo empeora que es lo esperado en modelos de series temporales, ya que las predicciones a largo plazo son más inciertas.")

    df_pred = pd.DataFrame({
        "Fecha": fechas_futuras.strftime('%d/%m/%Y'),
        "Demanda predicha (kWh)": predicciones_futuras
    })
    st.session_state["df_metricas"] = df_metricas
    col, _ = st.columns([1, 2])
    with col:
        st.dataframe(df_pred)