import streamlit as st

import plotly.express as px
import numpy as np
import pandas as pd
import requests

# PAGINA PRINCIPAL DEL PROYECTO(TITULO, IMAGEN Y DESCRIPCION)
def main():
    st.title("Proyecto Red Eléctrica España")

    st.image("https://norbelenergia.es/wp-content/uploads/2024/06/1200px-Red_Electrica_de_Espana_logo.svg1_.png", width=600)

    st.write("El objetivo principal de este proyecto es extraer, procesar y visualizar datos energéticos de la web de Red Eléctrica de España (REE), " \
    "relacionados con la demanda eléctrica, el balance energético, la generación y los intercambios internacionales de energía. Esto permite visualizar " \
    "y analizar cómo se comporta el sistema eléctrico español en distintos momentos del día y del año.")

    st.write('Definicion de los datos:')
    # Esto es un selectbox que permite seleccionar entre los diferentes tipos de datos que tenemos
    # y muestra una breve descripcion de cada uno de ellos
    opcion = st.selectbox('Seleccionar los datos:', 
                                   ('Balance', 'Demanda', 'Generación', 'Intercambio'))
    if opcion == 'Balance':
        st.info("🔄 El **balance energético** representa la diferencia entre la energía generada y la consumida, incluyendo pérdidas y ajustes del sistema.")
    elif opcion == 'Demanda':
        st.info("⚡ La **demanda eléctrica** muestra cuánta energía están consumiendo los usuarios en un momento dado o durante un periodo.")
    elif opcion == 'Generación':
        st.info("⚙️ La **generación eléctrica** indica cuánta energía se está produciendo y con qué fuentes (renovables, no renovables, nuclear, etc.).")
    elif opcion == 'Intercambio':
        st.info("🌍 Los **intercambios internacionales** reflejan la energía que España importa o exporta a países vecinos a través de las interconexiones.")

# AÑADIR LOS DATOS DE CADA UNA DE LAS SECCIONES EN LA FUNCION CORRESPONDIENTE
def Balance():
    st.title("Balance Energético")
    st.write("Aquí se agregaran los datos y graficas del balance energético de España.")
    df_balance = pd.read_csv('../../lib/data/processed/balance/balance-electrico-limpio.csv')
    df_balance


    grafico_lineas = df_balance.groupby(['fecha', 'energia'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                x='fecha',
                y='valor',
                color='energia',
                title="Evolución del balance energético desde 2019 hasta 2023",
                labels={'fecha': 'Fecha', 'energia': 'Tipo energia'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat='%b %Y', yaxis_title='kWh')
    st.plotly_chart(fig)


    df_balance['fecha'] = pd.to_datetime(df_balance['fecha'])
    df_balance['año'] = df_balance['fecha'].dt.year

    grafico_barras = df_balance.groupby(['año', 'tipo'])['valor'].sum().reset_index()

    fig = px.bar(grafico_barras,
                x='año',
                y='valor',
                color='tipo',
                title="Distribución de tipo de energía por años",
                labels={'valor': 'kWh', 'año': 'Año'},
                hover_data={'valor': ':.2f'},
                barmode='stack')
    fig.update_layout(height=700)
    st.plotly_chart(fig)


def Demanda():
    st.title("Demanda Eléctrica")
    st.write("Aquí se agregaran los datos y graficas de la demanda eléctrica de España.")

    df_demanda = pd.read_csv('../../lib/data/processed/demanda/demanda-limpio.csv')
    df_demanda

    df_ire = pd.read_csv('../../lib/data/processed/demanda/ire-limpio.csv')
    df_ire

    grafico_lineas = df_ire.groupby(['fecha', 'indicador'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                x='fecha',
                y='valor',
                color='indicador',
                title="Evolución de ire de demanda en la región peninsular",
                labels={'fecha': 'Fecha', 'energia': 'Wh', 'tipo energia': 'Tipo de energía'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat='%b %Y')
    st.plotly_chart(fig)


    grafico_lineas = df_demanda.groupby(['fecha', 'indicador'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                x='fecha',
                y='valor',
                color='indicador',
                title="Evolución de demanda en la región peninsular",
                labels={'fecha': 'Fecha', 'energia': 'Wh', 'tipo energia': 'Tipo de energía'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat='%b %Y')
    st.plotly_chart(fig)

    filtro = df_ire['indicador'].isin(['Índice general corregido', 'Índice industria corregido', 'Índice servicios corregido'])
    df_filtrado = df_ire[filtro]

    df_agrupado = df_filtrado.groupby(['año', 'indicador'])['valor'].sum().reset_index()


    grafico_barras = df_agrupado.groupby(['año', 'indicador'])['valor'].sum().reset_index()

    fig = px.bar(grafico_barras,
                x='año',
                y='valor',
                color='indicador',
                title="Distribución de tipo de energia por años",
                labels={'valor': 'Wh', 'indicador': 'indices'})
    st.plotly_chart(fig)

def Generacion():
    st.title("Generación Eléctrica")
    st.write("Aquí se agregaran los datos y graficas de la generación eléctrica de España.")

    df_generacion = pd.read_csv('estructura-generacion-limpio.csv')
    df_generacion


    grafico_lineas = df_generacion.groupby(['fecha', 'tipo'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                x='fecha',
                y='valor',
                color='tipo',
                title="Evolución de energía Renovable vs No renovable en la región peninsular",
                labels={'fecha': 'Fecha', 'energia': 'kWh', 'tipo energia': 'Tipo de energía'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat='%b %Y')
    st.plotly_chart(fig)


    grafico_barras = df_generacion.groupby(['año', 'tipo'])['valor'].sum().reset_index()

    fig = px.bar(grafico_barras,
                x='año',
                y='valor',
                color='tipo',
                title="Distribución de tipo de energia por años",
                labels={'energia': 'kWh', 'tipo': 'Tipo de energía'},
                hover_name='tipo',
                barmode='stack')
    st.plotly_chart(fig)

    grafico_hist = df_generacion.groupby(['indicador', 'año'])['valor'].sum().reset_index()

    fig = px.bar(grafico_hist,
                x='indicador',
                y='valor',
                color='año',  
                title='Distribución de generación por tipo de energía y año',
                barmode='group')
    st.plotly_chart(fig)
  
def intercambio():
    st.title("Intercambio Internacional")
    st.write("Aquí se agregaran los datos y graficas de intercambio internacional de energía de España.")

    df_intercambio = pd.read_csv('fronteras-limpio.csv')
    df_intercambio

    grafico_lineas = df_intercambio.groupby(['fecha', 'pais'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                x='fecha',
                y='valor',
                color='pais',
                title="Evolución de la exportacion de energía",
                labels={'fecha': 'Fecha', 'energia': 'kWh', 'tipo energia': 'Tipo de energía'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat='%b %Y')
    st.plotly_chart(fig)

    grafico_barras = df_intercambio.groupby(['año', 'pais'])['valor'].sum().reset_index()

    fig = px.bar(grafico_barras,
                x='año',
                y='valor',
                color='pais',
                title="Distribución de la exportacion de energia por años",
                labels={'energia': 'kWh', 'pais': 'pais'},
                hover_name='pais',
                barmode='stack')
    st.plotly_chart(fig)



# ESTA FUNCION SE PUEDE USAR COMO CONCLUSIONES O COMO COMPARACIONES PARA COMPARAR DATOS ENTRE LOS TIPOS QUE TENEMOS
def Conclusiones():
    st.title("Conclusiones de Datos")
    st.write("Aquí se agregaran conclusiones sobre los datos analizados.")
    # Aquí puedes agregar el código para mostrar las conclusiones de los datos
    # Por ejemplo, un resumen o análisis de los datos obtenidos


st.sidebar.title('Navegación')
pagina = st.sidebar.radio("", ("Página de Inicio", "Balance", "Demanda", "Generación", "Intercambio", "Conclusion de Datos"))



if pagina == 'Página de Inicio':
    main()
elif pagina == 'Balance':
    Balance()
elif pagina == 'Demanda':
    Demanda()
elif pagina == 'Generación':
    Generacion()
elif pagina == 'Intercambio':
    intercambio()
elif pagina == 'Conclusion de Datos':
    Conclusiones()
