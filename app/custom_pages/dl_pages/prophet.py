import pickle
import streamlit as st
from prophet.plot import plot_plotly, plot_components_plotly
from prophet import Prophet
from datetime import timedelta

def prophet(df):
    st.markdown('<a name="top"></a>', unsafe_allow_html=True)
    st.title("Meta Prophet")
    st.write('Aquí se mostrarán las predicciones del modelo Prophet para la región Peninsular.')

    # Selección del rango de días
    rango = st.selectbox(
        "Selecciona un rango:",
        options=[1, 7, 14, 24],
        index=3
    )

    # Cargar el modelo
    with open("../models/prophet_models/modelo_prophet_peninsular.pkl", "rb") as f:
        modelo = pickle.load(f)

    # Crear el futuro
    future = modelo.make_future_dataframe(periods=rango, freq='D')
    forecast = modelo.predict(future)

    # Solo los datos futuros
    df_futuro = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(rango)

    # Mostrar la tabla
    st.dataframe(df_futuro)

    # Crear la figura usando plot_plotly
    fig1 = plot_plotly(modelo, forecast)

    # Obtener fechas para ajustar el rango
    start_date = df_futuro['ds'].min()
    end_date = df_futuro['ds'].max()

    # Ajustar el layout del gráfico
    fig1.update_layout(
        title=f'Predicción de demanda para Peninsular usando Prophet',
        xaxis_title='Fecha',
        yaxis_title='Demanda',
        xaxis=dict(
            range=[start_date, end_date],  # Limitar zoom inicial
            rangeselector=dict(visible=False),  # Quitar botones de selección rápida
            rangeslider=dict(
                visible=True,
                range=[start_date, end_date]  # También limitar el rango del slider
            ),
            type="date"
        ),
        template='plotly_dark'
    )

    # Componentes del modelo
    fig2 = plot_components_plotly(modelo, forecast)
    fig2.update_layout(
        title=f'Componentes de la predicción de demanda para Peninsular',
        xaxis_title='Fecha',
        yaxis_title='Demanda',
        template='plotly_dark'
    )

    # Mostrar gráficos
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

    st.write('En la gráfica diaria observamos una curva plana; esto es debido a que Prophet, al no detectar'\
             ' una estacionalidad diaria significativa en los datos, genera predicciones sin mucha variación.')
    
    st.markdown("""
        <style>
        .inicio_pagina {
            display: inline-block;
            padding: 0.5em 1em;
            margin-top: 1em;
            background-color: #1c188c;
            color: white !important;
            text-decoration: none !important;
            border-radius: 10px;
            font-weight: bold;
            font-family: Verdana;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
            transition: background-color 0.3s ease;
            cursor: pointer;
        }
        .inicio_pagina:hover {
            background-color: #2c25db;
        }
        </style>

        <div style="text-align: right;">
            <a href="#top" class="inicio_pagina">⬆️ Volver al inicio</a>
        </div>
    """, unsafe_allow_html=True)