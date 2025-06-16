import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Pago en Efectivo",
    page_icon="💵",
    layout="centered"
)

# Estilos globales actualizados
st.markdown("""<style>
/* Fondo de toda la app */
html, body, .stApp, #root, header, main, section {
    background-color: #D4DFF0 !important;
    font-family: 'Inter', sans-serif !important;
    color: #2B3674 !important;
    margin: 0 !important;
    padding: 0 !important;
    height: 100%;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #2C3E50 !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
    font-family: 'Poppins', sans-serif !important;
}

/* Contenedor principal */
.block-container {
    max-width: 700px !important;
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    margin: auto !important;
}

/* Títulos */
h1, h2, h3, h4 {
    color: #2B3674 !important;
}

/* Botones */
.stButton > button {
    background-color: #2B3674 !important;
    color: white !important;
    padding: 14px 30px !important;
    border-radius: 10px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    margin: 10px 0 !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
}
.stButton > button:hover {
    background-color: #1A2156 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(26, 33, 86, 0.35) !important;
}
</style>""", unsafe_allow_html=True)

# Título
st.title("💵 Pago en Efectivo")
st.markdown("### Selecciona una opción")
st.markdown("<br>", unsafe_allow_html=True)

# Botón: Tengo efectivo justo
if st.button("✅ Tengo efectivo justo", use_container_width=True):
    st.session_state["tipo_efectivo"] = "justo"
    st.switch_page("pages/Pedido exitoso.py")

# Botón: Necesito cambio
if st.button("💱 Necesito cambio", use_container_width=True):
    st.session_state["tipo_efectivo"] = "cambio"
    st.switch_page("pages/Pedido exitoso.py")

# Espacio
st.markdown("<br><br>", unsafe_allow_html=True)

# Botón volver
if st.button("← Volver", use_container_width=True):
    st.switch_page("pages/Forma de pago.py")
