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
        st.write("- **Balance**: Contiene información sobre el balance energético que es la diferencia entre la energía generada y la consumida.")
        st.write("- **Demanda**: Contiene información sobre la demanda eléctrica que es la cantidad de energía están consumiendo los usuarios en un momento dado o durante un periodo.")
        st.write("- **Generación**: Contiene información sobre la generación eléctrica que indica cuánta energía se está produciendo y con qué fuentes (renovables, no renovables, nuclear, etc.).")
        st.write("- **Intercambio**: Contiene información sobre los intercambios internacionales de energía, es decir, la energía que España importa o exporta a países vecinos a través de las interconexiones..")
        # Con esto redimensionamos la imagen para que no salga gigante
        img = Image.open("app/images/diagrama sql.png")
        img = img.resize((650, 650))
        st.image(img, caption='Diagrama de la base de datos')