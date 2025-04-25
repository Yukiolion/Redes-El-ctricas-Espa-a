import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests

from app.custom_pages.exploratory_pages.Balance import Balance
from app.custom_pages.exploratory_pages.Demanda import Demanda
from app.custom_pages.exploratory_pages.Generacion import Generacion
from app.custom_pages.exploratory_pages.Intercambio import Intercambio

from custom_pages.Database import Database
from custom_pages.Exploratory import Exploratory
from custom_pages.DL import DL
from custom_pages.About import About


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
            "- Turbinación bombeo\n")
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
            "- Generación no renovable")
    elif opcion == 'Otras categorias':
        st.info(
            "⚖️ **Otras categorías**\n\n"
            "Estas no son fuentes de generación directa, pero están presentes en el sistema. Incluyen:\n\n"
            "- Consumo bombeo (se usa para almacenar energía, no genera)\n"
            "- Saldo I. internacionales (intercambios con otros países)\n"
            "- Saldo almacenamiento (puede incluir carga y entrega de baterías)\n"
            "- Carga batería (almacenamiento, no producción directa)")


st.sidebar.title('Navegación')
pagina = st.sidebar.radio("Selecciona una página:", 
                        ["Página principal", "Exploratory Data Analysis", "DL y Propeth", "Base de Datos", "About Us"])

# Página principal con tabs
if pagina == 'Página principal':
    main()
# Otras páginas
elif pagina == 'Exploratory Data Analysis':
    Exploratory()
elif pagina == 'DL y Propeth':
    DL()
elif pagina == 'Base de Datos':
    Database()
elif pagina == 'About Us':
    About()
