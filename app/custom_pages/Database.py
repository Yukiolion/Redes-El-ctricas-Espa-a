import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests
from PIL import Image

def Database():
        st.title("Estructura base de datos")
        st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
        st.write("En esta sección se muestra la estructura de la base de datos utilizada en el proyecto. La base de datos" \
        " está dividida en cuatro tablas principales:")
        st.write("- **Balance**: Contiene información sobre el balance energético.")
        st.write("- **Demanda**: Contiene información sobre la demanda eléctrica.")
        st.write("- **Generación**: Contiene información sobre la generación eléctrica.")
        st.write("- **Intercambio**: Contiene información sobre los intercambios internacionales de energía.")

        img = Image.open("app/images/diagrama sql.png")
        img = img.resize((950, 950))
        st.image(img, caption='Diagrama de la base de datos')