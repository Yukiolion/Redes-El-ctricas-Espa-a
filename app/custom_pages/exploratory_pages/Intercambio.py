import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests

def Intercambio(df_intercambio):
    st.title("Intercambio Internacional")
    st.write("El intercambio internacional energético se refiere a la compra y venta de energía " \
            "entre países. En el caso de la electricidad, se trata del flujo de energía eléctrica " \
            "que cruza las fronteras nacionales a través de interconexiones eléctricas.")

    df_intercambio['fecha'] = pd.to_datetime(df_intercambio['fecha'])
    df_intercambio['año'] = df_intercambio['fecha'].dt.year.astype(str)

    st.write("**🌍 Evolución de la exportación de energía por país**")

    # Colocamos selector para elegir el tipo de visualización:
    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Rango fechas"])

    # Grafico de lineas
    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30], key="select_dias_intercambio")
        fecha_max = df_intercambio['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_intercambio[df_intercambio['fecha'] >= fecha_min]
        tickformat = '%d %b'

        grafico_lineas = df_filtrado.groupby(['fecha', 'pais'])['valor'].sum().reset_index()
        fig = px.line(grafico_lineas,
                    x='fecha',
                    y='valor',
                    color='pais',
                    labels={'fecha': 'Fecha', 'valor': 'kWh', 'pais': 'País'})
        fig.update_traces(line=dict(width=1))
        fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
        st.plotly_chart(fig)

    else:
        fecha_min_total = df_intercambio['fecha'].min()
        fecha_max_total = df_intercambio['fecha'].max()
        rango_fechas = st.date_input(
            "Selecciona el rango de fechas:",
            value=(fecha_min_total.date(), fecha_max_total.date()),
            min_value=fecha_min_total.date(),
            max_value=fecha_max_total.date(),
            key="select_rango_intercambio")

        if (isinstance(rango_fechas, tuple)
            and len(rango_fechas) == 2
            and rango_fechas[0] is not None
            and rango_fechas[1] is not None):
            fecha_inicio = pd.to_datetime(rango_fechas[0])
            fecha_fin = pd.to_datetime(rango_fechas[1])

            if fecha_inicio <= fecha_fin:
                df_filtrado = df_intercambio[
                    (df_intercambio['fecha'] >= fecha_inicio) &
                    (df_intercambio['fecha'] <= fecha_fin)]
                tickformat = '%b %Y'

                grafico_lineas = df_filtrado.groupby(['fecha', 'pais'])['valor'].sum().reset_index()
                fig = px.line(grafico_lineas,
                            x='fecha',
                            y='valor',
                            color='pais',
                            labels={'fecha': 'Fecha', 'valor': 'kWh', 'pais': 'País'})
                fig.update_traces(line=dict(width=1))
                fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
                st.plotly_chart(fig)

    st.write("Las principales interconexiones de España están con Francia, Portugal y, en menor medida, con Marruecos y Andorra. " \
    "Estas importaciones y exportaciones se realizan principalmente a través de cables submarinos o líneas de alta tensión.")

    st.write("**🌍 Exportacion de energia por años**")

    # Gráfico de barras:
    grafico_barras = df_intercambio.groupby(['año', 'pais'])['valor'].sum().reset_index()
    fig = px.bar(grafico_barras,
                x='año',
                y='valor',
                color='pais',
                labels={'año': 'Año', 'valor': 'kWh'},
                hover_name='pais',
                barmode='stack')
    st.plotly_chart(fig)

    st.write("En este gráfico podemos ver La exportación de electricidad de España entre 2021 y 2022 aumentó significativamente, " \
    "pasando de 16,5 TWh a 25,4 TWh, lo que representa un incremento del 54%. Esto fué debido a la sequía en Portugal que afectó a su " \
    "capacidad de generación hidroeléctrica y a un parón de la energía nuclear en Francia debido a averías y problemas de mantenimiento.")

    st.write("**🌍 Exportacion de energia por años (Heatmap)**")

    # Grafico heatmap:
    
    grafico_barras = df_intercambio.groupby(['año', 'pais'])['valor'].sum().reset_index()
    heatmap_data = grafico_barras.pivot(index='año', columns='pais', values='valor')

    fig = px.imshow(heatmap_data,
                    labels={'x': 'Pais', 'y': 'Año', 'color': 'GWh'},
                    color_continuous_scale='Blues')
    st.plotly_chart(fig)

    st.write("En la gráfica de calor, vemos que las exportaciones a Andorra son bastante estables a lo largo de los años, las de "\
                "Marruecos aumentan poco a poco progresivamente, mientras que Portugal aumentó de manera brusca. Las exportaciones a Francia son las que " \
                "no siguen un patrón definido.")
    



    st.write("**🌍 Exportación de energía por años (Mapa coropletico)**")

    # Agrupar por año y país
    exportaciones_year = df_intercambio.groupby(['año', 'pais'])['valor'].sum().reset_index()

    # Colocamos selector para elegir el tipo de visualización:
    year = st.selectbox("Selecciona un año:", sorted(exportaciones_year['año'].unique()), key="mapa_año")

    # Filtrar solo el año seleccionado y colocar los nombres por ISO:
    exportaciones_filtradas = exportaciones_year[exportaciones_year['año'] == year].copy()

    exportaciones_filtradas['pais'] = exportaciones_filtradas['pais'].replace({
        'francia-frontera': 'FRA',
        'portugal-frontera': 'PRT',
        'marruecos-frontera': 'MAR',
        'andorra-frontera': 'AND'})

    # Escalar a GWh
    exportaciones_filtradas['valor'] = exportaciones_filtradas['valor'] / 1000

    # Mapa coropletico con selección por año
    fig = px.choropleth(
        exportaciones_filtradas,
        locations='pais',
        locationmode='ISO-3',
        color='valor',
        hover_name='pais',
        color_continuous_scale='RdYlBu',
        range_color=[0, exportaciones_year['valor'].max() / 1000],
        labels={'valor': 'GWh'},)

    fig.update_geos(
        visible=True,
        resolution=50,
        projection_type="natural earth",
        lataxis_range=[20, 60],
        lonaxis_range=[-20, 10])
    fig.update_layout(
        height=700,)
    st.plotly_chart(fig)



    
    st.write("**🌍 Exportación de energía anual per cápita**")

    # Grafico de energia per capita:
    df_energia_total = pd.read_csv('app/data/energia_per_capita.csv')
    
    fig_energia = px.line(
        df_energia_total,
        x="año",
        y="energia_per_capita",
        color="pais",
        markers=True,
        labels={"energia_per_capita": "MWh/persona", "año": "Año", "pais": "País"})

    fig_energia.update_layout(
        legend_title_text="País destino",
        hovermode="x unified",
        template="plotly_white")

    st.plotly_chart(fig_energia)

    st.write("- Marruecos: Tiende a mostrar valores per cápita muy pequeños.\n" \
        "- Francia: Tiende a tener altos volúmenes de energía exportada y una población grande, por lo que la "
            "energía per cápita exportada puede parecer moderada. \n" \
            "- Portugal: Con este país hay acuerdos de exportación en crecimiento, por eso se puede ver una subida per cápita constante.\n" \
            "- Andorra: Tiene una población muy baja (~77 mil habitantes), por lo que cualquier cantidad de energía exportada "
            "se traduce en un valor per cápita muy alto. Es probable que presente los valores más altos per cápita, "
            "aunque el volumen total sea pequeño.\n")
    
    st.write("**🌍 Comparación de la exportación eléctrica a lo largo de los años**")

    df_intercambio['año'] = df_intercambio['fecha'].dt.year
    años_disponibles = list(range(2015, 2025))
    año_1 = st.selectbox("Selecciona el primer año:", años_disponibles, key="año_1_intercambio")
    año_2 = st.selectbox("Selecciona el segundo año:", años_disponibles, key="año_2_intercambio")

    #st.write(f"Comparando los años: {año_1} vs {año_2}")

    años = [año_1, año_2]
    df_comparar = df_intercambio[df_intercambio['año'].isin(años)]

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
    "años. En el gráfico de debajo se muestran tanto los valores estadísticos como la gráfica de la evolución de la demanda.")

    # Colocamos dataframe con las estadísticas:
    st.dataframe(df_estadisticas)

    # Corregir la creación de la columna 'indicador_año', en lugar de 'indicador' usa algún criterio:
    # Aquí puedes usar una columna existente o asignar un valor fijo si no tienes una columna 'indicador'
    # Ejemplo: Si quieres que todos los valores tengan el mismo "indicador", puedes asignar un texto fijo.
    df_comparar['indicador_año'] = 'Indicador ' + df_comparar['año'].astype(str)

    # Si quieres usar alguna columna existente como 'tipo' o cualquier otra, puedes hacerlo:
    # df_comparar['indicador_año'] = df_comparar['tipo'] + ' ' + df_comparar['año'].astype(str)

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