import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests


def Balance():
    st.title("Balance Eléctrico")
    st.write("En este apartado se representa la cantidad total de electricidad generada por todas las fuentes disponibles " \
             "en el sistema eléctrico Español a lo largo de los años.")
    df_balance = pd.read_csv('../lib/data/processed/balance/balance-electrico-limpio.csv')

    st.write("**🔄 Evolución del balance a lo largo de los años**")
    df_balance['fecha'] = pd.to_datetime(df_balance['fecha'])
    df_balance['año'] = df_balance['fecha'].dt.year

    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Rango fechas"], key="grafico_balance")

    # Gráfico de líneas filtrado
    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30])
        fecha_max = df_balance['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_balance[df_balance['fecha'] >= fecha_min]
        tickformat = '%d %b'

        # Generar el gráfico directamente
        grafico_lineas = df_filtrado.groupby(['fecha', 'energia'])['valor'].sum().reset_index()
        fig = px.line(
            grafico_lineas,
            x='fecha',
            y='valor',
            color='energia',
            labels={'fecha': 'Fecha', 'valor': 'kWh', 'energia': 'Tipo de energía'}
        )
        fig.update_traces(line=dict(width=1))
        fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
        st.plotly_chart(fig)

    else:
        fecha_min_total = df_balance['fecha'].min()
        fecha_max_total = df_balance['fecha'].max()
        rango_fechas = st.date_input(
            "Selecciona el rango de fechas:",
            value=(fecha_min_total.date(), fecha_max_total.date()),
            min_value=fecha_min_total.date(),
            max_value=fecha_max_total.date()
        )

        if (
            isinstance(rango_fechas, tuple) 
            and len(rango_fechas) == 2 
            and rango_fechas[0] is not None 
            and rango_fechas[1] is not None
        ):
            fecha_inicio = pd.to_datetime(rango_fechas[0])
            fecha_fin = pd.to_datetime(rango_fechas[1])

            if fecha_inicio <= fecha_fin:
                df_filtrado = df_balance[
                    (df_balance['fecha'] >= fecha_inicio) &
                    (df_balance['fecha'] <= fecha_fin)
                ]
                tickformat = '%b %Y'

                # Generar el gráfico solo si las fechas son válidas
                grafico_lineas = df_filtrado.groupby(['fecha', 'energia'])['valor'].sum().reset_index()
                fig = px.line(
                    grafico_lineas,
                    x='fecha',
                    y='valor',
                    color='energia',
                    labels={'fecha': 'Fecha', 'valor': 'kWh', 'energia': 'Tipo de energía'}
                )
                fig.update_traces(line=dict(width=1))
                fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
                st.plotly_chart(fig)

    st.write("En esta gráfica se observa que la energía almacenada es la que menos watios por hora aporta. Tambien podemos observar " \
    "que desde el 2019 al 2024 la energía producida por las fuentes renovables va en aumento. Además se puede ver como se " \
    "equilibra con fuentes no renovables para afrontar la demanda eléctrica.")

    st.write("**🔄 Histograma del balance de electicidad**")
   
    df_balance['fecha'] = pd.to_datetime(df_balance['fecha'])
    df_balance['año'] = df_balance['fecha'].dt.year

    años_disponibles = sorted(df_balance['año'].unique())
    año = st.selectbox("Selecciona el año:", años_disponibles, key="select_año")

    df_filtrado = df_balance[df_balance['año'] == año]
    
    q1 = df_filtrado['valor'].quantile(0.25)
    q3 = df_filtrado['valor'].quantile(0.75)
    iqr = q3 - q1
    valla_inferior = q1 - 1.5 * iqr
    valla_superior = q3 + 1.5 * iqr

    # Histograma
    fig_hist = px.histogram(df_filtrado, 
                            x='valor',                         
                            labels={'valor': 'Demanda diaria (kWh)'})

    fig_hist.add_vline(x=valla_inferior, line_dash="dash", line_color="red",
                    annotation_text="Límite inferior", annotation_position="top left")
    fig_hist.add_vline(x=valla_superior, line_dash="dash", line_color="red",
                    annotation_text="Límite superior", annotation_position="top right")

    st.plotly_chart(fig_hist)

    st.write("Aquí podemos ver un histograma de la generación acumulada anual de electricidad, donde se marcan los límites de la valla de Tukey. "
         "Se puede ver que hay un grupo importante de tecnologias de generación que aportan muy poca energía al sistema durante largos periodos de tiempo. " \
         "Además se pueden apreciar algunos que consumen energía. " \
         "Es importante señalar que en este caso, los límites no se utilizan únicamente para identificar valores atípicos de manera estricta  "
         "sino para resaltar picos recurrentes de consumo a lo largo de los años. Los valores fuera de estos límites nos ayudan a entender" \
         " cómo se distribuye el consumo en un rango habitual, permitiéndonos detectar sobresaturaciones de la red eléctrica.") 

