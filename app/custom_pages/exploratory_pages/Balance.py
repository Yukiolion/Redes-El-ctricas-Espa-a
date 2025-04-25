import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests


def Balance(df_balance):
    st.title("Balance Eléctrico")
    st.write("En este apartado se representa la cantidad total de electricidad generada por todas las fuentes disponibles " \
             "en el sistema eléctrico Español a lo largo de los años.")

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
        df_filtrado = df_balance[df_balance['fecha'] >= fecha_min]
        tickformat = '%d %b'

        grafico_lineas = df_filtrado.groupby(['fecha', 'energia'])['valor'].sum().reset_index()
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
                df_filtrado = df_balance[(df_balance['fecha'] >= fecha_inicio) &
                    (df_balance['fecha'] <= fecha_fin)]
                tickformat = '%b %Y'

                grafico_lineas = df_filtrado.groupby(['fecha', 'energia'])['valor'].sum().reset_index()
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


    
    st.write("**🔄 Histograma del balance de electicidad**")
   
    df_balance['fecha'] = pd.to_datetime(df_balance['fecha'])
    df_balance['año'] = df_balance['fecha'].dt.year
    años_disponibles = sorted(df_balance['año'].unique())

    # Selector para los años:
    año = st.selectbox("Selecciona el año:", años_disponibles, key="select_año")

    df_filtrado = df_balance[df_balance['año'] == año]
    
    # Calculo quantiles:
    df_filtrado['valor'] = df_filtrado['valor'].astype(float)
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

    st.write("**⚡ Comparación del Balance eléctrica a lo largo de los años**")

    años_disponibles = list(range(2019, 2025))
    año_1 = st.selectbox("Selecciona el primer año:", años_disponibles, key="año_1_balance")
    año_2 = st.selectbox("Selecciona el segundo año:", años_disponibles, key="año_2_balance")

    st.write(f"Comparando los años: {año_1} vs {año_2}")

    años = [año_1, año_2]
    df_comparar = df_balance[df_balance['año'].isin(años)]

    df_comparar['valor'] = pd.to_numeric(df_comparar['valor'], errors='coerce')
    estadisticas_por_año = []

    for año in años:
        valores = df_comparar[df_comparar['año'] == año]['valor']
        st.dataframe(valores.describe())
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
                title="Evolución de demanda en la región peninsular",
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