import streamlit as st

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

# AÑADIR LOS DATOS DE CADA UNA DE LAS SECCIONES EN LA FUNCION CORRESPONDIENTE
def Balance():
    st.title("Balance Energético")
    st.write("Aquí se agregaran los datos y graficas del balance energético de España.")

def Demanda():
    st.title("Demanda Eléctrica")
    st.write("Aquí se agregaran los datos y graficas de la demanda eléctrica de España.")

def Generacion():
    st.title("Generación Eléctrica")
    st.write("Aquí se agregaran los datos y graficas de la generación eléctrica de España.")
  
def intercambio():
    st.title("Intercambio Internacional")
    st.write("Aquí se agregaran los datos y graficas de intercambio internacional de energía de España.")

# ESTA FUNCION SE PUEDE USAR COMO CONCLUSIONES O COMO COMPARACIONES PARA COMPARAR DATOS ENTRE LOS TIPOS QUE TENEMOS
def Conclusiones():
    st.title("Conclusiones de Datos")
    st.write("Aquí se agregaran conclusiones sobre los datos analizados.")
    # Aquí puedes agregar el código para mostrar las conclusiones de los datos
    # Por ejemplo, un resumen o análisis de los datos obtenidos


st.sidebar.title('Navegación')
pagina = st.sidebar.radio("", ("Página de Inicio", "Balance", "Demanda", "Generación", "Intercambio", "Conclusion de Datos"))



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
elif pagina == 'Conclusion de Datos':
    Conclusiones()
