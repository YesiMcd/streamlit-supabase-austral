import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Forma de Pago",
    page_icon="💳",
    layout="centered"
)

# Estilo de fondo general + encabezados, etc.
st.markdown("""
    <style>
    html, body, .stApp, #root, header, main, section {
        background-color: #D4DFF0 !important;
        font-family: 'Inter', sans-serif !important;
        color: #2B3674 !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 100%;
    }

    .block-container {
        max-width: 700px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        margin: auto !important;
    }

    h1, h2, h3, h4 {
        color: #2B3674 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stButton > button {
        background-color: #2B3674 !important;
        color: white !important;
        padding: 14px 30px !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
        width: 100% !important;
        margin: 10px 0 !important;
    }
    .stButton > button:hover {
        background-color: #1A2156 !important;
        box-shadow: 0 6px 18px rgba(26, 33, 86, 0.35) !important;
        transform: translateY(-2px) !important;
    }

    div.stButton {
        text-align: center !important;
        padding: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar styling
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #2C3E50 !important;
    }
    [data-testid="stSidebar"] .sidebar-content {
        background-color: #2C3E50 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título de la página
st.title("💰 Forma de Pago")

# Mensaje informativo
st.markdown("### Selecciona tu método de pago preferido")
st.markdown("<br>", unsafe_allow_html=True)

# Botón de Efectivo
if st.button("💵 Efectivo", use_container_width=True):
    st.session_state["metodo_pago"] = "efectivo"
    st.switch_page("pages/Pago en efectivo.py")

# Espacio entre botones
st.markdown("<br>", unsafe_allow_html=True)

# Botón de Tarjeta
if st.button("💳 Tarjeta", use_container_width=True):
    st.session_state["metodo_pago"] = "tarjeta"
    st.switch_page("pages/Datos de la tarjeta.py")

# Espacio
st.markdown("<br><br>", unsafe_allow_html=True)

# Botón Volver
if st.button("← Volver", use_container_width=True):
    st.switch_page("pages/Buscador de productos.py")
