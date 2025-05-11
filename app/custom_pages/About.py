import streamlit as st
from PIL import Image

from custom_pages.about_pages.andre import andre_info
from custom_pages.about_pages.eduardo import eduardo_info
from custom_pages.about_pages.luisa import lui_info
from custom_pages.about_pages.samuel import samuel_info

def About():
    
    st.title('About Us:')
    st.subheader('Conocenos un poco más!!')

    # Se crean las columnas para cada miembro del equipo
    andre, eduardo, luisa, samuel = st.columns(4, vertical_alignment="center")

    with andre:
        img = Image.open("app/custom_pages/about_pages/img/andre.jpg")
        img = img.resize((200, 200))
        st.image(img)
        andre_info()

    with eduardo:
        img = Image.open("app/custom_pages/about_pages/img/usuario.png")
        img = img.resize((200, 200))
        st.image(img)
        eduardo_info()

    with luisa:
        img = Image.open("app/custom_pages/about_pages/img/luisa.jpg")
        img = img.resize((200, 200))
        st.image(img)
        lui_info()

    with samuel:
        img = Image.open("app/custom_pages/about_pages/img/samuel.png")
        img = img.resize((200, 200))
        st.image(img)
        samuel_info()