import streamlit as st

st.set_page_config(page_title="Mi Perfil", page_icon="👤", layout="centered")

# Estilos personalizados
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Fondo general */
    body, .main {
        background: linear-gradient(135deg, #E8F0FE, #F8FAFF) !important;
        font-family: 'Inter', sans-serif !important;
        color: #2B3674 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Contenedor principal sin fondo blanco */
    .block-container {
        background-color: transparent !important;
        padding: 2rem 1rem !important;
        margin: 0 auto !important;
        max-width: 700px !important;
        box-shadow: none !important;
    }

    /* Título */
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        color: #2B3674 !important;
        margin-bottom: 1rem !important;
    }

    /* Inputs */
    input[type="text"], input[type="email"] {
        border-radius: 10px !important;
        border: 1.5px solid #2B3674 !important;
        padding: 0.6rem 1rem !important;
        font-size: 1rem !important;
        color: #2B3674 !important;
        font-family: 'Inter', sans-serif !important;
        background-color: white !important;
        width: 100% !important;
        box-sizing: border-box !important;
        transition: border-color 0.3s ease !important;
    }
    input[type="text"]:focus, input[type="email"]:focus {
        border-color: #1A2156 !important;
        outline: none !important;
    }

    /* Botones */
    .stButton > button {
        background-color: #2B3674 !important;
        color: white !important;
        padding: 0.8rem 2rem !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        margin-top: 1.5rem !important;
        width: 100% !important;
        cursor: pointer;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(43, 54, 116, 0.15);
    }
    .stButton > button:hover {
        background-color: #1A2156 !important;
        box-shadow: 0 6px 18px rgba(26, 33, 86, 0.35) !important;
        transform: translateY(-2px);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2C3E50 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    [data-testid="stSidebar"] .sidebar-content .sidebar-nav a {
        font-size: 20px !important;
        font-weight: 600 !important;
        padding: 20px 20px !important;
        margin: 8px 0 !important;
        border-radius: 20px !important;
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
    """,
    unsafe_allow_html=True,
)

# Contenido
st.markdown("## Mi Perfil 👤")

nombre = st.text_input("Nombre", value="")
email = st.text_input("Email", value="")
telefono = st.text_input("Número de teléfono", value="")
codigo_postal = st.text_input("Código postal", value="")
direccion = st.text_input("Dirección", value="")

col1, col2 = st.columns(2)

with col1:
    if st.button("Historial de compras"):
        st.info("Aquí se mostraría el historial de compras del usuario.")

with col2:
    if st.button("Guardar cambios"):
        st.success("Cambios guardados correctamente.")
        st.write(f"Nombre: {nombre}")
        st.write(f"Email: {email}")
        st.write(f"Teléfono: {telefono}")
        st.write(f"Código postal: {codigo_postal}")
        st.write(f"Dirección: {direccion}")
