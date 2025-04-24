import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests

from pages.Balance import Balance
from pages.Demanda import Demanda
from pages.Generacion import Generacion
from pages.Intercambio import Intercambio

def Exploratory():
    st.title("📊 Exploratory Data Analysis")
    tabs = st.tabs(["Balance", "Demanda", "Generación", "Intercambio"])

    with tabs[0]:
        Balance()
    with tabs[1]:
        Demanda()
    with tabs[2]:
        Generacion()
    with tabs[3]:
        Intercambio()