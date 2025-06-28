import streamlit as st
from PIL import Image
import base64
import os

# Configuración de página
st.set_page_config(
    page_title="Tu Super Online",
    layout="centered"
)

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
            div[data-testid="stSidebarNav"] ul li:nth-child(2), /* Registro */
            div[data-testid="stSidebarNav"] ul li:nth-child(3) { /* Tu Super online */
            div[data-testid="stSidebarNav"] ul li:nth-child(1), /* Inicio */            
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
            
            /* Estilo del título de navegación - ELIMINADO - se maneja con div inline */
            
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
                display: block !important;
                visibility: visible !important;
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
        </style>
    """, unsafe_allow_html=True)
    
    # Configurar el sidebar
    with st.sidebar:
        # Usar span con color blanco específico
        st.markdown('<div style="font-size: 1.5rem; font-weight: 600; margin: 1.25rem 0px 1rem; font-family: Poppins; background-color: transparent !important;"><span style="color: white !important; background-color: transparent !important;">Navegación</span></div>', unsafe_allow_html=True)
        

        # Obtener páginas disponibles en la carpeta pages
        pages_dir = "pages"
        allowed_pages = []  # Sin páginas permitidas ya que el usuario está logueado
        
        if os.path.exists(pages_dir):
            for page_name in allowed_pages:  # Usar orden específico
                file_path = f"{pages_dir}/{page_name}.py"
                if os.path.exists(file_path):
                    # Agregar iconos para hacer más visual
                    icon = "📝" if page_name == "Registro" else "🛒"
                    if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
                        st.switch_page(f"pages/{page_name}.py")
        
        # Agregar botón para Carrito
        if st.button("🛒 Carrito", key="nav_carrito", use_container_width=True):
            st.switch_page("pages/Buscador de productos.py")
        
        # Agregar botón para Mi perfil
        if st.button("👤 Mi perfil", key="nav_mi_perfil", use_container_width=True):
            st.switch_page("pages/Mi perfil.py")
        
        # Agregar botón para Cerrar sesión al final
        if st.button("🚪 Cerrar sesión", key="nav_cerrar_sesion", use_container_width=True):
            # Limpiar la sesión
            st.session_state.clear()
            st.switch_page("Inicio.py")

# EJECUTAR LA CONFIGURACIÓN DEL SIDEBAR
configure_sidebar()

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


# Estilos CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    .stApp {{
        background-color: #D4DFF0 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0 !important;
    }}

    /* Sidebar styling */
    /* Los estilos del sidebar se manejan en la función configure_sidebar() */

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
    
    /* ELIMINAR TODAS LAS EXCEPCIONES DEL SIDEBAR - se maneja con div inline */

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
    </style>
""", unsafe_allow_html=True)
