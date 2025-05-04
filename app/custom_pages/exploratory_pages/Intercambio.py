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
    
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
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

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

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

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
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
    
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
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
            "se traduce en un valor per cápita muy alto.\n")
    
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.write("**🌍 Comparación de la exportación eléctrica a lo largo de los años**")

    df_intercambio['año'] = df_intercambio['fecha'].dt.year

    start_year = df_intercambio['fecha'].dt.year.min()
    end_year = df_intercambio['fecha'].dt.year.max()

    años_disponibles = list(range(start_year, end_year + 1))
    año_1 = st.selectbox("Selecciona el primer año:", años_disponibles, key="año_1_intercambio")
    año_2 = st.selectbox("Selecciona el segundo año:", años_disponibles, key="año_2_intercambio")
    años = [año_1, año_2]

    df_comparar = df_intercambio[df_intercambio['año'].isin(años)].copy()
    df_comparar['valor'] = pd.to_numeric(df_comparar['valor'], errors='coerce')
    df_comparar['pais_año'] = df_comparar['pais'] + ' ' + df_comparar['año'].astype(str)

    estadisticas_por_año = []
    for año in años:
        valores = df_comparar[df_comparar['año'] == año]['valor']
        stats = valores.describe()

        estadisticas_por_año.append({
            'año': año,
            'media': stats['mean'],
            'mediana': valores.median(),
            'min': stats['min'],
            'max': stats['max']
        })

    df_estadisticas = pd.DataFrame(estadisticas_por_año)

    st.write("Estadísticas generales por año:")
    st.dataframe(df_estadisticas)

    df_comparar['mes'] = df_comparar['fecha'].dt.month
    df_comparar['dia'] = df_comparar['fecha'].dt.day
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    df_comparar['nombre_mes'] = df_comparar['mes'].apply(lambda x: meses[x - 1])

    st.write("Comparación del intercambio eléctrico por país entre los años seleccionados.")
    ver_año_entero = st.checkbox("Comparar el año completo", key="ver_año_intercambio")

    if not ver_año_entero:
        meses_unicos = df_comparar['nombre_mes'].unique().tolist()
        meses_disponibles = [mes for mes in meses if mes in meses_unicos]
        index_default = meses_disponibles.index('Enero') if 'Enero' in meses_disponibles else 0

        mes_seleccionado = st.selectbox(
            "Selecciona el mes a comparar:",
            meses_disponibles,
            index=index_default,
            key="mes_intercambio"
        )

        df_filtrado = df_comparar[df_comparar['nombre_mes'] == mes_seleccionado].copy()
    else:
        df_filtrado = df_comparar.copy()

    df_filtrado['dia_mes'] = df_filtrado['fecha'].dt.strftime('%d-%b')

    mostrar_estadisticas = st.checkbox("Mostrar líneas de media, mediana, máximo y mínimo", key="estadisticas_intercambio")

    if ver_año_entero:
        df_filtrado['dia_del_año'] = df_filtrado['fecha'].dt.dayofyear

        mes_ticks = df_filtrado.groupby('mes')['dia_del_año'].min().sort_index()

        fig = px.line(
            df_filtrado,
            x='dia_del_año',
            y='valor',
            color='pais_año',
            labels={'dia_del_año': 'Mes', 'valor': 'kWh', 'pais_año': 'País y Año'}
        )

        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=mes_ticks.values,
                ticktext=meses[:len(mes_ticks)]
            ),
            xaxis_title='Mes',
            yaxis_title='Intercambio (kWh)',

            legend_title='País y Año'
        )
    else:
        fig = px.line(
            df_filtrado,
            x='dia',
            y='valor',
            color='pais_año',
            labels={'dia': 'Día', 'valor': 'kWh', 'pais_año': 'País y Año'}
        )

        fig.update_layout(
            xaxis=dict(dtick=1),
            xaxis_title='Día del mes',
            yaxis_title='Intercambio (kWh)',
            legend_title='País y Año'
        )

    fig.update_traces(line=dict(width=2))

    if mostrar_estadisticas:
        estadisticas_filtradas = []
        for año in años:
            valores = df_filtrado[df_filtrado['año'] == año]['valor']
            stats = valores.describe()
            estadisticas_filtradas.append({
                'año': año,
                'media': stats['mean'],
                'mediana': valores.median(),
                'min': stats['min'],
                'max': stats['max']
            })

        colors = {'media': 'blue', 'mediana': 'green', 'min': 'red', 'max': 'orange'}
        line_styles = {'media': 'solid', 'mediana': 'dash', 'min': 'dot', 'max': 'dashdot'}

        for est in estadisticas_filtradas:
            año = est['año']
            for tipo in ['media', 'mediana', 'min', 'max']:
                fig.add_hline(
                    y=est[tipo],
                    line=dict(color=colors[tipo], dash=line_styles[tipo], width=1),
                    annotation_text=f"{tipo.capitalize()} {año}",
                    annotation_position="top left"
                )

    st.plotly_chart(fig)