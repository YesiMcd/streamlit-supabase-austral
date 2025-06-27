import streamlit as st
import os

# Configuración de la página
st.set_page_config(
    page_title="Datos de la Tarjeta",
    page_icon="💳",
    layout="centered"
)

# --- Función para configurar el sidebar ---
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
        st.title("Navegación")
        
        # Agregar botón para Inicio (página principal) - PRIMERO
        if st.button("🏠 Inicio", key="nav_inicio", use_container_width=True):
            st.switch_page("Inicio.py")
        
        # Obtener páginas disponibles en la carpeta pages
        pages_dir = "pages"
        allowed_pages = ["Registro", "Tu Super online"]  # Páginas permitidas sin incluir Inicio
        
        if os.path.exists(pages_dir):
            for page_name in allowed_pages:  # Usar orden específico
                file_path = f"{pages_dir}/{page_name}.py"
                if os.path.exists(file_path):
                    # Agregar iconos para hacer más visual
                    icon = "📝" if page_name == "Registro" else "🛒"
                    if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
                        st.switch_page(f"pages/{page_name}.py")

# --- Configurar el sidebar ---
configure_sidebar()

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