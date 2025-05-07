from PIL import Image
import streamlit as st

def andre_info():
    st.markdown("""
        <style>
        .section-title {
            font-size: 32px;
            font-weight: bold;
            margin-top: 2em;
            color: #b01923;
        }
    """, unsafe_allow_html=True)
    # Presentacion
    st.markdown("""
    ¡Hola! Soy **Andre** y junto a mis compañeros hemos desarrollado este proyecto enfocado en la predicción y análisis de redes eléctricas.  
    Si te ha parecido interesante o quieres saber más, no dudes en contactarme:
    """)
    st.markdown('<p class="section-title">Contacto</p>', unsafe_allow_html=True)
    st.markdown("📧 **Email:** [a.ravn1052@gmail.com](mailto:a.ravn1052@gmail.com)")
    st.markdown("💼 **LinkedIn:** [linkedin.com/in/andré-raven-villa](https://www.linkedin.com/in/andré-raven-villa)")
    st.markdown("🌐 **GitHub:** [github.com/Yukiolion](https://github.com/Yukiolion)")

    st.markdown("---")

    with open("app/custom_pages/about_pages/CV/cv_andre.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="📄 Descargar CV",
            data=PDFbyte,
            file_name="cv_andre.pdf",
            mime="application/pdf"
        )
