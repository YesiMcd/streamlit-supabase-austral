import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Tu Super Online",
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
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* Forzar el color de fondo en múltiples elementos de Streamlit */
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
    
    .block-container {
        background: #D4DFF0 !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #D4DFF0 !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #D4DFF0 !important;
    }

    /* Centrar título y subtítulo */
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
        font-family: 'Inter', sans-serif;
    }

    h1 {
        font-size: 3rem;
        font-weight: 700;
        color: #2B3674;
        margin-top: 2rem;
        font-family: 'Inter', sans-serif;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #707EAE;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }

    .info-highlight {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2B3674;
        margin-top: 1.5rem;
        font-family: 'Inter', sans-serif;
    }

    .stButton > button {
        background-color: #2B3674 !important;
        color: white !important;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1.3rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 6px 20px rgba(43, 54, 116, 0.25), 
                    0 2px 6px rgba(43, 54, 116, 0.15);
        border: none;
    }

    .stButton > button:hover {
        background-color: #1A2156 !important;
        box-shadow: 0 4px 12px rgba(43, 54, 116, 0.15);
        transform: translateY(-2px);
    }

    .background-decoration {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #D4DFF0;
        z-index: -1;
    }

    .background-circles {
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }

    .circle {
        position: absolute;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(43, 54, 116, 0.1), rgba(43, 54, 116, 0.05));
    }

    .circle-1 {
        width: 300px;
        height: 300px;
        top: -100px;
        right: -100px;
    }

    .circle-2 {
        width: 200px;
        height: 200px;
        bottom: -50px;
        left: -50px;
    }

    .icon-container {
        text-align: center;
        margin-bottom: 1rem;
    }

    .icon-large {
        font-size: 4rem;
        margin-bottom: 0.5rem;
        display: block;
    }

   .column-container {
        padding: 1.5rem;
        border-radius: 15px;
        /* Fondo más opaco y con mejor contraste */
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        margin: 0.5rem;
        transition: all 0.3s ease;
        /* Sombra más pronunciada para resaltar del fondo */
        box-shadow: 0 10px 30px rgba(43, 54, 116, 0.15),
                     0 4px 12px rgba(43, 54, 116, 0.1),
                    0 2px 6px rgba(0, 0, 0, 0.05);
        /* Borde sutil para mejor definición */
        border: 1px solid rgba(255, 255, 255, 0.8);
    }

    .column-container:hover {
        transform: translateY(-8px);
        /* Sombra más intensa en hover */
        box-shadow: 0 15px 40px rgba(43, 54, 116, 0.2),
                    0 6px 16px rgba(43, 54, 116, 0.15),
                    0 3px 8px rgba(0, 0, 0, 0.1);
        /* Fondo ligeramente más opaco en hover */
        background: rgba(255, 255, 255, 0.95);
    }
    </style>

    <div class="background-decoration">
        <div class="background-circles">
            <div class="circle circle-1"></div>
            <div class="circle circle-2"></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Contenido principal - Título y subtítulo centrados
st.markdown("""
    <div class="title-container">
        <h1>¡Tu Super Online!</h1>
        <p class="subtitle">Bienvenido a tu supermercado digital</p>
    </div>
""", unsafe_allow_html=True)

# Crear dos columnas para los botones
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="column-container">
            <div class="icon-container">
                <span class="icon-large">🛒</span>
                <h3 style="color: #2B3674; margin: 0;">Carrito</h3>
                <p style="color: #707EAE; font-size: 1.5rem;">Comienza tu compra</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Crear Carrito", key="crear_carrito"):
        st.success("¡Carrito creado exitosamente!")
        # Aquí puedes agregar la lógica para crear el carrito

with col2:
    st.markdown("""
        <div class="column-container">
            <div class="icon-container">
                <span class="icon-large">👤</span>
                <h3 style="color: #2B3674; margin: 0;">Mi Perfil</h3>
                <p style="color: #707EAE; font-size: 1.5rem;">Gestiona tu cuenta</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Acceder al Perfil", key="acceder_perfil"):
        st.info("Accediendo a tu perfil...")
        # Aquí puedes agregar la lógica para acceder al perfil

# Información adicional
st.markdown('<p class="info-highlight">¡Disfruta de la mejor experiencia de compra online!</p>', unsafe_allow_html=True)