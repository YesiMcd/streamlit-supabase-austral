import streamlit as st
from PIL import Image
from io import BytesIO
import base64
from conexion import get_supabase_client
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(layout="wide")

# Inicializar cliente de Supabase
supabase = get_supabase_client()

# --- Funciones auxiliares ---
def image_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def configure_sidebar():
    """Configura el sidebar para mostrar solo las páginas principales."""
    
    # Aplicar CSS para ocultar todas las páginas excepto las principales
    st.markdown("""
        <style>
            /* Ocultar todas las páginas por defecto */
            div[data-testid="stSidebarNav"] ul {
                display: none !important;
            }
            
            /* Mostrar solo las páginas permitidas */
            div[data-testid="stSidebarNav"] ul li:nth-child(1), /* Inicio */
            div[data-testid="stSidebarNav"] ul li:nth-child(2), /* Registro */
            div[data-testid="stSidebarNav"] ul li:nth-child(3) { /* Tu Super online */
                display: block !important;
            }
            
            /* Ocultar específicamente las páginas no deseadas */
            div[data-testid="stSidebarNav"] ul li:nth-child(n+4) {
                display: none !important;
            }
            
            /* Estilo del sidebar - fondo completo */
            div[data-testid="stSidebar"] {
                background-color: #5b7d9e !important;
            }
            
            div[data-testid="stSidebar"] > div {
                background-color: #5b7d9e !important;
            }
            
            div[data-testid="stSidebar"] .sidebar-content {
                background-color: #5b7d9e !important;
            }
            
            section[data-testid="stSidebar"] {
                background-color: #5b7d9e !important;
            }
            
            section[data-testid="stSidebar"] > div {
                background-color: #5b7d9e !important;
            }
            
            /* Estilo del título de navegación - posicionado más arriba */
            div[data-testid="stSidebar"] h1 {
                margin-top: -10px !important;
                padding-top: 15px !important;
                color: white !important;
                font-family: 'Poppins', sans-serif !important;
            }
            
            div[data-testid="stSidebar"] * {
                color: white !important;
                font-family: 'Poppins', sans-serif !important;
            }
            
            /* Estilo de los botones del sidebar - IMPORTANTE: asegurar que sean visibles */
            div[data-testid="stSidebar"] .stButton {
                display: block !important;
                visibility: visible !important;
            }
            
            div[data-testid="stSidebar"] .stButton > button {
                background-color: #4b6783 !important;
                color: white !important;
                font-size: 16px !important;
                font-weight: 600 !important;
                padding: 12px 20px !important;
                margin: 8px 0 !important;
                border-radius: 10px !important;
                transition: all 0.3s ease !important;
                width: 100% !important;
                border: none !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
            }
            
            div[data-testid="stSidebar"] .stButton > button:hover {
                background-color: #3a5570 !important;
                transform: translateX(5px) !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }
            
            /* Asegurar que el contenedor del sidebar sea visible */
            div[data-testid="stSidebar"] .element-container {
                display: block !important;
                visibility: visible !important;
            }
            
            /* Estilo para los enlaces de navegación */
            div[data-testid="stSidebarNav"] ul li a {
                font-size: 18px !important;
                font-weight: 600 !important;
                padding: 12px 20px !important;
                margin: 8px 0 !important;
                border-radius: 10px !important;
                transition: all 0.3s ease !important;
                display: block !important;
                text-decoration: none !important;
            }
            div[data-testid="stSidebarNav"] ul li a:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
                transform: translateX(5px) !important;
            }
            div[data-testid="stSidebarNav"] ul li a.active {
                background-color: rgba(255, 255, 255, 0.2) !important;
                font-weight: 700 !important;
            }
                <style>
            /* Oculta los tooltips blancos tipo "key=..." */
            [title^="key="] {
             display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Configurar el sidebar
    with st.sidebar:
        st.title("Navegación")
        
        # Agregar botón para Inicio (página principal) - PRIMERO
        if st.button("🏠 Inicio", key="nav_inicio", use_container_width=True):
            st.switch_page("Inicio.py")
        
        # Obtener páginas disponibles en la carpeta pages
        pages_dir = "pages"
        allowed_pages = ["Registro"]  # Páginas permitidas sin incluir Inicio
        
        if os.path.exists(pages_dir):
            for page_name in allowed_pages:  # Usar orden específico
                file_path = f"{pages_dir}/{page_name}.py"
                if os.path.exists(file_path):
                    # Agregar iconos para hacer más visual
                    icon = "📝" if page_name == "Registro" else "🛒"
                    if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
                        st.switch_page(f"pages/{page_name}.py")
        
# EJECUTAR LA CONFIGURACIÓN DEL SIDEBAR
configure_sidebar()

# Estilo personalizado reforzado para el sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #5b7d9e !important;
    }
    [data-testid="stSidebar"] .sidebar-content {
        background-color: #5b7d9e !important;
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
    
    /* Estilos específicos para los botones del sidebar */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #4b6783 !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 12px 20px !important;
        margin: 8px 0 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #3a5570 !important;
        transform: translateX(5px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Cargar imágenes ---
logo = Image.open("logo_carrito.png")
logo_b64 = image_to_base64(logo)

titulo_bg = Image.open("fondo del titulo.jpg")
titulo_bg_b64 = image_to_base64(titulo_bg)

login_img = Image.open("imagen_login3.jpg")
login_img_b64 = image_to_base64(login_img)

gradiente_img = Image.open("gradiente2.jpg")
gradiente_img_b64 = image_to_base64(gradiente_img)

gradiente2_img = Image.open("gradiente2.jpg")
gradiente2_img_b64 = image_to_base64(gradiente2_img)

# --- Estilos personalizados ---
st.markdown(f"""
    <style>
        .stApp {{
            background-color: #D4DFF0 !important;
        }}

        header, footer, [data-testid="stToolbar"] {{
            display: none !important;
        }}
        
        .block-container {{
            padding-top: 0rem;
        }}
        .header-container {{
            background-image: url('data:image/png;base64,{titulo_bg_b64}');
            background-size: cover;
            background-position: center;
            padding: 3px 30px;
            display: flex;
            align-items: center;
            gap: 8px;
            width: 100%;
            height: 100px;
            margin-top: 45px;
            margin-bottom: 20px;
            border-radius: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }}
        .header-container img {{
            height: 70px;
            margin: 0;
        }}
        .header-container h3 {{
            color: #0C517E;
            font-size: 32px;
            font-family: 'Nunito', 'Arial', sans-serif;
            font-weight: 600;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2),
                         -1px -1px 0 rgba(255, 255, 255, 0.3);
            margin: 0;
            letter-spacing: 0.5px;
        }}
        .right-column {{
            background-image: url('data:image/png;base64,{gradiente2_img_b64}');
            background-size: cover;
            background-position: center;
            border-radius: 30px;
            padding: 30px;
            height: 550px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            position: relative;
            margin-top: -520px;
        }}
        [data-testid="stForm"] {{
            position: relative;
            z-index: 2;
            background: rgba(255, 255, 255, 0.3);
            width: 100%;
            max-width: 550px;
            margin: 0 auto;
            margin-top: 25px;
            padding: 40px;
            border-radius: 30px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}
        .form-title {{
            color: white;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 30px;
            font-family: 'Nunito', 'Arial', sans-serif;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }}
        /* Estilos para los inputs de Streamlit */
        [data-testid="stTextInput"] > div > div > input {{
            border: 1px solid #4A90E2 !important;
            border-radius: 8px !important;
            padding: 12px !important;
            background: white !important;
            color: #333 !important;
            outline: none !important;
        }}
        [data-testid="stTextInput"] > div > div > input:focus {{
            border: 1px solid #0C517E !important;
            box-shadow: none !important;
        }}
        [data-testid="stTextInput"] > div > div > input:invalid {{
            border: 1px solid #4A90E2 !important;
            box-shadow: none !important;
        }}
        /* Estilos para el contenedor base de Streamlit */
        [data-baseweb="input"] {{
            border: none !important;
            background: white !important;
            border-radius: 8px !important;
        }}
        [data-baseweb="input"] > div {{
            border: none !important;
            background: white !important;
            border-radius: 8px !important;
        }}
        [data-baseweb="input"] > div:hover {{
            border: none !important;
            box-shadow: none !important;
        }}
        [data-baseweb="input"] > div:focus-within {{
            border: none !important;
            box-shadow: none !important;
        }}
        /* Estilos para el checkbox */
        .stCheckbox > div {{
            color: #333 !important;
        }}
        .password-link {{
            text-align: right;
            font-size: 13px;
            color: #0C517E;
            text-decoration: underline;
            margin-top: -10px;
            margin-bottom: 20px;
        }}
        .stFormSubmitButton > button {{
            background-color: #0C517E !important;
            color: white !important;
            border: none !important;
            width: 100% !important;
            padding: 12px !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            margin-top: 20px !important;
            box-shadow: 0 4px 10px rgba(12, 81, 126, 0.2) !important;
            transition: all 0.3s ease !important;
        }}
        .stFormSubmitButton > button:hover {{
            background-color: #083652 !important;
            transform: scale(1.02) !important;
        }}
        .left-column {{
            background-image: url('data:image/png;base64,{login_img_b64}');
            background-size: cover;
            background-position: center;
            border-radius: 30px;
            padding: 30px;
            height: 550px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
        }}
        
        .register-box {{
            position: absolute;
            top: 20px;
            right: 20px;
            background-color: transparent;
            padding: 25px 30px;
            border-radius: 18px;
            text-align: center;
            z-index: 2;
            box-shadow: none;
            backdrop-filter: none;
        }}
        .register-box p {{
            color: #0C517E;
            font-size: 22px;
            font-weight: bold;
            margin: 0 0 20px 0;
        }}
        .register-box button {{
            background-color: #0C517E !important;
            color: white !important;
            padding: 14px 28px !important;
            border-radius: 25px !important;
            border: none !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(12, 81, 126, 0.3) !important;
        }}
        .register-box button:hover {{
            background-color: #083652 !important;
            transform: scale(1.03) !important;
        }}
    </style>
    <script>
        // Función para inspeccionar los elementos de Streamlit
        function inspectStreamlitElements() {{
            const inputs = document.querySelectorAll('[data-testid="stTextInput"]');
            inputs.forEach(input => {{
                console.log('Input element:', input);
                console.log('Classes:', input.className);
                console.log('Parent classes:', input.parentElement.className);
            }});
        }}
        // Ejecutar la inspección cuando el documento esté listo
        document.addEventListener('DOMContentLoaded', inspectStreamlitElements);
    </script>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(f"""
<div class="header-container">
    <img src="data:image/png;base64,{logo_b64}">
    <h3>SuperListo</h3>
</div>
""", unsafe_allow_html=True)

# --- Dos columnas ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="left-column">
        <div class="register-box">
            <p>¿Todavía no tenés cuenta?</p>
            <form action="/Registro" method="get">
                <button type="submit">Registrate</button>
            </form>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    with st.form("login_form", clear_on_submit=False):
        st.markdown("<div class='form-title'>Iniciar sesión</div>", unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="Tu correo", key="email")
        password = st.text_input("Contraseña", type="password", placeholder="Tu contraseña", key="password")
        recordar = st.checkbox("Recordarme", key="recordarme")
        st.markdown("<div class='password-link'><a href='#'>¿Olvidaste tu contraseña?</a></div>", unsafe_allow_html=True)
        
        enviar = st.form_submit_button("INGRESAR")
    
    st.markdown("""
    <div class="right-column">
    </div>
    """, unsafe_allow_html=True)

    # Lógica de autenticación
    if enviar:
        if email and password:
            try:
                response = supabase.table("Cliente").select("*").eq("email", email).eq("Contraseña", password).execute()
                if response.data and len(response.data) > 0:
                    st.session_state.user_email = email
                    st.switch_page("pages/Tu Super online.py")
                else:
                    st.error("No existe una cuenta con estas credenciales")
            except Exception as e:
                st.error(f"Error al verificar las credenciales: {str(e)}")
        else:
            st.warning("Por favor completá todos los campos")

# ESTILOS CSS GLOBALES PARA FORZAR EL COLOR BLANCO DEL TÍTULO
st.markdown("""
    <style>
    /* ESTILOS NUCLEARES PARA EL SIDEBAR */
    [data-testid="stSidebar"] div span {
        color: white !important;
    }
    
    [data-testid="stSidebar"] div div span {
        color: white !important;
    }
    
    [data-testid="stSidebar"] * span {
        color: white !important;
    }
    
    /* Forzar color blanco en cualquier elemento del sidebar */
    [data-testid="stSidebar"] div[style*="font-size: 1.5rem"] span {
        color: white !important;
        background-color: transparent !important;
    }
    
    /* Sobrescribir cualquier color heredado */
    [data-testid="stSidebar"] span {
        color: white !important;
        color: white !important;
        color: white !important;
    }
    
    /* Forzar color blanco en el título h1 del sidebar */
    [data-testid="stSidebar"] h1 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .st-emotion-cache-n14c82 h1 {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)