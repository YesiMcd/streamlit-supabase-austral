import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import os

# --- Configuración de la página ---
st.set_page_config(
    page_title="Forma de Pago",
    page_icon="💳",
    layout="centered"
)

# --- Función para convertir imagen a base64 ---
def image_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

# --- Cargar imagen y convertir a base64 ---
logo_b64 = None
try:
    # Intentar cargar la imagen desde la raíz del proyecto
    logo_path = "fondo del titulo.jpg"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        logo_b64 = image_to_base64(logo_img)
    else:
        # Si no se encuentra la imagen, usar un color de fondo sólido
        st.markdown("""
            <div style="
                background-color: #2B3674;
                width: 100%;
                height: 100px;
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                margin-bottom: 20px;
            ">
                <h1 style='
                    font-size: 2.5rem;
                    color: white;
                    margin: 0;
                    text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
                '>💰 Forma de Pago</h1>
            </div>
        """, unsafe_allow_html=True)
except Exception as e:
    # Si hay algún error, usar un color de fondo sólido
    st.markdown("""
        <div style="
            background-color: #2B3674;
            width: 100%;
            height: 100px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            margin-bottom: 20px;
        ">
            <h1 style='
                font-size: 2.5rem;
                color: white;
                margin: 0;
                text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
            '>💰 Forma de Pago</h1>
        </div>
    """, unsafe_allow_html=True)

# --- Estilos globales ---
st.markdown("""
    <style>
    html, body, .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #D4DFF0 !important;
        font-family: 'Inter', sans-serif !important;
        color: #2B3674 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .block-container {
        max-width: 700px !important;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        margin: auto !important;
        background-color: #D4DFF0 !important;
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

    /* Separador decorativo */
    .linea-separadora {
        border-top: 1.5px solid #A8B8D8;
        margin: 30px auto 20px auto;
        width: 80%;
    }

    /* Ocultar/cambiar color del header y toolbar */
    header[data-testid="stHeader"] {
        background-color: #D4DFF0 !important;
        height: 0px !important;
    }
    
    .stToolbar {
        background-color: #D4DFF0 !important;
    }
    
    [data-testid="stToolbar"] {
        background-color: #D4DFF0 !important;
    }
    
    /* Remover cualquier cuadro blanco en la parte superior */
    .stApp > div:first-child,
    .stApp > header,
    .stApp > div[data-testid="stHeader"] {
        background-color: #D4DFF0 !important;
    }
    
    /* Si hay un elemento con clase específica que cause el cuadro blanco */
    div[data-testid="stVerticalBlock"] > div:first-child {
        background-color: #D4DFF0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Banner con título centrado ---
if logo_b64:
    st.markdown(f"""
        <div style="
            background-image: url('data:image/jpeg;base64,{logo_b64}');
            background-size: cover;
            background-position: center;
            width: 100%;
            height: 100px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            margin-bottom: 20px;
        ">
            <h1 style='
                font-size: 2.5rem;
                color: white;
                margin: 0;
                text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
            '>💰 Forma de Pago</h1>
        </div>
    """, unsafe_allow_html=True)

# --- Frase debajo del título ---
st.markdown("### Selecciona tu método de pago preferido")
st.markdown("<br>", unsafe_allow_html=True)

# --- Botones ---
if st.button("💵 Efectivo", use_container_width=True):
    st.session_state["metodo_pago"] = "efectivo"
    st.switch_page("pages/Pago en efectivo.py")

if st.button("💳 Tarjeta", use_container_width=True):
    st.session_state["metodo_pago"] = "tarjeta"
    st.switch_page("pages/Datos de la tarjeta.py")

# --- Separador decorativo ---
st.markdown('<div class="linea-separadora"></div>', unsafe_allow_html=True)

# --- Botón Volver ---
if st.button("← Volver", use_container_width=True):
    st.switch_page("pages/Buscador de productos.py")