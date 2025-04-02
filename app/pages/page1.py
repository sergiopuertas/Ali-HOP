from pages.lib import *

st.markdown("""
    <style>
        .appview-container .main, .block-container {
            padding: 10 !important;
            margin: 10 !important;
            max-width: 80% !important;
        }
    </style>
""", unsafe_allow_html=True)
all_food_data = get_all_food_data()
if "messages" not in st.session_state:
    st.session_state.messages = []

_,left_col, right_col = st.columns((1,7,7))

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

st.container(height=40, border=False)
st.markdown( """
<style>
    /* Estilos para la flecha minimalista */
    .scroll-arrow {
        display: block;
        width: 80px;
        height: 80px;
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
st.container(height=110, border=False)
cols = st.columns((2, 15, 1))


with cols[1]:
    st.header("Selecciona los electrolitos y descubre qué alimentos pueden ser desaconsejables para ti")
cols = st.columns((2, 20, 2))
with cols[1]:
    st.markdown('<div id="target-section"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns((5, 1))
    with col1:
        selected = st.multiselect(
            "Selección de iones:",
            options=electrolytes.keys(),
            format_func=lambda x: electrolytes[x],
            placeholder="Escoge aquí",
            key="ion_select",
            label_visibility="collapsed"
        )
    df = process_selected_data(selected, all_food_data)
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

    col_bien,_, col_limitar,_, col_mal = st.columns((3,1,3,1,3))

    category_columns = {
        "aconsejada": col_bien,
        "limitada": col_limitar,
        "desaconsejada": col_mal
    }

    if df.empty:
        pass
    else:
        for category, col in category_columns.items():
            with col:
                st.markdown(
                    f"<h3 style='text-align: center; color: {'#28a745' if category == 'aconsejada' else '#ffc107' if category == 'limitada' else '#dc3545'};'>"
                    f"{'RECOMENDADO' if category == 'aconsejada' else 'LIMITAR' if category == 'limitada' else 'ELIMINAR'}"
                    f"</h3>",
                    unsafe_allow_html=True
                )
                alimentos = df[df["final_category"] == category]
                for _, row in alimentos.iterrows():
                    show_photos(row)

with st.empty():
    st.container(height=400, border=False)


