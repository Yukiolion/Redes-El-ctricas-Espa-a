import streamlit as st

from custom_pages.about_pages.andre import andre_info
from custom_pages.about_pages.eduardo import eduardo_info
from custom_pages.about_pages.luisa import lui_info
from custom_pages.about_pages.samuel import samuel_info

def About():
    
    st.title('About Us:')
    st.subheader('Conocenos un poco más!!')


    tabs = st.tabs(["Andre", "Eduardo", "Luisa", "Samuel"])

    with tabs[0]:
        andre_info()
    with tabs[1]:
        eduardo_info()
    with tabs[2]:
        lui_info()
    with tabs[3]:
        samuel_info()