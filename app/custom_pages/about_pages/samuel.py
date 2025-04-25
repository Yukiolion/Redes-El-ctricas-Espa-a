import streamlit as st

def samuel_info():
    st.title('Samuel')

    # Estilo personalizado
    st.markdown("""
        <style>
        .title {
            font-size: 50px;
            font-weight: bold;
            color: #b01923;
        }
        .subtitle {
            font-size: 24px;
            color: #333;
        }
        .section-title {
            font-size: 32px;
            font-weight: bold;
            margin-top: 2em;
            color: #b01923;
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 1em;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            background-color: #fafafa;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="title">Hola, soy Samuel 👋</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Desarrollador de software Full-Stack | Ciencia de Datos | IA</p>', unsafe_allow_html=True)

    # st.markdown('<p class="section-title">Sobre mí</p>', unsafe_allow_html=True)
    # st.write("""
    # Soy un apasionado por la tecnología con experiencia en desarrollo web, análisis de datos y modelos de aprendizaje automático.
    # Siempre estoy aprendiendo nuevas herramientas para resolver problemas reales.
    # """)

    # st.markdown('<p class="section-title">Proyectos</p>', unsafe_allow_html=True)

    # cols = st.columns(3)

    # with cols[0]:
    #     st.markdown('<div class="card">', unsafe_allow_html=True)
    #     st.subheader("📊 Proyecto 1")
    #     st.write("Descripción breve del proyecto.")
    #     st.link_button("Ver más", "https://github.com/tuusuario/proyecto1")
    #     st.markdown('</div>', unsafe_allow_html=True)

    # with cols[1]:
    #     st.markdown('<div class="card">', unsafe_allow_html=True)
    #     st.subheader("🤖 Proyecto 2")
    #     st.write("Otro proyecto que te representa.")
    #     st.link_button("Ver más", "https://github.com/tuusuario/proyecto2")
    #     st.markdown('</div>', unsafe_allow_html=True)

    # with cols[2]:
    #     st.markdown('<div class="card">', unsafe_allow_html=True)
    #     st.subheader("📱 Proyecto 3")
    #     st.write("Aplicación móvil o frontend.")
    #     st.link_button("Ver más", "https://github.com/tuusuario/proyecto3")
    #     st.markdown('</div>', unsafe_allow_html=True)

    # Contacto
    st.markdown('<p class="section-title">Contacto</p>', unsafe_allow_html=True)
    st.write("📧 Email: samueljsanchez24@email.com")
    st.write("💼 LinkedIn: www.linkedin.com/in/samuel-sanchez-robles-ba2a5425a")