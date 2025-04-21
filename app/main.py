import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests


# PAGINA PRINCIPAL DEL PROYECTO(TITULO, IMAGEN Y DESCRIPCION)
def main():
    st.title("Proyecto Red Eléctrica España")

    st.image("Red_Eléctrica_de_España_(logo).png", width=600)

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

    # Gráfico de líneas filtrado
    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30])
        fecha_max = df_balance['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_balance[df_balance['fecha'] >= fecha_min]
        titulo = f"Evolución de balance - Últimos {dias} días"
        tickformat = '%d %b'
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_balance['año'].unique()))
        df_filtrado = df_balance[df_balance['año'] == año]
        titulo = f"Evolución de balance - Año {año}"
        tickformat = '%b %Y'

    grafico_lineas = df_filtrado.groupby(['fecha', 'energia'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                x='fecha',
                y='valor',
                color='energia',
                title="Balance energético en España",
                labels={'fecha': 'Fecha', 'valor': 'KWh', 'energia': 'Tipo de energía'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
    st.plotly_chart(fig)
    st.write("En esta grafica se observa que la energía almacenada es la que menos watios por hora aporta. Tambien podemos observar" \
    "que desde el 2019 al 2024 la energía producida por las fuentes renovables va en aumento. Admemás se puede ver que hay como un " \
    "equilibrio entre fuentes renovables y no renovables para poder hacer frente a la demanda eléctrica.")

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
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30], key="select_dias")
        fecha_max = df_demanda['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_demanda[df_demanda['fecha'] >= fecha_min]
        titulo = f"Evolución de demanda - Últimos {dias} días"
        tickformat = '%d %b'
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_demanda['año'].unique()), key="select_año")
        df_filtrado = df_demanda[df_demanda['año'] == año]
        titulo = f"Evolución de demanda - Año {año}"
        tickformat = '%b %Y'

    
    grafico_lineas = df_filtrado.groupby(['fecha', 'indicador'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                x='fecha',
                y='valor',
                color='indicador',
                title="Evolución de demanda en la región peninsular",
                labels={'fecha': 'Fecha', 'valor': 'Wh', 'indicador': 'Tipo de energía'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
    st.plotly_chart(fig)
    st.write("En esta grafica se observa que la demanda energética sigue unos patrones mas o menos estables a lo largo" \
    "de los años, los meses donde más aumnenta son los de enero y los de julio, coincidiendo con las épocas mas frias y mas calurosas" \
    "de la península.")
    
    st.write("**Gráficas teniendo en cuenta el Índice de Red Eléctrica (IRE)**")
    
    filtro = df_ire['indicador'].isin(['Índice general corregido', 'Índice industria corregido', 'Índice servicios corregido'])
    df_filtrado = df_ire[filtro]

    df_agrupado = df_filtrado.groupby(['año', 'indicador'])['valor'].sum().reset_index()

     # Gráfico de líneas
    
    año = st.selectbox("Selecciona el año:", sorted(df_demanda['año'].unique()), key="select_año2")
    df_filtrado = df_demanda[df_demanda['año'] == año]
    titulo = f"Evolución de demanda - Año {año}"
    tickformat = '%b %Y'

    # 🔧 Filtramos df_ire por el año seleccionado
    df_ire_filtrado = df_ire[df_ire['año'] == año]

    grafico_lineas = df_ire_filtrado.groupby(['fecha', 'indicador'])['valor'].sum().reset_index()

    fig = px.line(grafico_lineas,
                x='fecha',
                y='valor',
                color='indicador',
                title="Evolución de ire de demanda en la región peninsular",
                labels={'fecha': 'Fecha', 'valor': 'Wh', 'indicador': 'Tipo de energía'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
    st.plotly_chart(fig)

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
    st.write("En la grafica podemos observar que el IRE Servicios despunta en Julio haciendo aumentar el IRE General y el IRE Industria es el que más bajo está " \
    "en agosto, cuadrando con el periodo vacacional. Además, a partir de marzo de 2020 todos los valores se desploman debido a la pandemia.")

    grafico_barras = df_agrupado.groupby(['año', 'indicador'])['valor'].sum().reset_index()

    fig = px.bar(grafico_barras,
                x='año',
                y='valor',
                color='indicador',
                title="Distribución de los tipos de ire por años",
                labels={'valor': 'Wh', 'indicador': 'indices'})
    st.plotly_chart(fig)
    st.write("Este gráfico muestra una visión general de los diferentes IRE a lo largo de los años.")

## Grafico para comparar dos años:
    st.write("**Comparación de la demanda eléctrica a lo largo de los años**")

    años_disponibles = list(range(2019, 2025))

    st.title("Comparar dos años")

    # Selección de los dos años a comparar
    año_1 = st.selectbox("Selecciona el primer año:", años_disponibles, key="año1")
    año_2 = st.selectbox("Selecciona el segundo año:", años_disponibles, key="año2")

    # Mostrar la selección
    st.write(f"Comparando los años: {año_1} vs {año_2}")

    # Filtrar los datos para los años seleccionados
    años = [año_1, año_2]
    df_comparar = df_demanda[df_demanda['año'].isin(años)]

    estadisticas_por_año = []

    for año in años:
        valores = df_comparar[df_comparar['año'] == año]['valor']
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

    st.dataframe(df_estadisticas)

    # Añadir una columna combinada para el gráfico
    df_comparar['indicador_año'] = df_comparar['indicador'] + ' ' + df_comparar['año'].astype(str)

    fig = px.line(df_comparar,
                x='fecha',
                y='valor',
                color='indicador_año',
                title="Evolución de demanda en la región peninsular",
                labels={'fecha': 'Fecha', 'valor': 'Wh', 'indicador_año': 'Indicador por año'})

    fig = go.Figure(fig)
    colors = {
        'media': 'blue',
        'mediana': 'green',
        'min': 'red',
        'max': 'orange'
    }
    line_styles = {
        'media': 'solid',
        'mediana': 'dash',
        'min': 'dot',
        'max': 'dashdot'
    }

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



def Generacion():
    st.title("Generación")
    st.write("Definimos la generación como la producción de energía en b.a. (bornes de alternador), " \
    "menos la consumida por los servicios auxiliares y las pérdidas en los transformadores.")

    df_generacion = pd.read_csv('../lib/data/processed/generacion/estructura-generacion-limpio.csv')
    df_generacion['fecha'] = pd.to_datetime(df_generacion['fecha'])
    df_generacion['año'] = df_generacion['fecha'].dt.year

    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Año específico"])

    

    # Gráfico de energía renovable vs no renovable
    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30], key="select_dias")
        fecha_max = df_generacion['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_generacion[df_generacion['fecha'] >= fecha_min]
        titulo = f"Evolución de la generación de energía - Últimos {dias} días"
        tickformat = '%d %b'
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_generacion['año'].unique()), key="select_año")
        df_filtrado = df_generacion[df_generacion['año'] == año]
        titulo = f"Evolución de la generación de energía - Año {año}"
        tickformat = '%b %Y'

    grafico_lineas_generacion = df_filtrado.groupby(['fecha', 'tipo'])['valor'].sum().reset_index()
    fig_generacion = px.line(grafico_lineas_generacion,
                             x='fecha',
                             y='valor',
                             color='tipo',
                             title="Generación de energía Renovable vs No renovable en la región peninsular",
                             labels={'fecha': 'Fecha', 'valor': 'kWh', 'tipo': 'Tipo de energía'})
    fig_generacion.update_traces(line=dict(width=1))
    fig_generacion.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
    st.plotly_chart(fig_generacion)

    st.write("Como ya hemos visto en otras gráficas, se puede ver un aumento de la generación de energía renovable. Esto es debido " \
    "a la inversión privada tanto de empresas como de particulares incentivada por el gobierno.")

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
                x='año',
                y='valor',
                color='indicador',  
                title='Generación por tipo de energía y año',
                barmode='group',
                height=600)
    st.plotly_chart(fig)

    st.write("En este grafico podemos ver la evolución de las diferentes fuentes de energía a lo largo de los años. Podemos" \
    "destacar que, la energía solar fotovoltaica ha aumentado considerablemente pasando de unos 9.200kW a 44.500kW. Tambien se puede " \
    "destacar que la energía del ciclo combiando aumentó en 2022 (que es el respaldo cuando se necesita energía inmediata)" \
    " y si nos fijamos en el valor total de la energía gastada en 2022 es mayor. La energía hidráulica, depende mucho de la meteorología, con lo que " \
    "de acuerdo con eso podemos ver que es muy volátil según años. La energía eólica vemos como ha subido a lo largo de los años al incentivar" \
    "las inversiones en energías renovables. La energía derivada de la cogeneración, disminuye bruscamente a partir del 2019 por la reducción de " \
    "la necesidad de calor debido al cambio climático asumiendo el ciclo combinado como fuente de energía sin la producción de calor. La energía derivada" \
    "de las centrales de carbón aporta cada vez menos debido a las directrices de la Unión Europea.")
  
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
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30], key="select_dias")
        fecha_max = df_intercambio['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_intercambio[df_intercambio['fecha'] >= fecha_min]
        titulo = f"Evolución de la generación de energía - Últimos {dias} días"
        tickformat = '%d %b'
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_intercambio['año'].unique()), key="select_año")
        df_filtrado = df_intercambio[df_intercambio['año'] == año]
        titulo = f"Evolución de la generación de energía - Año {año}"
        tickformat = '%b %Y'

    # Gráfico de líneas por país
    grafico_lineas = df_filtrado.groupby(['fecha', 'pais'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
                  x='fecha',
                  y='valor',
                  color='pais',
                  title="Evolución de la exportación de energía por país",
                  labels={'fecha': 'Fecha', 'valor': 'kWh', 'pais': 'País'})
    fig.update_traces(line=dict(width=1))
    fig.update_layout(xaxis_title='Fecha', xaxis_tickformat=tickformat)
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
