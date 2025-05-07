import streamlit as st

def eduardo_info():
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
    ¡Hola! Soy **Eduardo** y junto a mis compañeros hemos desarrollado este proyecto enfocado en la predicción y análisis de redes eléctricas.  
    Si te ha parecido interesante o quieres saber más, no dudes en contactarme:
    """)
    st.markdown('<p class="section-title">Contacto</p>', unsafe_allow_html=True)
    st.markdown("📧 **Email:** [eduar.romero.villegas@gmail.com ](mailto:eduar.romero.villegas@gmail.com )")
    st.markdown("💼 **LinkedIn:**")
    st.markdown("🌐 **GitHub:**")


    st.markdown("---")

    with open("app/custom_pages/about_pages/CV/CV_Eduardo_Romero.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        st.download_button(
            label="📄 Descargar mi CV",
            data=PDFbyte,
            file_name="CV_Eduardo_Romero.pdf",
            mime="application/pdf"
        )