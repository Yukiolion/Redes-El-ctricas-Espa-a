import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
#from lib.scripts.master import actualizacion_general
from custom_pages.Balance import Balance
from custom_pages.Demanda import Demanda
from custom_pages.Generacion import Generacion
from custom_pages.Intercambio import Intercambio



def Exploratory():
    st.title("📊 Exploratory Data Analysis")

# if st.button("🔄 Actualizar base de datos"):
#     with st.spinner("Actualizando la base de datos..."):
#         actualizacion_general()
#     st.success("✅ Base de datos actualizada.")


    tabs = st.tabs(["Balance", "Demanda", "Generación", "Intercambio"])

    with tabs[0]:
        Balance()
    with tabs[1]:
        Demanda()
    with tabs[2]:
        Generacion()
    with tabs[3]:
        Intercambio()