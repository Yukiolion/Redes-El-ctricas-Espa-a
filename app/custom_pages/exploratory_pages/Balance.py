import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests
import calendar


def Balance(df_balance):
    st.title("Balance Eléctrico")
    st.write("En este apartado se representa la cantidad total de electricidad generada por todas las fuentes disponibles " \
            "en el sistema eléctrico Español a lo largo de los años.")
    
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.write("**🔄 Evolución del balance a lo largo de los años**")

    df_balance['fecha'] = pd.to_datetime(df_balance['fecha'])
    df_balance['año'] = df_balance['fecha'].dt.year

    # Colocamos selector para elegir el tipo de visualización:
    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Rango fechas"], key="grafico_balance")

    # Gráfico de líneas
    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30])
        fecha_max = df_balance['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado_evol = df_balance[df_balance['fecha'] >= fecha_min]
        tickformat = '%d %b'

        grafico_lineas = df_filtrado_evol.groupby(['fecha', 'energia'])['valor'].sum().reset_index()
        fig = px.line(
            grafico_lineas,
            x='fecha',
            y='valor',
            color='energia',
            labels={'fecha': 'Fecha', 'valor': 'kWh', 'energia': 'Tipo de energía'})
        fig.update_traces(line=dict(width=1))
        fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
        st.plotly_chart(fig)

    else:
        fecha_min_total = df_balance['fecha'].min()
        fecha_max_total = df_balance['fecha'].max()
        rango_fechas = st.date_input("Selecciona el rango de fechas:",
            value=(fecha_min_total.date(), fecha_max_total.date()),
            min_value=fecha_min_total.date(),
            max_value=fecha_max_total.date())

        if (isinstance(rango_fechas, tuple) and len(rango_fechas) == 2 
            and rango_fechas[0] is not None 
            and rango_fechas[1] is not None):
            fecha_inicio = pd.to_datetime(rango_fechas[0])
            fecha_fin = pd.to_datetime(rango_fechas[1])

            if fecha_inicio <= fecha_fin:
                df_filtrado_evol = df_balance[(df_balance['fecha'] >= fecha_inicio) &
                    (df_balance['fecha'] <= fecha_fin)]
                tickformat = '%b %Y'

                grafico_lineas = df_filtrado_evol.groupby(['fecha', 'energia'])['valor'].sum().reset_index()
                fig = px.line(
                        grafico_lineas,
                        x='fecha',
                        y='valor',
                        color='energia',
                        labels={'fecha': 'Fecha', 'valor': 'kWh', 'energia': 'Tipo de energía'})
                fig.update_traces(line=dict(width=1))
                fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
                st.plotly_chart(fig)

    st.write("En esta gráfica se observa que la energía almacenada es la que menos watios por hora aporta. Tambien podemos observar " \
    "que desde el 2019 al 2024 la energía producida por las fuentes renovables va en aumento. Además se puede ver como se " \
    "equilibra con fuentes no renovables para afrontar la demanda eléctrica.")


    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.write("**🔄 Histograma del balance de electicidad**")

    df_balance['fecha'] = pd.to_datetime(df_balance['fecha'])
    df_balance['año'] = df_balance['fecha'].dt.year
    años_disponibles = sorted(df_balance['año'].unique())

    # Selector para los años:
    año = st.selectbox("Selecciona el año:", años_disponibles, key="select_año_balance")

    df_filtrado_hist = df_balance[df_balance['año'] == año]
    
    # Calculo quantiles:
    df_filtrado_hist = df_filtrado_hist.copy()
    df_filtrado_hist['valor'] = df_filtrado_hist['valor'].astype(float)
    q1 = df_filtrado_hist['valor'].quantile(0.25)
    q3 = df_filtrado_hist['valor'].quantile(0.75)
    iqr = q3 - q1
    valla_inferior = q1 - 1.5 * iqr
    valla_superior = q3 + 1.5 * iqr

    # Histograma
    fig_hist = px.histogram(df_filtrado_hist, 
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
    
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.write("**🔄 Comparación del Balance Eléctrico a lo largo de los años**")


    df_balance = df_balance.groupby(['energia', 'fecha'], as_index=False)['valor'].sum()

    df_balance['año'] = df_balance['fecha'].dt.year

    start_year = df_balance['fecha'].dt.year.min()
    end_year = df_balance['fecha'].dt.year.max()

    años_disponibles = list(range(start_year, end_year + 1))
    año_1 = st.selectbox("Selecciona el primer año:", años_disponibles, key="año_1_balance")
    año_2 = st.selectbox("Selecciona el segundo año:", años_disponibles, key="año_2_balance")

    if año_1 == año_2:
        st.warning("Selecciona dos años diferentes para comparar.")
        st.stop()

    años = [año_1, año_2]

    df_comparar = df_balance[df_balance['año'].isin(años)].copy()
    df_comparar['valor'] = pd.to_numeric(df_comparar['valor'], errors='coerce')
    df_comparar['energia_año'] = df_comparar['energia'] + ' ' + df_comparar['año'].astype(str)

    estadisticas_por_año = []
    for año in años:
        valores = df_comparar[df_comparar['año'] == año]['valor'].dropna()
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
    ver_año_entero = st.checkbox("Comparar el año completo", key="ver_año_intercambio_balance")

    if not ver_año_entero:
        meses_unicos = df_comparar['nombre_mes'].unique().tolist()
        meses_disponibles = [mes for mes in meses if mes in meses_unicos]
        index_default = meses_disponibles.index('Enero') if 'Enero' in meses_disponibles else 0

        mes_seleccionado = st.selectbox(
            "Selecciona el mes a comparar:",
            meses_disponibles,
            index=index_default,
            key="mes_intercambio_balance"
        )

        df_filtrado = df_comparar[df_comparar['nombre_mes'] == mes_seleccionado].copy()
    else:
        df_filtrado = df_comparar.copy()

    df_filtrado['dia_mes'] = df_filtrado['fecha'].dt.strftime('%d-%b')

    mostrar_estadisticas = st.checkbox("Mostrar líneas de media, mediana, máximo y mínimo", key="estadisticas_intercambio_balance")

    if ver_año_entero:
        df_filtrado['dia_del_año'] = df_filtrado['fecha'].dt.dayofyear
        mes_ticks = df_filtrado.groupby(['energia','mes'])['dia_del_año'].min().sort_index()

        fig = px.line(
            df_filtrado,
            x='dia_del_año',
            y='valor',
            color='energia_año',
            labels={'dia_del_año': 'Mes', 'valor': 'kWh', 'energia_año': 'Energia y Año'}
        )

        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=mes_ticks.values,
                ticktext=[m[:3] for m in meses[:len(mes_ticks)]]
            ),
            xaxis_title='Mes',
            yaxis_title='Intercambio (kWh)',
            legend_title='Energia y Año'
        )
    else:
        fig = px.line(
            df_filtrado,
            x='dia',
            y='valor',
            color='energia_año',
            labels={'dia': 'Día', 'valor': 'kWh', 'energia_año': 'Energia y Año'}
        )

        fig.update_layout(
            xaxis=dict(dtick=1),
            xaxis_title='Día del mes',
            yaxis_title='Intercambio (kWh)',
            legend_title='Energia y Año'
        )

    fig.update_traces(line=dict(width=1))

    if mostrar_estadisticas:
        estadisticas_filtradas = []
        for año in años:
            valores = df_filtrado[df_filtrado['año'] == año]['valor'].dropna()
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
