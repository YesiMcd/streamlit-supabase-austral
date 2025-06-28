import streamlit as st
import os

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
            
            /* Estilo del sidebar */
            div[data-testid="stSidebar"] {
                background-color: #5b7d9e !important;
            }
            div[data-testid="stSidebar"] * {
                color: white !important;
                font-family: 'Poppins', sans-serif !important;
            }
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
    
    # Obtener la lista de páginas permitidas
    allowed_pages = [
        "Inicio",
        "Tu Super online"
    ]
    
    # Obtener todas las páginas disponibles
    pages_dir = "pages"
    available_pages = []
    for file in os.listdir(pages_dir):
        if file.endswith(".py") and file != "__init__.py":
            page_name = file.replace(".py", "")
            if page_name in allowed_pages:
                available_pages.append(page_name)
    
    # Configurar el sidebar
    with st.sidebar:
        st.title("Navegación")
        
        # Mostrar solo las páginas permitidas
        for page in available_pages:
            if st.button(page, key=f"nav_{page}"):
                st.switch_page(f"pages/{page}.py")
        
        # Agregar botón para Mi perfil
        if st.button("👤 Mi perfil", key="nav_mi_perfil", use_container_width=True):
            st.switch_page("pages/Mi perfil.py")
        
        # Agregar botón para Cerrar sesión al final
        if st.button("🚪 Cerrar sesión", key="nav_cerrar_sesion", use_container_width=True):
            # Limpiar la sesión
            st.session_state.clear()
            st.switch_page("Inicio.py") 