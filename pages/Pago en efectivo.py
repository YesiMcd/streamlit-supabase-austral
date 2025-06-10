import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Pago en Efectivo",
    page_icon="💵",
    layout="centered"
)

# Estilo personalizado
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 25px 30px;
        border-radius: 15px;
        border: none;
        font-size: 20px;
        transition: all 0.3s ease;
        margin: 15px 0;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transform: translateY(-3px);
    }
    .volver-button > button {
        background-color: #6c757d;
        font-size: 16px;
        padding: 15px 25px;
        margin-top: 30px;
    }
    .volver-button > button:hover {
        background-color: #5a6268;
    }
    div.stButton {
        text-align: center;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Título de la página
st.title("💵 Pago en Efectivo")

# Mensaje informativo
st.markdown("### Selecciona una opción")

# Espacio para separar
st.markdown("<br>", unsafe_allow_html=True)

# Contenedor para los botones principales
container = st.container()

with container:
    # Botón de efectivo justo
    if st.button("✅ Tengo efectivo justo", use_container_width=True):
        st.session_state["tipo_efectivo"] = "justo"
        st.success("¡Perfecto! Continúa con el pago exacto")

    # Espacio entre botones
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botón de necesito cambio
    if st.button("💱 Necesito cambio", use_container_width=True):
        st.session_state["tipo_efectivo"] = "cambio"
        st.success("De acuerdo, prepararemos tu cambio")

# Espacio para separar
st.markdown("<br>" * 2, unsafe_allow_html=True)

# Botón para volver atrás
if st.button("← Volver", use_container_width=True):
    st.session_state["page"] = "anterior"