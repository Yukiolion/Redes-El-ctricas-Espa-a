import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests

def Generacion(df_generacion):
    st.title("Generación")
    st.write("Definimos la generación como la producción de energía en b.a. (bornes de alternador), " \
    "menos la consumida por los servicios auxiliares y las pérdidas en los transformadores.")

    st.write("**⚙️ Generación de energía Renovable vs No renovable en la región peninsular**")

    df_generacion['fecha'] = pd.to_datetime(df_generacion['fecha'])
    df_generacion['año'] = df_generacion['fecha'].dt.year.astype(str)

    # Colocamos selector para elegir el tipo de visualización:
    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Rango fechas"], key="grafico_generacion")

    # Gráfico de energía renovable vs no renovable
    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30], key="select_dias_generacion")
        fecha_max = df_generacion['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_generacion[df_generacion['fecha'] >= fecha_min]
        tickformat = '%d %b'

        grafico_lineas_generacion = df_filtrado.groupby(['fecha', 'tipo'])['valor'].sum().reset_index()
        fig_generacion = px.line(grafico_lineas_generacion,
                                x='fecha',
                                y='valor',
                                color='tipo',
                                labels={'fecha': 'Fecha', 'valor': 'kWh', 'tipo': 'Tipo de energía'})
        fig_generacion.update_traces(line=dict(width=1))
        fig_generacion.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
        st.plotly_chart(fig_generacion)

    else:
        fecha_min_total = df_generacion['fecha'].min()
        fecha_max_total = df_generacion['fecha'].max()
        rango_fechas = st.date_input(
            "Selecciona el rango de fechas:",
            value=(fecha_min_total.date(), fecha_max_total.date()),
            min_value=fecha_min_total.date(),
            max_value=fecha_max_total.date(),
            key="select_rango_generacion")

        if (isinstance(rango_fechas, tuple)
            and len(rango_fechas) == 2
            and rango_fechas[0] is not None
            and rango_fechas[1] is not None):
            fecha_inicio = pd.to_datetime(rango_fechas[0])
            fecha_fin = pd.to_datetime(rango_fechas[1])

            if fecha_inicio <= fecha_fin:
                df_filtrado = df_generacion[
                    (df_generacion['fecha'] >= fecha_inicio) &
                    (df_generacion['fecha'] <= fecha_fin)]
                tickformat = '%b %Y'

                grafico_lineas_generacion = df_filtrado.groupby(['fecha', 'tipo'])['valor'].sum().reset_index()
                fig_generacion = px.line(grafico_lineas_generacion,
                                        x='fecha',
                                        y='valor',
                                        color='tipo',
                                        labels={'fecha': 'Fecha', 'valor': 'kWh', 'tipo': 'Tipo de energía'})
                fig_generacion.update_traces(line=dict(width=1))
                fig_generacion.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
                st.plotly_chart(fig_generacion)

    st.write("Como ya hemos visto en otras gráficas, se puede ver un aumento de la generación de energía renovable. Esto es debido " \
    "a la inversión privada tanto de empresas como de particulares incentivada por el gobierno.")




    st.write("**⚙️ Distribución de tipo de energia por años**")

    # Colocamos selector para elegir las fuentes de energía:
    modo_seleccion = st.radio("Modo de visualización:", options=["Todos", "Seleccionar fuentes energía"], key="grafico_fuentes")
    indicadores_disponibles = df_generacion['indicador'].unique()

    if modo_seleccion == "Todos":
        df_filtrado1 = df_generacion
    else:
        indicadores_seleccionados = st.multiselect(
            "Selecciona uno o varios indicadores:",
            options=sorted(indicadores_disponibles),
            default=sorted(indicadores_disponibles)[:1])
        df_filtrado1 = df_generacion[df_generacion['indicador'].isin(indicadores_seleccionados)]

    grafico_hist = df_filtrado1.groupby(['indicador', 'año'])['valor'].sum().reset_index()

    fig = px.bar(grafico_hist,
                x='año',
                y='valor',
                color='indicador',
                labels={'año': 'Año', 'valor': 'kWh'},
                barmode='group',
                height=600)

    st.plotly_chart(fig)

    st.write("En este gráfico podemos ver la evolución de las diferentes fuentes de energía a lo largo de los años. Podemos" \
    "destacar que, la energía solar fotovoltaica ha aumentado considerablemente pasando de unos 9.200kW a 44.500kW. Tambien se puede " \
    "destacar que la energía del ciclo combinado (que es el respaldo cuando se necesita energía inmediata) aumentó en 2022 " \
    " y si nos fijamos en el valor total de la energía gastada en 2022 es mayor. La energía hidráulica, depende mucho de la meteorología, con lo que " \
    "de acuerdo con eso podemos ver que es muy volátil según años. La energía eólica vemos como ha subido a lo largo de los años al incentivar" \
    "las inversiones en energías renovables. La energía derivada de la cogeneración, disminuye bruscamente a partir del 2019 por la reducción de " \
    "la necesidad de calor debido al cambio climático asumiendo el ciclo combinado como fuente de energía sin la producción de calor. La energía derivada" \
    "de las centrales de carbón aporta cada vez menos debido a las directrices de la Unión Europea.")

    st.write("**⚙️ Comparación de las fuentes de energía a lo largo de los años**")
    
    df_generacion['año'] = df_generacion['fecha'].dt.year
    años_disponibles = list(range(2015, 2025))
    año_1 = st.selectbox("Selecciona el primer año:", años_disponibles, key="año_1_generacion")
    año_2 = st.selectbox("Selecciona el segundo año:", años_disponibles, key="año_2_generacion")

    #st.write(f"Comparando los años: {año_1} vs {año_2}")

    años = [año_1, año_2]
    df_comparar = df_generacion[df_generacion['año'].isin(años)].copy()

    df_comparar['valor'] = pd.to_numeric(df_comparar['valor'], errors='coerce')
    estadisticas_por_año = []

    for año in años:
        valores = df_comparar[df_comparar['año'] == año]['valor']
        #st.dataframe(valores.describe())
        stats = valores.describe()

        media = stats['mean']
        mediana = valores.median()
        minimo = stats['min']
        maximo = stats['max']

        estadisticas_por_año.append({
            'año': año,
            'media': media,
            'mediana': mediana,
            'min': minimo,
            'max': maximo,
        })

    df_estadisticas = pd.DataFrame(estadisticas_por_año)

    st.write("En esta tabla podemos seleccionar los valores de media, mediana, máximo y mínimo y comparar dichos valores entre" \
    "años. En el grafico de debajo se muestran tanto los valores estadísticos como la gráfica de la evolución de la demanda.")

    # Colocamos dataframe con las estadísticas:
    st.dataframe(df_estadisticas)

    df_comparar['indicador_año'] = df_comparar['indicador'] + ' ' + df_comparar['año'].astype(str)

    # Grafico comparativo de los años:
    fig = px.line(df_comparar,
                x='fecha',
                y='valor',
                color='indicador_año',
                labels={'fecha': 'Fecha', 'valor': 'kWh', 'indicador_año': 'Indicador por año'})

    fig = go.Figure(fig)
    colors = {
        'media': 'blue',
        'mediana': 'green',
        'min': 'red',
        'max': 'orange'}
    line_styles = {
        'media': 'solid',
        'mediana': 'dash',
        'min': 'dot',
        'max': 'dashdot'}

    for estadisticas in estadisticas_por_año:
        año = estadisticas['año']
        for tipo in ['media', 'mediana', 'min', 'max']:
            fig.add_hline(y=estadisticas[tipo],
                        line=dict(color=colors[tipo], dash=line_styles[tipo], width=1),
                        annotation_text=f"{tipo.capitalize()} {año}",
                        annotation_position="top left")

    fig.update_layout(
        xaxis_title='Fecha',
        xaxis_tickformat='%b %Y',
        legend_title='Indicador por año'
    )
    fig.update_traces(line=dict(width=1))

    st.plotly_chart(fig)