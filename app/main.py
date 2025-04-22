import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests


# PAGINA PRINCIPAL DEL PROYECTO(TITULO, IMAGEN Y DESCRIPCION)
def main():
    st.title("Proyecto Red Eléctrica España")

    st.image("images/Red_Eléctrica_de_España_(logo).png", width=600)

    st.write("El objetivo principal de este proyecto es extraer, procesar y visualizar datos energéticos de la web de Red Eléctrica de España (REE), " \
    "relacionados con la demanda eléctrica, el balance energético, la generación y los intercambios internacionales de energía. Esto permite visualizar " \
    "y analizar cómo se comporta el sistema eléctrico español en distintos momentos del día y del año.")

    st.write('Definicion de los datos:')
    # Esto es un selectbox que permite seleccionar entre los diferentes tipos de datos que tenemos
    # y muestra una breve descripcion de cada uno de ellos
    opcion = st.selectbox('Seleccionar los datos:', 
                                   ('Balance', 'Demanda', 'Generación', 'Intercambio'))
    if opcion == 'Balance':
        st.info("🔄 El **balance energético** representa la diferencia entre la energía generada y la consumida.")
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
            "- Otras renovables (biogás, biomasa, hidráulica marina y geotérmica)\n"
            "- Generación renovable\n"
            "- Turbinación bombeo\n"
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

    st.write("**🔄 Evolución del balance a lo largo de los años**")
    df_balance['fecha'] = pd.to_datetime(df_balance['fecha'])
    df_balance['año'] = df_balance['fecha'].dt.year

    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Año específico"])

    # Gráfico de líneas filtrado
    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30])
        fecha_max = df_balance['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_balance[df_balance['fecha'] >= fecha_min]
        tickformat = '%d %b'
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_balance['año'].unique()))
        df_filtrado = df_balance[df_balance['año'] == año]
        tickformat = '%b %Y'

    grafico_lineas = df_filtrado.groupby(['fecha', 'energia'])['valor'].sum().reset_index()
    fig = px.line(grafico_lineas,
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
    año = st.selectbox("Selecciona el año:", años_disponibles, key="select_año")

    df_filtrado = df_balance[df_balance['año'] == año]
    
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


def Demanda():
    st.title("Demanda Eléctrica")
    st.write("La demanda eléctrica se refiere a la cantidad de electricidad que los consumidores requieren en " \
            " un momento o periodo específico. Es una medida de la cantidad de energía que se necesita para satisfacer " \
            " las necesidades de los usuarios, ya sean residenciales, comerciales o industriales.")

    df_demanda = pd.read_csv('../lib/data/processed/demanda/demanda-limpio.csv')
    df_ire = pd.read_csv('../lib/data/processed/demanda/ire-limpio.csv')
    df_demanda['fecha'] = pd.to_datetime(df_demanda['fecha'])
    df_demanda['año'] = df_demanda['fecha'].dt.year

    st.write("**⚡Evolución de demanda en la región peninsular**")

    # Selección del tipo de visualización
    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Año específico"])

    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30], key="select_dias")
        fecha_max = df_demanda['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_demanda[df_demanda['fecha'] >= fecha_min]
        tickformat = '%d %b'
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_demanda['año'].unique()), key="select_año")
        df_filtrado = df_demanda[df_demanda['año'] == año]
        tickformat = '%b %Y'

    
    grafico_lineas = df_filtrado.groupby(['fecha', 'indicador'])['valor'].sum().reset_index()
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
    
    filtro = df_ire['indicador'].isin(['Índice general corregido', 'Índice industria corregido', 'Índice servicios corregido'])
    df_filtrado = df_ire[filtro]

    df_agrupado = df_filtrado.groupby(['año', 'indicador'])['valor'].sum().reset_index()

     # Gráfico de líneas
    
    año = st.selectbox("Selecciona el año:", sorted(df_demanda['año'].unique()), key="select_año2")
    df_filtrado = df_demanda[df_demanda['año'] == año]
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

    grafico_barras = df_agrupado.groupby(['año', 'indicador'])['valor'].sum().reset_index()

    fig = px.bar(grafico_barras,
                x='año',
                y='valor',
                color='indicador',
                title="Distribución de los tipos de ire por años",
                labels={'valor': 'kWh', 'indicador': 'indices'})
    st.plotly_chart(fig)
    st.write("Este gráfico muestra una visión general de los diferentes IRE a lo largo de los años.")

    ## Grafico para comparar dos años:
    st.write("**⚡ Comparación de la demanda eléctrica a lo largo de los años**")

    años_disponibles = list(range(2019, 2025))

    año_1 = st.selectbox("Selecciona el primer año:", años_disponibles, key="año1")
    año_2 = st.selectbox("Selecciona el segundo año:", años_disponibles, key="año2")

    st.write(f"Comparando los años: {año_1} vs {año_2}")

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

    df_comparar['indicador_año'] = df_comparar['indicador'] + ' ' + df_comparar['año'].astype(str)

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
    
    st.write("**⚙️ Generación de energía Renovable vs No renovable en la región peninsular**")
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
        tickformat = '%d %b'
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_generacion['año'].unique()), key="select_año")
        df_filtrado = df_generacion[df_generacion['año'] == año]
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
    grafico_barras = df_generacion.groupby(['año', 'tipo'])['valor'].sum().reset_index()

    fig = px.bar(grafico_barras,
                x='año',
                y='valor',
                color='tipo',
                labels={'año': 'Año', 'valor': 'kWh'},
                hover_name='tipo',
                barmode='stack')
    st.plotly_chart(fig)
    st.write("**⚙️ Generación por tipo de energía y años**")
    grafico_hist = df_generacion.groupby(['indicador', 'año'])['valor'].sum().reset_index()

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
  
def intercambio():
    st.title("Intercambio Internacional")
    st.write("El intercambio internacional energético se refiere a la compra y venta de energía " \
            "entre países. En el caso de la electricidad, se trata del flujo de energía eléctrica " \
            "que cruza las fronteras nacionales a través de interconexiones eléctricas.")

    df_intercambio = pd.read_csv('../lib/data/processed/intercambio/fronteras-limpio.csv')
    df_intercambio['fecha'] = pd.to_datetime(df_intercambio['fecha'])
    df_intercambio['año'] = df_intercambio['fecha'].dt.year
    st.write("**🌍 Evolución de la exportación de energía por país**")
    seleccion = st.radio("Elegir tipo de grafico", ["Últimos días", "Año específico"])

    if seleccion == "Últimos días":
        dias = st.selectbox("Selecciona el rango de días:", [7, 14, 30], key="select_dias")
        fecha_max = df_intercambio['fecha'].max()
        fecha_min = fecha_max - pd.Timedelta(days=dias)
        df_filtrado = df_intercambio[df_intercambio['fecha'] >= fecha_min]
        tickformat = '%d %b'
    else:
        año = st.selectbox("Selecciona el año:", sorted(df_intercambio['año'].unique()), key="select_año")
        df_filtrado = df_intercambio[df_intercambio['año'] == año]
        tickformat = '%b %Y'

    # Gráfico de líneas por país
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

    # Grafico heatmap:
    grafico_barras = df_intercambio.groupby(['año', 'pais'])['valor'].sum().reset_index()
    st.write("**🌍 Exportacion de energia por años (Heatmap)**")
    heatmap_data = grafico_barras.pivot(index='año', columns='pais', values='valor')

    fig = px.imshow(heatmap_data,
                    labels={'x': 'Pais', 'y': 'Año', 'color': 'GWh'},
                    color_continuous_scale='Blues')
    st.plotly_chart(fig)

    st.write("En la gráfica de calor, vemos que las exportaciones a Andorra son bastante estables a lo largo de los años, las de "\
             "Marruecos aumentan poco a poco progresivamente, mientras que Portugal aumentó de manera brusca. Las exportaciones a Francia son las que " \
             "no siguen un patrón definido.")
    
    # Mapa coropletico con selección por año
    st.write("**🌍 Exportación de energía por años (Mapa coropletico)**")

    # Agrupar por año y país
    exportaciones_year = df_intercambio.groupby(['año', 'pais'])['valor'].sum().reset_index()

    # Selectbox para elegir el año
    year = st.selectbox("Selecciona un año:", sorted(exportaciones_year['año'].unique()), key="mapa_año")

    # Filtrar solo el año seleccionado
    exportaciones_filtradas = exportaciones_year[exportaciones_year['año'] == year].copy()

    # Reemplazar nombres por ISO
    exportaciones_filtradas['pais'] = exportaciones_filtradas['pais'].replace({
        'francia-frontera': 'FRA',
        'portugal-frontera': 'PRT',
        'marruecos-frontera': 'MAR',
        'andorra-frontera': 'AND'
    })

    # Escalar a GWh
    exportaciones_filtradas['valor'] = exportaciones_filtradas['valor'] / 1000

    # Crear mapa
    fig = px.choropleth(
        exportaciones_filtradas,
        locations='pais',
        locationmode='ISO-3',
        color='valor',
        hover_name='pais',
        color_continuous_scale='RdYlBu',
        range_color=[0, exportaciones_year['valor'].max() / 1000],
        labels={'valor': 'GWh'},
        title=f'Exportación de energía por país en {year}'
    )

    fig.update_geos(
        visible=True,
        resolution=50,
        projection_type="natural earth",
        lataxis_range=[20, 60],
        lonaxis_range=[-20, 10]
    )

    st.plotly_chart(fig)

def database():
        st.title("Estructura base de datos")
        st.write("En esta sección se muestra la estructura de la base de datos utilizada en el proyecto.")
        st.write("La base de datos está dividida en cuatro tablas principales:")
        st.write("- Balance: Contiene información sobre el balance energético.")
        st.write("- Demanda: Contiene información sobre la demanda eléctrica.")
        st.write("- Generación: Contiene información sobre la generación eléctrica.")
        st.write("- Intercambio: Contiene información sobre los intercambios internacionales de energía.")

        st.image('../database/diagrama sql.png' , caption='Diagrama de la base de datos', use_container_width=True)


st.sidebar.title('Navegación')
pagina = st.sidebar.radio("", ("Página de Inicio", "Balance", "Demanda", "Generación", "Intercambio", 'Estructura base de datos'))



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
elif pagina == 'Estructura base de datos':
    database()