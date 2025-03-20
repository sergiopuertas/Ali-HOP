import streamlit as st
import time
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

st.markdown("""
    <style>
        .appview-container .main, .block-container {
            padding: 10 !important;
            margin: 10 !important;
            max-width: 80% !important;
        }
    </style>
""", unsafe_allow_html=True)

conn = st.connection("neon", type="sql")


def generate_pdf(df):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    col1_x = 80
    col2_x = 270
    col3_x = 460

    y_start = height - 100
    y_offset = 20
    margin_bottom = 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y_start, "Lista de alimentos a limitar o no consumir:")

    y = y_start - 40

    def draw(y):
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.red)
        c.drawString(col1_x, y, "RECOMENDADO")
        c.drawString(col2_x, y, "LIMITAR")
        c.drawString(col3_x, y, "ELIMINAR")
        y -= y_offset
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        return y

    y = draw(y)

    categories = {
        "aconsejada": df[df["final_category"] == "aconsejada"]["alimento"].tolist(),
        "limitada": df[df["final_category"] == "limitada"]["alimento"].tolist(),
        "desaconsejada": df[df["final_category"] == "desaconsejada"]["alimento"].tolist()
    }

    max_len = max(len(c) for c in categories.values())
    for cat in categories:
        categories[cat] += [""] * (max_len - len(categories[cat]))

    for items in zip(categories["aconsejada"], categories["limitada"], categories["desaconsejada"]):
        if y < margin_bottom:
            c.showPage()
            y = y_start - 40
            y = draw(y)

        c.drawString(col1_x, y, items[0])
        c.drawString(col2_x, y, items[1])
        c.drawString(col3_x, y, items[2])
        y -= y_offset

    c.save()
    buffer.seek(0)
    return buffer

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
        stream_message("Me gustaría que le echases un vistazo a los resultados de tu último análisis y me localices los electrolitos.📄", speaker="left")
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

@st.cache_data(ttl=600)
def get_food_data(electrolitos):
    if not electrolitos:
        return pd.DataFrame()
    try:
        query = f"""
            SELECT alimento, image, {', '.join(electrolitos)}
            FROM alimentos
            WHERE {' OR '.join([f"{e} IS NOT NULL" for e in electrolitos])}
        """
        return conn.query(query, ttl = 600)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

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




# Estado de la aplicación
if "messages" not in st.session_state:
    st.session_state.messages = []


cols = st.columns((1, 8, 1))

with cols[1]:
    st.markdown('<div id="target-section"></div>', unsafe_allow_html=True)
    st.header("Selecciona los electrolitos y descubre qué alimentos pueden ser desaconsejables para ti")

    electrolytes = {
        'sodio': '🧂 Sodio (Na+)',
        'potasio': '🍌 Potasio (K+)',
        'fosforo': '🐟 Fósforo (P+)',
    }

    col1, col2 = st.columns((4, 1))
    with col1:
        selected = st.multiselect(
            "Selección de iones:",
            options=electrolytes.keys(),
            format_func=lambda x: electrolytes[x],
            placeholder="Escoge aquí",
            key="ion_select",
            label_visibility="collapsed"
        )
    df = get_food_data(selected)
    if not df.empty:
        order = {"aconsejada": 1, "limitada": 2, "desaconsejada": 3}
        if len(selected) == 1:
            df["final_category"] = df[selected[0]]
        else:
            def get_category(row):
                return max(
                    (row[e] for e in selected),
                    key=lambda x: order.get(x, 0)
                )
            df["final_category"] = df.apply(get_category, axis=1)
        with col2:
            pdf_buffer = generate_pdf(df)
            st.download_button(
                "Descargar",
                data=pdf_buffer,
                file_name="recomendaciones_alimenticias.pdf",
                mime="application/pdf"
            )

    # Consulta a la base de datos con cada cambio

    col_bien,_, col_limitar,_, col_mal = st.columns((2,1, 2,1, 2))

    category_columns = {
        "aconsejada": col_bien,
        "limitada": col_limitar,
        "desaconsejada": col_mal
    }

    if df.empty:
        pass
    else:
        # Mostrar resultados
        for category, col in category_columns.items():
            col.subheader("RECOMENDADO" if category == "aconsejada" else
                          "LIMITAR" if category == "limitada" else "ELIMINAR")

            alimentos = df[df["final_category"] == category]
            for _, row in alimentos.iterrows():
                with col:
                    try:
                        st.markdown(f""" <div style="position: relative; width: 100%; height: 200px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; margin-bottom: 10px;">
                                                                        <img src={row["image"]}" style="width: 100%; height: 100%; object-fit: cover;">
                                                                        <div style="position: absolute; bottom: 0; width: 100%; background-color: rgba(0, 0, 0, 0.5); color: white; padding: 5px; text-align: center;">
                                                                            <strong>{row['alimento']}</strong>
                                                                        </div>
                                                                    </div>
                    """, unsafe_allow_html=True)
                    except Exception as e:
                        col.write(f"Error cargando imagen: {e}")

with st.empty():
    st.container(height=300, border=False)