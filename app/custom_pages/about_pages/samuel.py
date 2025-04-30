import streamlit as st

def samuel_info():
    st.title('Samuel')

    st.markdown("""
        <style>
        .title {
            font-size: 50px;
            font-weight: bold;
            color: #b01923;
        }
        .subtitle {
            font-size: 24px;
            color: #fafafa;
        }
        .section-title {
            font-size: 32px;
            font-weight: bold;
            margin-top: 2em;
            color: #b01923;
        }
        .project {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 1em;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            background-color: #fafafa;
        }
        </style>
    """, unsafe_allow_html=True)
    # Presentacion
    st.markdown('<p class="title">Hola, soy Samuel 👋</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Desarrollador de software Full-Stack | Ciencia de Datos | IA</p>', unsafe_allow_html=True)

    # Contacto
    st.markdown('<p class="section-title">Contacto</p>', unsafe_allow_html=True)
    st.write("📧 Email: samueljsanchez24@email.com")
    st.write("💼 LinkedIn: www.linkedin.com/in/samuel-sanchez-robles-ba2a5425a")