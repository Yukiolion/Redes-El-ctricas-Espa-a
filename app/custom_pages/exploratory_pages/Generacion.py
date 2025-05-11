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

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.write("**⚙️ Generación de energía Renovable vs No renovable en la región peninsular**")

    df_generacion['fecha'] = pd.to_datetime(df_generacion['fecha'])
    df_generacion['año'] = df_generacion['fecha'].dt.year.astype(str)

    # Colocamos selector para elegir el tipo de visualización:
    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Rango fechas"], key="grafico_generacion")

    # Gráfico de líneas para la opción de últimos días:
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

    # Gráfico de líneas para la opción de rango de fechas:
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



    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.write("**⚙️ Distribución de tipo de energia por años**")

    # Seleccionamos por todas o las mas importantes:
    modo_seleccion = st.radio("Modo de visualización:", options=["Todos", "Las más importantes"], key="grafico_fuentes")
    
    indicadores_importantes = [
        "Solar fotovoltaica",
        "Carbón",
        "Ciclo combinado",
        "Hidráulica",
        "Eólica",
        "Cogeneración"
    ]

    # Seleccionamos todas:
    if modo_seleccion == "Todos":
        df_filtrado1 = df_generacion

    # Seleccionamos las mas importantes:
    else:
        df_filtrado1 = df_generacion[df_generacion['indicador'].isin(indicadores_importantes)]

    grafico_hist = df_filtrado1.groupby(['indicador', 'año'])['valor'].sum().reset_index()

    fig = px.bar(
        grafico_hist,
        x='año',
        y='valor',
        color='indicador',
        labels={'año': 'Año', 'valor': 'kWh'},
        barmode='group',
        height=600
    )

    st.plotly_chart(fig)

    st.write("En este gráfico podemos ver la evolución de las diferentes fuentes de energía a lo largo de los años. Podemos" \
    "destacar que, la energía solar fotovoltaica ha aumentado considerablemente pasando de unos 9.200kW a 44.500kW. Tambien se puede " \
    "destacar que la energía del ciclo combinado (que es el respaldo cuando se necesita energía inmediata) aumentó en 2022 " \
    " y si nos fijamos en el valor total de la energía gastada en 2022 es mayor. La energía hidráulica, depende mucho de la meteorología, con lo que " \
    "de acuerdo con eso podemos ver que es muy volátil según años. La energía eólica vemos como ha subido a lo largo de los años al incentivar" \
    "las inversiones en energías renovables. La energía derivada de la cogeneración, disminuye bruscamente a partir del 2019 por la reducción de " \
    "la necesidad de calor debido al cambio climático asumiendo el ciclo combinado como fuente de energía sin la producción de calor. La energía derivada" \
    "de las centrales de carbón aporta cada vez menos debido a las directrices de la Unión Europea.")

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.write("**⚙️ Comparación de las fuentes de energía a lo largo de los años**")
    
    df_generacion['año'] = df_generacion['fecha'].dt.year
    
    start_year = df_generacion['fecha'].dt.year.min()
    end_year = df_generacion['fecha'].dt.year.max()

    años_disponibles = list(range(start_year, end_year + 1))
    año_1 = st.selectbox("Selecciona el primer año:", años_disponibles, key="año_1_generacion")
    año_2 = st.selectbox("Selecciona el segundo año:", años_disponibles, key="año_2_generacion")

    años = [año_1, año_2]
    df_comparar = df_generacion[df_generacion['año'].isin(años)].copy()

    df_comparar['valor'] = pd.to_numeric(df_comparar['valor'], errors='coerce')
    
    # Hacemos la tabla de estadísticas:
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

    st.write("En esta tabla podemos seleccionar los valores de media, mediana, máximo y mínimo y comparar dichos valores entre" \
    "años. En el grafico de debajo se muestran tanto los valores estadísticos como la gráfica de la evolución de la demanda.")

    st.dataframe(df_estadisticas)

    df_comparar['indicador_año'] = df_comparar['indicador'] + ' ' + df_comparar['año'].astype(str)

    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    fig = px.line(df_comparar,
                x='fecha',
                y='valor',
                color='indicador_año',
                labels={'fecha': 'Fecha', 'valor': 'kWh', 'indicador_año': 'Indicador por año'})

    df_comparar['mes'] = df_comparar['fecha'].dt.month
    df_comparar['dia'] = df_comparar['fecha'].dt.day
    df_comparar['nombre_mes'] = df_comparar['mes'].apply(lambda x: meses[x-1])

    st.write("Con este gráfico podemos comparar el valor de generación mes a mes o el año completo para cada uno de los años seleccionados.")

    ver_año_entero = st.checkbox("Comparar el año completo", key="ver_año_entero_generacion")

    # Comparamos por meses:
    if not ver_año_entero:
        meses_unicos = df_comparar['nombre_mes'].unique().tolist()
        meses_disponibles = [mes for mes in meses if mes in meses_unicos]
        index_default = meses_disponibles.index('Enero') if 'Enero' in meses_disponibles else 0

        mes_seleccionado = st.selectbox("Selecciona el mes a comparar:", meses_disponibles, index=index_default, key="comparar_mes_generacion")
        df_filtrado = df_comparar[df_comparar['nombre_mes'] == mes_seleccionado]
    else:
        df_filtrado = df_comparar.copy()

    mostrar_estadisticas = st.checkbox("Mostrar líneas de media, mediana, máximo y mínimo", key="estadisticas_generacion")

    df_filtrado['dia_mes'] = df_filtrado['fecha'].dt.strftime('%d-%b')

    # Comparamos por años completos
    if ver_año_entero:
        df_filtrado['mes'] = df_filtrado['fecha'].dt.month
        df_filtrado['dia_del_año'] = df_filtrado['fecha'].dt.dayofyear
        df_filtrado['indicador_año'] = df_filtrado['indicador'] + ' ' + df_filtrado['año'].astype(str)

        mes_ticks = df_filtrado.groupby('mes')['dia_del_año'].min().sort_index()

        fig = px.line(
            df_filtrado,
            x='dia_del_año',
            y='valor',
            color='indicador_año',
            labels={'dia_del_año': 'Mes', 'valor': 'kWh', 'indicador_año': 'Fuente por año'}
        )

        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=mes_ticks.values,
                ticktext=meses[:len(mes_ticks)]
            ),
            xaxis_title='Mes',
            yaxis_title='Generación (kWh)',
            legend_title='Fuente por año'
        )
    else:
        df_filtrado['indicador_año'] = df_filtrado['indicador'] + ' ' + df_filtrado['año'].astype(str)

        fig = px.line(
            df_filtrado,
            x='dia',
            y='valor',
            color='indicador_año',
            labels={'dia': 'Día', 'valor': 'kWh', 'indicador_año': 'Fuente por año'}
        )

        fig.update_layout(
            xaxis=dict(dtick=1),
            xaxis_title='Día del mes',
            yaxis_title='Generación (kWh)',
            legend_title='Fuente por año'
        )

    fig.update_traces(line=dict(width=2))

    # Lineas estadísticas:
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

    if mostrar_estadisticas:
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