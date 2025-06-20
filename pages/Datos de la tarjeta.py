import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Datos de la Tarjeta",
    page_icon="💳",
    layout="centered"
)

# Estilo personalizado reforzado
st.markdown("""
    <style>
    html, body, .stApp, #root, header, main, section {
        background-color: #D4DFF0 !important;
        font-family: 'Inter', sans-serif !important;
        color: #2B3674 !important;
        margin: 0;
        padding: 0;
        height: 100%;
    }
    .block-container {
        background-color: #D4DFF0 !important;
        max-width: 700px !important;
        padding-top: 2rem;
        padding-bottom: 2rem;
        margin: auto;
    }
    input[type="text"], input[type="password"] {
        border-radius: 10px !important;
        border: 1.5px solid #2B3674 !important;
        padding: 10px 14px !important;
        font-size: 16px !important;
        background-color: white !important;
    }
    .stTextInput > div > div > input {
        width: 100% !important;
    }
    .stButton > button {
        background-color: #2B3674 !important;
        color: white !important;
        padding: 14px 30px !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #1A2156 !important;
        transform: translateY(-1px);
    }
    [data-testid="stSidebar"] {
        background-color: #2C3E50 !important;
    }
    [data-testid="stSidebar"] .sidebar-content {
        background-color: #2C3E50 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
        font-family: 'Poppins', sans-serif !important;
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
    h1, h2, h3, h4 {
        color: #2B3674 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.title("💳 Datos de la Tarjeta")

# Formulario
with st.form("formulario_tarjeta"):
    numero_tarjeta = st.text_input("Número de la Tarjeta", max_chars=16)
    col1, col2 = st.columns(2)

    with col1:
        fecha_vencimiento = st.text_input("Fecha de Vencimiento", placeholder="MM/AA", max_chars=5)

    with col2:
        codigo_seguridad = st.text_input("Código de Seguridad", type="password", max_chars=4)

    nombre_tarjeta = st.text_input("Nombre en la Tarjeta")

    st.markdown("### Tipo de Tarjeta")
    tipo_tarjeta = st.radio("Seleccione el tipo de tarjeta", options=["Débito", "Crédito"], horizontal=True, label_visibility="collapsed")

    submitted = st.form_submit_button("PAGAR")

    if submitted:
        if not numero_tarjeta or not fecha_vencimiento or not codigo_seguridad or not nombre_tarjeta:
            st.error("Por favor, complete todos los campos")
        else:
            st.success("¡Pago procesado con éxito!")
            st.session_state["pago_completado"] = True
            st.switch_page("pages/Pedido exitoso.py")

# Botón volver
if st.button("← Volver"):
    st.switch_page("pages/Forma de Pago.py")
