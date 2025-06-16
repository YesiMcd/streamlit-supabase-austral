import streamlit as st
from PIL import Image
import base64

# Función para convertir imagen a base64
def image_to_base64(image):
    import io
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# --- Cargar imágenes ---
logo = Image.open("logo_carrito.png")
logo_b64 = image_to_base64(logo)

# Configuración de la página
st.set_page_config(
    page_title="Tu Super Online",
    layout="centered"
)

# Estilo personalizado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    .stApp {
        background-color: #D4DFF0 !important;
    }

    .main {
        background: #D4DFF0 !important;
        min-height: 100vh;
        padding: 2rem;
        font-family: 'Inter', sans-serif !important;
        text-align: center;
    }

    .title-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-bottom: 2rem;
        width: 100%;
    }

    .title-container h1 {
        font-size: 3rem;
        font-weight: 700;
        color: #2B3674;
        margin: 0 0 0.5rem 0;
        font-family: 'Inter', sans-serif;
    }

    .title-container .subtitle {
        font-size: 1.1rem;
        color: #707EAE;
        margin: 0 0 1rem 0;
    }

    .info-highlight {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2B3674;
        margin-top: 1.5rem;
    }

    .stButton > button {
        background-color: #2B3674 !important;
        color: white !important;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1.3rem;
        font-weight: 500;
        width: 100%;
        box-shadow: 0 6px 20px rgba(43, 54, 116, 0.25);
        border: none;
    }

    .stButton > button:hover {
        background-color: #1A2156 !important;
        box-shadow: 0 4px 12px rgba(43, 54, 116, 0.15);
        transform: translateY(-2px);
    }

    div[data-testid="column"] {
        display: flex !important;
        height: 400px !important;
    }

    div[data-testid="column"] > div {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: stretch !important;
    }

    .column-container {
        height: 320px !important;
        min-height: 320px !important;
        max-height: 320px !important;
        padding: 1.5rem;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        margin: 0.5rem;
        box-shadow: 0 10px 30px rgba(43, 54, 116, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.8);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .icon-container {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .logo-large {
        width: 80px;
        height: 80px;
        margin-bottom: 0.5rem;
        animation: floatSlow 4s ease-in-out infinite;
        filter: drop-shadow(0 4px 8px rgba(43, 54, 116, 0.2));
    }

    .profile-icon {
        font-size: 4rem;
        margin-bottom: 0.5rem;
        animation: float 3.5s ease-in-out infinite;
        animation-delay: 0.5s;
    }

    @keyframes floatSlow {
        0% { transform: translateY(0px) rotate(0deg); }
        33% { transform: translateY(-8px) rotate(2deg); }
        66% { transform: translateY(-4px) rotate(-1deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    </style>
""", unsafe_allow_html=True)

# Título y subtítulo
st.markdown("""
    <div class="title-container">
        <h1>¡Tu Super Online!</h1>
        <p class="subtitle">Bienvenido a tu supermercado digital</p>
    </div>
""", unsafe_allow_html=True)

# Crear dos columnas
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown(f"""
        <div class="column-container">
            <div class="icon-container">
                <img src="data:image/png;base64,{logo_b64}" class="logo-large" alt="Logo Carrito">
                <h3 style="color: #2B3674; margin: 0;">Carrito</h3>
                <p style="color: #707EAE; font-size: 1.5rem;">Comienza tu compra</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Crear Carrito", key="crear_carrito"):
        st.switch_page("pages/Buscador de productos.py")

with col2:
    st.markdown("""
        <div class="column-container">
            <div class="icon-container">
                <span class="profile-icon">👤</span>
                <h3 style="color: #2B3674; margin: 0;">Mi Perfil</h3>
                <p style="color: #707EAE; font-size: 1.5rem;">Gestiona tu cuenta</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("Acceder al Perfil", key="acceder_perfil"):
        st.switch_page("pages/Mi perfil.py")

# Pie de página
st.markdown('<p class="info-highlight">¡Disfruta de la mejor experiencia de compra online!</p>', unsafe_allow_html=True)
