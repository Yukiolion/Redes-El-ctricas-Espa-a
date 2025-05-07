import streamlit as st
from PIL import Image

def lui_info():
    st.markdown("""
        <style>
        .section-title {
            font-size: 32px;
            font-weight: bold;
            margin-top: 2em;
            color: #b01923;
        }
    """, unsafe_allow_html=True)

    st.markdown("""
    ¡Hola! Soy **Luisa** y junto a mis compañeros hemos desarrollado este proyecto enfocado en la predicción y análisis de redes eléctricas.  
    Si te ha parecido interesante o quieres saber más, no dudes en contactarme:
    """)
    st.markdown('<p class="section-title">Contacto</p>', unsafe_allow_html=True)
    st.markdown("📧 **Email:** [luisagarciatorres@gmail.com](mailto:luisagarciatorres@gmail.com)")
    st.markdown("💼 **LinkedIn:** [linkedin.com/in/luisa-garcia-torres](https://www.linkedin.com/in/luisa-garcia-torres/)")
    st.markdown("🌐 **GitHub:**")

    st.markdown("---")

    with open("app/custom_pages/about_pages/CV/CV_Luisa_Garcia.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="📄 Descargar mi CV",
            data=PDFbyte,
            file_name="CV_Luisa_Garcia.pdf",
            mime="application/pdf"
        )