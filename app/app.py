import streamlit as st
from streamlit_lottie import st_lottie
import time
st.markdown("""
    <style>
        /* Quitar márgenes y padding del contenedor principal */
        .appview-container .main, .block-container {
            padding: 10 !important;
            margin: 10 !important;
            max-width: 80% !important;
        }
    </style>
""", unsafe_allow_html=True)
cols = st.columns((1,8,1))
# Configurar estado de sesión
if "stream_done" not in st.session_state:
    st.session_state.stream_done = False

def load_lottie():
    return st_lottie(
        "https://lottie.host/66bdfdea-9ae1-4873-a970-8d4846d04256/QZjjsPQNDo.json",
        speed=10,
        width=800,
        height=350,
        key="initial",
        reverse=False
    )
with cols[1]:
    # Animación Lottie

    load_lottie()
    _PRESENTACION = """
    Soy tu asistente médico nutricional, y estoy aquí para ayudarte a cuidar tu alimentación y mejorar tu bienestar. Mi objetivo es guiarte para que identifiques y limites aquellos alimentos que pueden no ser beneficiosos para tu salud 💪. ¿Me ayudarías? 
    """

    def stream_data(text):
        # Mostrar texto solo si no se ha completado antes
        if not st.session_state.stream_done:
            placeholder = st.empty()
            full_text = ""
            for word in text.split(" "):
                full_text += word + " "
                placeholder.markdown(full_text)
                time.sleep(0.15)
            st.session_state.stream_done = True
        else:
            st.markdown(text)  # Mostrar texto completo directamente

    # Mostrar presentación
    stream_data(_PRESENTACION)
    st.container(height=80, border=False)

    # Botón solo aparece después del streaming
    if st.session_state.stream_done:
        if st.button("|\n\n 🔬 Empezar 🔬 \n\n|", use_container_width=True):
            st.switch_page("pages/page1.py")