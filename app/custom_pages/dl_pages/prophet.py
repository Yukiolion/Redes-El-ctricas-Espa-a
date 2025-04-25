import streamlit as st

def prophet():
    st.title("Prophet")
    st.write(
        """
        Prophet is an open-source forecasting tool developed by Facebook. It is designed to handle time series data that may have missing values and seasonal effects. Prophet is particularly useful for business applications, such as sales forecasting, where the data may have strong seasonal patterns.
        """
    )
    st.write(
        """
        Key features of Prophet include:
        - Automatic detection of seasonal effects
        - Robustness to missing data
        - Ability to handle outliers
        - User-friendly interface for non-technical users
        """
    )