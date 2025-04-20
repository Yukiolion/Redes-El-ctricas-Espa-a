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

    st.write('Clasificación de las fuentes de energía')
    # Esto es un selectbox que permite seleccionar entre los diferentes tipos de datos que tenemos
    # y muestra una breve descripcion de cada uno de ellos
    opcion = st.selectbox('Fuentes de energía:', 
                                   ('Renovables', 'No renovables', 'Otras categorias'))
    if opcion == 'Renovables':
        st.info(
            "🌱 **Fuentes de energía renovables**\n\n"
            "Estas fuentes se regeneran de manera natural y son sostenibles en el tiempo. Incluyen:\n\n"
            "- Eólica\n"
            "- Hidráulica\n"
            "- Hidroeólica\n"
            "- Solar fotovoltaica\n"
            "- Solar térmica\n"
            "- Otras renovables\n"
            "- Residuos renovables\n"
            "- Generación renovable\n"
            "- Turbinación bombeo\n"
            "- Entrega batería"
        )
    elif opcion == 'No renovables':
        st.info(
            "⚙️ **Fuentes de energía no renovables**\n\n"
            "Estas fuentes provienen de recursos limitados o contaminantes. Incluyen:\n\n"
            "- Carbón\n"
            "- Ciclo combinado\n"
            "- Cogeneración\n"
            "- Fuel + Gas\n"
            "- Motores diésel\n"
            "- Nuclear\n"
            "- Residuos no renovables\n"
            "- Turbina de gas\n"
            "- Turbina de vapor\n"
            "- Generación no renovable"
        )
    elif opcion == 'Otras categorias':
        st.info(
            "⚖️ **Otras categorías**\n\n"
            "Estas no son fuentes de generación directa, pero están presentes en el sistema. Incluyen:\n\n"
            "- Consumo bombeo (se usa para almacenar energía, no genera)\n"
            "- Demanda en b.c. (baja tensión, no es fuente)\n"
            "- Saldo I. internacionales (intercambios con otros países)\n"
            "- Saldo almacenamiento (puede incluir carga y entrega de baterías)\n"
            "- Carga batería (almacenamiento, no producción directa)"
        )

# AÑADIR LOS DATOS DE CADA UNA DE LAS SECCIONES EN LA FUNCION CORRESPONDIENTE
def Balance():
    st.title("Balance Energético")
    st.write("En este apartado se representa la cantidad total de electricidad generada por todas las fuentes disponibles " \
             "en el sistema eléctrico Español a lo largo de los años.")
    df_balance = pd.read_csv('../lib/data/processed/balance/balance-electrico-limpio.csv')
    
    df_balance['fecha'] = pd.to_datetime(df_balance['fecha'])
    df_balance['año'] = df_balance['fecha'].dt.year

    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Año específico"])

    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30])
        fecha_max = df_balance['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_balance[df_balance['fecha'] >= fecha_min]

        titulo = f"Producción de energía - Últimos {dias} días"
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_balance['año'].unique()))
        df_filtrado = df_balance[df_balance['año'] == año]
        titulo = f"Balance energético - Año {año}"

    # Gráfico de líneas filtrado
    grafico_lineas = df_filtrado.groupby(['fecha', 'energia'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                  x='fecha',
                  y='valor',
                  color='energia',
                  title=titulo,
                  labels={'fecha': 'Fecha', 'valor': 'kWh'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat='%d %b')
    st.plotly_chart(fig)

    # Gráfico de barras por año (sin filtro)
    grafico_barras = df_balance.groupby(['año', 'tipo'])['valor'].sum().reset_index()
    fig = px.bar(grafico_barras,
                 x='año',
                 y='valor',
                 color='tipo',
                 title="Distribución de la producción de energía por años",
                 labels={'valor': 'kWh', 'año': 'Año'},
                 hover_data={'valor': ':.2f'},
                 barmode='stack')
    fig.update_layout(height=700)
    st.plotly_chart(fig)


def Demanda():
    st.title("Demanda Eléctrica")
    st.write("La demanda eléctrica se refiere a la cantidad de electricidad que los consumidores requieren en " \
            " un momento o periodo específico. Es una medida de la cantidad de energía que se necesita para satisfacer " \
            " las necesidades de los usuarios, ya sean residenciales, comerciales o industriales.")

    df_demanda = pd.read_csv('../lib/data/processed/demanda/demanda-limpio.csv')
    df_ire = pd.read_csv('../lib/data/processed/demanda/ire-limpio.csv')
    df_demanda['fecha'] = pd.to_datetime(df_demanda['fecha'])
    df_demanda['año'] = df_demanda['fecha'].dt.year

    # Selección del tipo de visualización
    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Año específico"])

    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30])
        fecha_max = df_demanda['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_demanda[df_demanda['fecha'] >= fecha_min]

        titulo = f"Evolución de demanda - Últimos {dias} días"
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_demanda['año'].unique()))
        df_filtrado = df_demanda[df_demanda['año'] == año]
        titulo = f"Evolución de demanda - Año {año}"

    # Gráfico de líneas filtrado
    grafico_lineas = df_filtrado.groupby(['fecha', 'indicador'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                  x='fecha',
                  y='valor',
                  color='indicador',
                  title="Evolución de demanda en la región peninsular",
                  labels={'fecha': 'Fecha', 'valor': 'Wh', 'indicador': 'Tipo de energía'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat='%b %Y')
    st.plotly_chart(fig)

    st.write("*Índice de Red Eléctrica (IRE)* es el indicador eléctrico adelantado que recoge la evolución " \
            " del consumo de energía eléctrica de las empresas que tienen un consumo de energía eléctrica " \
            " de tamaño medio/alto (potencia contratada superior a 450 kW). ")
    
    filtro = df_ire['indicador'].isin(['Índice general corregido', 'Índice industria corregido', 'Índice servicios corregido'])
    df_filtrado = df_ire[filtro]

    df_agrupado = df_filtrado.groupby(['año', 'indicador'])['valor'].sum().reset_index()



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


    grafico_barras = df_agrupado.groupby(['año', 'indicador'])['valor'].sum().reset_index()

    fig = px.bar(grafico_barras,
                x='año',
                y='valor',
                color='indicador',
                title="Distribución de los tipos de ire por años",
                labels={'valor': 'Wh', 'indicador': 'indices'})
    st.plotly_chart(fig)

def Generacion():
    st.title("Generación Eléctrica")
    st.write("La generación eléctrica convierte energía mecánica, térmica o luminosa en electricidad " \
            "utilizable para consumo doméstico, industrial y comercial.")

    df_generacion = pd.read_csv('../lib/data/processed/generacion/estructura-generacion-limpio.csv')
    df_generacion['fecha'] = pd.to_datetime(df_generacion['fecha'])
    df_generacion['año'] = df_generacion['fecha'].dt.year

    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Año específico"])

    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30])
        fecha_max = df_generacion['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_generacion[df_generacion['fecha'] >= fecha_min]

        titulo = f"Evolución de generación - Últimos {dias} días"
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_generacion['año'].unique()))
        df_filtrado = df_generacion[df_generacion['año'] == año]
        titulo = f"Evolución de generación - Año {año}"

    # Gráfico de energía renovable vs no renovable
    grafico_lineas_generacion = df_filtrado.groupby(['fecha', 'tipo'])['valor'].sum().reset_index()
    fig_generacion = px.line(grafico_lineas_generacion,
                             x='fecha',
                             y='valor',
                             color='tipo',
                             title="Evolución de energía Renovable vs No renovable en la región peninsular",
                             labels={'fecha': 'Fecha', 'valor': 'kWh', 'tipo': 'Tipo de energía'})
    fig_generacion.update_traces(line=dict(width=1))
    fig_generacion.update_layout(xaxis_title='Fecha', xaxis_tickformat='%b %Y')
    st.plotly_chart(fig_generacion)


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
    st.write("El intercambio internacional energético se refiere a la compra y venta de energía " \
            "entre países. En el caso de la electricidad, se trata del flujo de energía eléctrica " \
            "que cruza las fronteras nacionales a través de interconexiones eléctricas.")

    df_intercambio = pd.read_csv('../lib/data/processed/intercambio/fronteras-limpio.csv')
    df_intercambio['fecha'] = pd.to_datetime(df_intercambio['fecha'])
    df_intercambio['año'] = df_intercambio['fecha'].dt.year

    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Año específico"])

    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30])
        fecha_max = df_intercambio['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_intercambio[df_intercambio['fecha'] >= fecha_min]
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_intercambio['año'].unique()))
        df_filtrado = df_intercambio[df_intercambio['año'] == año]

    # Gráfico de líneas por país
    grafico_lineas = df_filtrado.groupby(['fecha', 'pais'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                  x='fecha',
                  y='valor',
                  color='pais',
                  title="Evolución de la exportación de energía por país",
                  labels={'fecha': 'Fecha', 'valor': 'kWh', 'pais': 'País'})
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

    # Grafico heatmap:
    grafico_barras = df_intercambio.groupby(['año', 'pais'])['valor'].sum().reset_index()

    heatmap_data = grafico_barras.pivot(index='año', columns='pais', values='valor')

    fig = px.imshow(heatmap_data,
                    title="Distribución de la exportación de energía por años (Heatmap)",
                    labels={'x': 'Pais', 'y': 'Año', 'color': 'kWh'},
                    color_continuous_scale='Blues')
    st.plotly_chart(fig)

st.sidebar.title('Navegación')
pagina = st.sidebar.radio("", ("Página de Inicio", "Balance", "Demanda", "Generación", "Intercambio"))



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
