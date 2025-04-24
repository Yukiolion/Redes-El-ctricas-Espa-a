import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests

from libs.Balance import Balance
from libs.Demanda import Demanda
from libs.Generacion import Generacion
from libs.Intercambio import Intercambio

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