import streamlit as st
import time
import pandas as pd
import base64

from fontTools.ttLib import xmlToTag

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

# 1. Configuración inicial del estado de la aplicación
if "messages" not in st.session_state:
    st.session_state.messages = []


# 2. Función para añadir mensajes con efecto de streaming
def stream_message(text, speaker: str = "left"):
    message_id = f"msg_{len(st.session_state.messages)}"

    if message_id not in st.session_state:
        st.session_state[message_id] = {
            "speaker": speaker,
            "text": text,
            "displayed": "",
            "completed": False
        }
        st.session_state.messages.append(message_id)

    message = st.session_state[message_id]

    # Mostrar progreso del texto
    if not message["completed"]:
        placeholder = st.empty()
        for char in message["text"]:
            message["displayed"] += char
            placeholder.text(f"`{message['displayed']}`")
            time.sleep(0.02)
        message["completed"] = True


# 3. Interfaz de chat
left_col, right_col = st.columns(2)

# Mostrar historial de mensajes
for msg_id in st.session_state.messages:
    msg_data = st.session_state[msg_id]

    if msg_data["speaker"] == "left":
        with left_col:
            st.text(f"{msg_data['displayed']}")
            st.container(height=75, border=False)

    else:
        with right_col:
            st.container(height=85, border=False)
            st.text(f"{msg_data['displayed']}")


# 4. Flujo de conversación
if not st.session_state.messages:
    with left_col:
        stream_message("Me gustaría que le echases un vistazo a los resultados de tu última diálisis y me localices los electrolitos.📄", speaker="left")
        st.container(height=75, border=False)

    with right_col:
        st.container(height=85, border=False)
        stream_message("Pero... ¿Qué son los electrolitos?🧐", speaker="right")

    with left_col:
        stream_message("Son sustancias que se encuentran en el cuerpo humano en forma predominante de sales minerales, tales como sodio, potasio o fósforo.🔋", speaker="left")

    with right_col:
        st.container(height=85, border=False)
        stream_message("¡Ah vale, lo entiendo! Buscaré los datos.🔎", speaker="right")

    with left_col:
        st.container(height=75, border=False)
        stream_message("¡Genial! Cuando los hayas encontrado, utiliza la herramienta de abajo para seleccionarlos y ver qué alimentos deberías limitar dependiendo de qué electrolitos tengas altos 📈", speaker="left")
        st.container(height=45, border=False)


st.markdown("""
<style>
    /* Estilos para la flecha minimalista */
    .scroll-arrow {
        display: block;
        width: 50px;
        height: 50px;
        margin: 20px auto; /* Centrado */
        font-size: 2em;
        line-height: 50px;
        text-align: center;
        color: #dc3545;
        text-decoration: none; /* Quita subrayado */
        cursor: pointer;
    }
    .scroll-arrow:hover {
        color: #c82333;
    }
</style>

<!-- Enlace con la flecha -->
<a href="#target-section" class="scroll-arrow">&#8595;</a>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        document.querySelector(".scroll-arrow").addEventListener("click", function(event) {
            event.preventDefault();
            document.querySelector("#target-section").scrollIntoView({ behavior: 'smooth' });
        });
    });
</script>
""", unsafe_allow_html=True)
def load_food_data():
    df = pd.read_csv("alimentos.csv")
    return df

df = load_food_data()
cols = st.columns((1,8,1))

if "selected_electrolytes" not in st.session_state:
    st.session_state.selected_electrolytes = []
with cols[1]:
    with st.empty():
        st.container(height=200, border=False)
    st.markdown('<div id="target-section"></div>', unsafe_allow_html=True)
    st.header("Selecciona los electrolitos y descubre qué alimentos pueden ser desaconsejables para ti")
    st.container(height=30, border=False)
    electrolytes = {
        'Sodio':'🧂 Sodio (Na+)',
        'Potasio':'🍌 Potasio (K+)',
        'Fosforo':'🐟 Fósforo (P+)',
    }
    selected = st.multiselect(
            "Selección de iones:",
            options=electrolytes.keys(),
            label_visibility="collapsed",
            key="ion_pills",
            format_func=lambda ion: electrolytes[ion],
            placeholder="Escoge aquí"
        )
    st.container(height=30, border=False)
    st.session_state.selected_electrolytes = selected

    col_limitar,_, col_mal = st.columns((2,1,2))
    category_columns = {
        "limitada": col_limitar,
        "desaconsejada": col_mal
    }

    order = {
        "aconsejada": 1,
        "limitada": 2,
        "desaconsejada": 3
    }
    @st.cache_data
    def img_to_base64(img_path):
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    if len(selected) == 0:
        for category, col in category_columns.items():
            if category != "aconsejada":
                col.subheader(category.upper(), anchor=category)
    else:
        if len(selected) == 1:
            ion = selected[0]
            df["final_category"] = df[ion]
        else:
            def worst_recommendation(row):
                recs = [row[ion] for ion in selected]
                return max(recs, key=lambda cat: order[cat])

            df["final_category"] = df.apply(worst_recommendation, axis=1)

        for category, col in category_columns.items():
            if category != "aconsejada":
                col.subheader(category.upper(), anchor=category)
                filtered = df[df["final_category"] == category]
                for idx, row in filtered.iterrows():
                    with col.container():
                        if row.get("Image"):
                            try:
                                #col.image(row["Image"], caption=row['Alimento'], use_container_width=True)
                                st.markdown(f"""
                                                <div style="position: relative; width: 100%; height: 200px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; margin-bottom: 10px;">
                                                    <img src={row["Image"]}" style="width: 100%; height: 100%; object-fit: cover;">
                                                    <div style="position: absolute; bottom: 0; width: 100%; background-color: rgba(0, 0, 0, 0.5); color: white; padding: 5px; text-align: center;">
                                                        <strong>{row['Alimento']}</strong>
                                                    </div>
                                                </div>
                                                """, unsafe_allow_html=True)
                            except Exception as e:
                                    col.write(f"Error cargando imagen: {e}")
                        else:
                            col.markdown(
                                    f"<div style='padding: 10px; background-color: #f0f0f0;'><strong>{row['Alimento']}</strong></div>",
                                    unsafe_allow_html=True
                            )

with st.empty():
    st.container(height=300, border=False)