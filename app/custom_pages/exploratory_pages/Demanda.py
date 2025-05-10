import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests


def Demanda(df_demanda, df_ire):
    st.title("Demanda Eléctrica")
    st.write("La demanda eléctrica se refiere a la cantidad de electricidad que los consumidores requieren en " \
            " un momento o periodo específico. Es una medida de la cantidad de energía que se necesita para satisfacer las necesidades " \
            "de los usuarios, ya sean residenciales, comerciales o industriales.")

    df_demanda['fecha'] = pd.to_datetime(df_demanda['fecha'])
    df_demanda['año'] = df_demanda['fecha'].dt.year

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.write("**⚡Evolución de demanda en la región peninsular**")

    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Rango fechas"], key="grafico_demanda")

    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30], key="select_dias")
        fecha_max = df_demanda['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado_dem = df_demanda[df_demanda['fecha'] >= fecha_min]
        tickformat = '%d %b'

        grafico_lineas = df_filtrado_dem.groupby(['fecha', 'indicador'])['valor'].sum().reset_index()
        fig = px.line(grafico_lineas,
                    x='fecha',
                    y='valor',
                    color='indicador',
                    labels={'fecha': 'Fecha', 'valor': 'kWh', 'indicador': 'Tipo de energía'})
        fig.update_traces(line=dict(width=1))
        fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
        st.plotly_chart(fig)
    else:
        fecha_min_total = df_demanda['fecha'].min()
        fecha_max_total = df_demanda['fecha'].max()
        rango_fechas = st.date_input(
            "Selecciona el rango de fechas:",
            value=(fecha_min_total.date(), fecha_max_total.date()),
            min_value=fecha_min_total.date(),
            max_value=fecha_max_total.date(),
            key="select_rango_demanda")

        if (isinstance(rango_fechas, tuple) and len(rango_fechas) == 2
            and rango_fechas[0] is not None
            and rango_fechas[1] is not None):
            fecha_inicio = pd.to_datetime(rango_fechas[0])
            fecha_fin = pd.to_datetime(rango_fechas[1])

            if fecha_inicio <= fecha_fin:
                df_filtrado_dem = df_demanda[(df_demanda['fecha'] >= fecha_inicio) &
                    (df_demanda['fecha'] <= fecha_fin)]
                tickformat = '%b %Y'

                grafico_lineas = df_filtrado_dem.groupby(['fecha', 'indicador'])['valor'].sum().reset_index()
                fig = px.line(grafico_lineas,
                            x='fecha',
                            y='valor',
                            color='indicador',
                            labels={'fecha': 'Fecha', 'valor': 'kWh', 'indicador': 'Tipo de energía'})
                fig.update_traces(line=dict(width=1))
                fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
                st.plotly_chart(fig)
    st.write("En esta grafica se observa que la demanda energética sigue unos patrones mas o menos estables a lo largo" \
    "de los años, los meses donde más aumnenta son los de enero y los de julio, coincidiendo con las épocas mas frias y mas calurosas" \
    "de la península.")
    

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.write("**⚡Índice de Red Eléctrica (IRE)**")
    st.write("El IRE es el indicador eléctrico adelantado que recoge la evolución " \
            " del consumo de energía eléctrica de las empresas que tienen un consumo de energía eléctrica " \
            " de tamaño medio/alto (potencia contratada superior a 450 kW). Al revisar los valores del IRE tenemos que tener en " \
            "cuenta algunos conceptos clave:\n"
            "- **Ire**: Es el índice tal cual se calcula a partir de los datos reales de consumo eléctrico, sin ningún tipo de ajuste. " \
            " Es decir, refleja la evolución bruta de la demanda eléctrica respecto al mismo mes del año anterior y puede estar afectado por " \
            "factores externos como el tiempo o las festividades.\n"
            "- **Ire Corregido**: Se ajustan los valores para eliminar los efectos de las festividades (si un mes tiene mas fines de semana o feriados)" \
            "y la temperatura para realizar comparaciones mas justas entre periodos.\n")
    st.write("Por otra parte, tenemos tres tipos de IRE:\n" \
            "- **Ire General**: Es el índice que representa la evolución total de la demanda eléctrica nacional (en España) para una determinada fecha o periodo," \
            " comparado con el mismo periodo del año anterior. Incluye todos los sectores: industrial, servicios y doméstico. \n" \
            "- **Ire Industria**: Este mide específicamente la demanda eléctrica de la industria. Es un buen indicador de la actividad industrial del país, " \
            "ya que si las fábricas consumen más electricidad, suele ser porque están produciendo más.\n" \
            "- **Ire Servicios**: Refleja el consumo eléctrico del sector servicios (oficinas, comercios, hoteles, hospitales, etc.). Puede estar influenciado " \
            "por la actividad económica y también por factores estacionales como el turismo o el clima.")
    # Creamos un filtro para los datos de IRE
    df_ire['fecha'] = pd.to_datetime(df_ire['fecha'])
    df_ire['año'] = df_ire['fecha'].dt.year
    filtro = df_ire['indicador'].isin(['Índice general corregido', 'Índice industria corregido', 'Índice servicios corregido'])
    df_ire_reducido = df_ire[filtro]
    
    # Hacemos un selectbox para elegir el año
    # y luego mostrar el gráfico
    año = st.selectbox("Selecciona el año:", sorted(df_ire['año'].unique()), key="select_año2")
    tickformat = '%b %Y'
    df_ire_filtrado = df_ire[df_ire['año'] == año]



    grafico_lineas = df_ire_filtrado.groupby(['fecha', 'indicador'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                x='fecha',
                y='valor',
                color='indicador',
                title="Evolución de ire de demanda en la región peninsular",
                labels={'fecha': 'Fecha', 'valor': 'kWh', 'indicador': 'Tipo de energía'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
    st.plotly_chart(fig)

    st.write("En la grafica podemos observar que el IRE Servicios despunta en Julio haciendo aumentar el IRE General y el IRE Industria es el que más bajo está " \
    "en agosto, cuadrando con el periodo vacacional. Además, a partir de marzo de 2020 todos los valores se desploman debido a la pandemia.")

    df_ire['año'] = df_ire['fecha'].dt.year.astype(str)
    df_ire_reducido = df_ire[filtro]
    df_agrupado = df_ire_reducido.groupby(['año', 'indicador'])['valor'].sum().reset_index()
    fig = px.bar(df_agrupado,
                x='año',
                y='valor',
                color='indicador',
                title="Distribución de los tipos de ire por años",
                labels={'valor': 'kWh', 'indicador': 'indices'})
    fig.update_layout(xaxis_title='Año', xaxis_tickformat='%Y')
    st.plotly_chart(fig)
    st.write("Este gráfico muestra una visión general de los diferentes IRE a lo largo de los años.")

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.write("**⚡ Comparación de la Demanda Eléctrica a lo largo de los años**")
    
    inicio_año = df_demanda['fecha'].dt.year.min()
    final_año = df_demanda['fecha'].dt.year.max()
    años_disponibles = list(range(inicio_año, final_año + 1))
    año_1 = st.selectbox("Selecciona el primer año:", años_disponibles, key="año_1.1_balance")
    año_2 = st.selectbox("Selecciona el segundo año:", años_disponibles, key="año_2.1_balance")
    años = [año_1, año_2]
    df_comparar = df_demanda[df_demanda['año'].isin(años)].copy()
    df_comparar['valor'] = pd.to_numeric(df_comparar['valor'], errors='coerce')
    estadisticas_por_año = []
    for año in años:
        valores = df_comparar[df_comparar['año'] == año]['valor']
        estadisticas = valores.describe()
        media = estadisticas['mean']
        mediana = valores.median()
        minimo = estadisticas['min']
        maximo = estadisticas['max']
        estadisticas_por_año.append({
            'año': año,
            'media': media,
            'mediana': mediana,
            'min': minimo,
            'max': maximo,})

    df_estadisticas = pd.DataFrame(estadisticas_por_año)
    st.write("En esta tabla podemos seleccionar los valores de media, mediana, máximo y mínimo y comparar dichos valores entre" \
    " años.")
    st.dataframe(df_estadisticas)

    df_comparar['indicador_año'] = 'Indicador ' + df_comparar['año'].astype(str)
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    df_comparar['mes'] = df_comparar['fecha'].dt.month
    df_comparar['dia'] = df_comparar['fecha'].dt.day
    df_comparar['nombre_mes'] = df_comparar['mes'].apply(lambda x: meses[x-1])
    st.write("Con este gráfico podemos comparar el valor del balance mes a mes o el año completo para cada uno de los años seleccionados.")

    ver_año_entero = st.checkbox("Comparar el año completo", key="año_demanda")

    if not ver_año_entero:
        meses_unicos = df_comparar['nombre_mes'].unique().tolist()
        meses_disponibles = [mes for mes in meses if mes in meses_unicos]
        index_norm = meses_disponibles.index('Enero') if 'Enero' in meses_disponibles else 0
        mes_seleccionado = st.selectbox("Selecciona el mes a comparar:",
            meses_disponibles,
            index=index_norm, key="comparar_mes")
        df_filtrado = df_comparar[df_comparar['nombre_mes'] == mes_seleccionado]

    else:
        df_filtrado = df_comparar.copy()
    mostrar_estadisticas = st.checkbox("Mostrar líneas de media, mediana, máximo y mínimo", key="estadisticas_demanda")

    df_filtrado['dia_mes'] = df_filtrado['fecha'].dt.strftime('%d-%b')

    if ver_año_entero:
        df_filtrado['mes'] = df_filtrado['fecha'].dt.month
        df_filtrado['dia_del_año'] = df_filtrado['fecha'].dt.dayofyear
        df_filtrado['indicador_año'] = 'Demanda ' + df_filtrado['año'].astype(str)
        mes_selec = df_filtrado.groupby('mes')['dia_del_año'].min().sort_index()

        fig = px.line(df_filtrado,
            x='dia_del_año',
            y='valor',
            color='indicador_año',
            labels={'dia_del_año': 'Mes', 'valor': 'kWh', 'indicador_año': 'Año'})

        fig.update_layout(
            xaxis=dict(tickmode='array',
                tickvals=mes_selec.values,
                ticktext=meses[:len(mes_selec)]),
            xaxis_title='Mes',
            yaxis_title='Demanda (kWh)',
            legend_title='Año')
        
    else:
        df_filtrado = df_filtrado[df_filtrado['nombre_mes'] == mes_seleccionado]
        df_filtrado['indicador_año'] = 'Demanda ' + df_filtrado['año'].astype(str)

        fig = px.line(
            df_filtrado,
            x='dia',
            y='valor',
            color='indicador_año',
            labels={'dia': 'Días', 'valor': 'kWh', 'indicador_año': 'Año'})

        fig.update_layout(
            xaxis=dict(dtick=1),
            xaxis_title='Día del mes',
            yaxis_title='Demanda (kWh)',
            legend_title='Año')

    fig.update_traces(line=dict(width=2))

    estadisticas_filtradas = []
    for año in años:
        valores = df_filtrado[df_filtrado['año'] == año]['valor']
        estadisticas = valores.describe()

        estadisticas_filtradas.append({
            'año': año,
            'media': estadisticas['mean'],
            'mediana': valores.median(),
            'min': estadisticas['min'],
            'max': estadisticas['max']})

    if mostrar_estadisticas:
        colors = {'media': 'blue', 'mediana': 'green', 'min': 'red', 'max': 'orange'}
        line_styles = {'media': 'solid', 'mediana': 'dash', 'min': 'dot', 'max': 'dashdot'}

        for est in estadisticas_filtradas:
            año = est['año']
            for tipo in ['media', 'mediana', 'min', 'max']:
                fig.add_hline(y=est[tipo],
                    line=dict(color=colors[tipo], dash=line_styles[tipo], width=1),
                    annotation_text=f"{tipo.capitalize()} {año}",
                    annotation_position="top left")

    st.plotly_chart(fig)