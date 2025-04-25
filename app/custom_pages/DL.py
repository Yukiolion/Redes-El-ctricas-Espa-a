import streamlit as st

from custom_pages.dl_pages.gru import gru
from custom_pages.dl_pages.prophet import prophet
from custom_pages.dl_pages.rnn import rnn

def DL():
    tabs = st.tabs(["GRU", "Prophet", "RNN"])

    with tabs[0]:
        gru()
    with tabs[1]:
        prophet()
    with tabs[2]:
        rnn()