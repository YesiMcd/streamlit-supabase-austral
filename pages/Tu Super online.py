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

# Cargar imágenes
logo = Image.open("logo_carrito.png")
logo_b64 = image_to_base64(logo)

# Cargar imagen de fondo que subiste
fondo = Image.open("fondo del titulo.jpg")
fondo_b64 = image_to_base64(fondo)

# Configuración de página
st.set_page_config(
    page_title="Tu Super Online",
    layout="centered"
)

# Estilos CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    .stApp {{
        background-color: #D4DFF0 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0 !important;
    }}

    header, footer, [data-testid="stToolbar"] {{
        display: none !important;
    }}

    /* Resetear márgenes del contenedor principal */
    .main > div {{
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }}

    .block-container {{
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: none !important;
    }}

    /* Fondo superior completo con imagen que ocupa todo el ancho */
    .hero {{
        width: 100vw;
        height: 350px;
        background-image: url("data:image/png;base64,{fondo_b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        margin: 0;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        position: relative;
    }}

    .hero::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(212, 223, 240, 0.1);
        backdrop-filter: blur(1px);
    }}

    .hero-content {{
        position: relative;
        z-index: 2;
        text-align: center;
    }}

    .hero h1 {{
        font-size: 3.5rem;
        font-weight: 700;
        color: #2B3674;
        margin-bottom: 1rem;
        text-shadow: 0px 2px 4px rgba(255, 255, 255, 0.6);
        line-height: 1.2;
    }}

    .hero p {{
        font-size: 1.5rem;
        color: #2B3674;
        margin: 0;
        text-shadow: 0px 1px 2px rgba(255, 255, 255, 0.5);
        font-weight: 500;
    }}

    /* Contenedor principal centrado después del hero */
    .main-content {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }}

    .info-highlight {{
        font-size: 1.3rem;
        font-weight: 600;
        color: #2B3674;
        margin-top: 2rem;
        text-align: center;
    }}

    .stButton > button {{
        background-color: #2B3674 !important;
        color: white !important;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1.3rem;
        font-weight: 500;
        width: 100%;
        box-shadow: 0 6px 20px rgba(43, 54, 116, 0.25);
        border: none;
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: #1A2156 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(43, 54, 116, 0.3);
    }}

    div[data-testid="column"] {{
        display: flex !important;
        height: 400px !important;
    }}

    div[data-testid="column"] > div {{
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: stretch !important;
    }}

    .column-container {{
        height: 320px;
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
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}

    .column-container:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(43, 54, 116, 0.2);
    }}

    .icon-container {{
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }}

    .logo-large {{
        width: 80px;
        height: 80px;
        margin-bottom: 0.5rem;
        animation: floatSlow 4s ease-in-out infinite;
        filter: drop-shadow(0 4px 8px rgba(43, 54, 116, 0.2));
    }}

    .profile-icon {{
        font-size: 4rem;
        margin-bottom: 0.5rem;
        animation: float 3.5s ease-in-out infinite;
        animation-delay: 0.5s;
    }}

    @keyframes floatSlow {{
        0% {{ transform: translateY(0px) rotate(0deg); }}
        33% {{ transform: translateY(-8px) rotate(2deg); }}
        66% {{ transform: translateY(-4px) rotate(-1deg); }}
        100% {{ transform: translateY(0px) rotate(0deg); }}
    }}

    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0px); }}
    }}

    /* Responsive */
    @media (max-width: 768px) {{
        .hero {{
            height: 300px;
            padding: 1rem;
        }}
        
        .hero h1 {{
            font-size: 2.5rem;
        }}
        
        .hero p {{
            font-size: 1.2rem;
        }}
        
        .column-container {{
            height: 280px;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# Hero section que ocupa todo el ancho superior
st.markdown("""
    <div class="hero-container">
        <div class="hero">
            <div class="hero-content">
                <h1>¡Tu Super Online!</h1>
                <p>Bienvenido a tu supermercado digital</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Contenido principal con el layout normal de Streamlit
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Crear columnas más centradas
col_left, col1, col2, col_right = st.columns([1, 2, 2, 1], gap="medium")

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

# Pie
st.markdown('<p class="info-highlight">¡Disfruta de la mejor experiencia de compra online!</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)