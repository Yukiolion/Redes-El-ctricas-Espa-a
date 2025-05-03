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
    col1, col2 = st.columns([1, 4])  # Columna pequeña para la foto, grande para el texto

    with col1:
        img = Image.open("app/custom_pages/about_pages/img/andre.jpg")
        img = img.resize((200, 200))
        st.image(img)

    with col2:
        st.markdown("""
        ¡Hola! Soy **Andre** y junto a mis compañeros hemos desarrollado este proyecto enfocado en la predicción y análisis de redes eléctricas.  
        Si te ha parecido interesante o quieres saber más, no dudes en contactarme:
        """)
        st.markdown('<p class="section-title">Contacto</p>', unsafe_allow_html=True)
        st.markdown("📧 **Email:** [a.ravn1052@gmail.com](mailto:a.ravn1052@gmail.com)")
        st.markdown("💼 **LinkedIn:** [linkedin.com/in/andré-raven-villa-2b10b71a](https://www.linkedin.com/in/andré-raven-villa-2b10b71a)")

    st.markdown("---")

    with open("app/custom_pages/about_pages/CV/cv_andre.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="📄 Descargar CV",
            data=PDFbyte,
            file_name="cv_andre.pdf",
            mime="application/pdf"
        )
