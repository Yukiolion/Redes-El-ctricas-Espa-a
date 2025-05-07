from PIL import Image
import streamlit as st

def samuel_info():
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
    ¡Hola! Soy **Samuel** y junto a mis compañeros hemos desarrollado este proyecto enfocado en la predicción y análisis de redes eléctricas.  
    Si te ha parecido interesante o quieres saber más, no dudes en contactarme:
    """)
    st.markdown('<p class="section-title">Contacto</p>', unsafe_allow_html=True)
    st.markdown("📧 **Email:** [samueljsanchez24@email.com](mailto:samueljsanchez24@email.com)")
    st.markdown("💼 **LinkedIn:** [linkedin.com/in/samuel-j-sanchez](https://www.linkedin.com/in/samuel-j-sanchez)")
    st.markdown("🌐 **GitHub:** [github.com/Samu-Sr00](https://github.com/Samu-Sr00)")

    st.markdown("---")

    with open("app/custom_pages/about_pages/CV/CV_Samuel_Sanchez.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="📄 Descargar CV",
            data=PDFbyte,
            file_name="CV_Samuel_Sanchez.pdf",
            mime="application/pdf"
        )