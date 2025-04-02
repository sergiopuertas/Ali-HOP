import streamlit as st
import time
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from typing import Dict, List
import threading


conn = st.connection("neon", type="sql")

electrolytes = {
    'sodio': '🧂 Sodio (Na+)',
    'potasio': '🍌 Potasio (K+)',
    'fosforo': '🐟 Fósforo (P+)',
}

@st.cache_data(ttl=600)
def get_all_food_data():
    """Carga todos los datos de alimentos con electrolitos de una vez"""
    try:
        query = """
            SELECT alimento, image, sodio, potasio, fosforo 
            FROM alimentos
            WHERE sodio IS NOT NULL 
               OR potasio IS NOT NULL 
               OR fosforo IS NOT NULL
        """
        return conn.query(query, ttl=600)
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()



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


def process_selected_data(selected_ions: List[str], all_data: pd.DataFrame) -> pd.DataFrame:
    """Filtra y categoriza los alimentos basado en los iones seleccionados"""
    if not selected_ions:
        return pd.DataFrame()

    # 1. Filtrar filas con datos para los iones seleccionados
    mask = all_data[selected_ions].notnull().any(axis=1)
    df = all_data.loc[mask, ['alimento', 'image'] + selected_ions].copy()

    # 2. Determinar la categoría final
    order = {"aconsejada": 1, "limitada": 2, "desaconsejada": 3}

    if len(selected_ions) == 1:
        df["final_category"] = df[selected_ions[0]]
    else:
        def get_category(row):
            return max(
                (row[e] for e in selected_ions),
                key=lambda x: order.get(x, 0)
            )

        df["final_category"] = df.apply(get_category, axis=1)

    return df

def show_photos(row):
    try:
        st.markdown(f""" <div style="position: relative; width: 100%; height: 200px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; margin-bottom: 10px;">
                         <img src={row["image"]}" style="width: 100%; height: 100%; object-fit: cover;">
                          <div style="position: absolute; bottom: 0; width: 100%; background-color: rgba(0, 0, 0, 0.5); color: white; padding: 5px; text-align: center;">
                            <strong>{row['alimento']}</strong>
                           </div>
                          </div> """, unsafe_allow_html=True)
    except Exception as e:
        st.write(f"Error cargando imagen: {e}")


