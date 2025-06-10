import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Pago en Efectivo",
    page_icon="💵",
    layout="centered"
)

# Sidebar styling
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #2C3E50;
    }
    [data-testid="stSidebar"] .sidebar-content {
        background-color: #2C3E50;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    [data-testid="stSidebar"] .sidebar-content .sidebar-nav a {
        font-size: 18px !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        margin: 8px 0 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        display: block !important;
        text-decoration: none !important;
    }
    [data-testid="stSidebar"] .sidebar-content .sidebar-nav a:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        transform: translateX(5px) !important;
    }
    [data-testid="stSidebar"] .sidebar-content .sidebar-nav a.active {
        background-color: rgba(255, 255, 255, 0.2) !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)



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