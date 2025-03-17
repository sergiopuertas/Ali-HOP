import streamlit as st
import time
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


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


def generate_pdf(selected,df):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Configuración de columnas
    col1_x = 100  # Posición X de la primera columna (limitar)
    col2_x = 300  # Posición X de la segunda columna (eliminar)
    y_start = height - 100  # Posición inicial en Y
    y_offset = 20  # Espaciado entre líneas
    margin_bottom = 50  # Margen mínimo antes de cambiar de página

    # Título principal
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y_start, f"Lista de alimentos a limitar o no consumir: ")

    y = y_start - 40

    def draw(y):

        # Dibujar encabezados de las columnas
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.red)
        c.drawString(col1_x, y, "LIMITAR")
        c.drawString(col2_x, y, "ELIMINAR")

        y -= y_offset  # Espaciado debajo de los títulos
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        return y
    y = draw(y)
    # Filtrar los alimentos por categoría
    limitada = df[df["final_category"] == "limitada"]["Alimento"].tolist()
    desaconsejada = df[df["final_category"] == "desaconsejada"]["Alimento"].tolist()

    # Asegurar que ambas columnas tengan la misma cantidad de elementos
    max_len = max(len(limitada), len(desaconsejada))
    limitada += [""] * (max_len - len(limitada))  # Rellenar con espacios vacíos
    desaconsejada += [""] * (max_len - len(desaconsejada))

    # Dibujar alimentos en columnas
    for lim, elim in zip(limitada, desaconsejada):
        # Ajustar para evitar que se salga de la página
        if y < margin_bottom:
            c.showPage()
            y = y_start - 40
            y = draw(y)

        # Dibujar alimentos
        c.drawString(col1_x, y, lim)
        c.drawString(col2_x, y, elim)
        y -= y_offset  # Mover hacia abajo

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
    st.markdown('<div id="target-section"></div>', unsafe_allow_html=True)
    st.header("Selecciona los electrolitos y descubre qué alimentos pueden ser desaconsejables para ti")
    st.container(height=30, border=False)
    electrolytes = {
        'Sodio':'🧂 Sodio (Na+)',
        'Potasio':'🍌 Potasio (K+)',
        'Fosforo':'🐟 Fósforo (P+)',
    }
    col = st.columns((5,1))
    with col[0]:
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

    if len(selected) == 0:
        for category, col in category_columns.items():
            if category != "aconsejada":
                col.subheader("LIMITAR" if category == "limitada" else "ELIMINAR", anchor=category)
    else:
        if len(selected) == 1:
            ion = selected[0]
            df["final_category"] = df[ion]
        else:
            def worst_recommendation(row):
                recs = [row[ion] for ion in selected]
                return max(recs, key=lambda cat: order[cat])

            df["final_category"] = df.apply(worst_recommendation, axis=1)

        with col[1]:
            pdf_buffer = generate_pdf(selected,df)
            st.download_button(
                        label="Descargar",
                        data=pdf_buffer,
                        file_name=f"alimentos_{','.join(selected)}.pdf",
                        mime="application/pdf",
                        key="download_button",
                        use_container_width=True
                    )
        for category, col in category_columns.items():
            if category != "aconsejada":
                col.subheader("LIMITAR" if category == "limitada" else "ELIMINAR", anchor=category)
                filtered = df[df["final_category"] == category]
                for idx, row in filtered.iterrows():
                    with col.container():
                        if row.get("Image"):
                            try:
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