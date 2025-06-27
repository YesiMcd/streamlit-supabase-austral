import streamlit as st
import os

import streamlit as st
import os

# --- Función para configurar el sidebar ---
def configure_sidebar():
    """Configura el sidebar para mostrar solo las páginas principales."""
    
    # Aplicar CSS personalizado
    st.markdown("""
        <style>
            /* Ocultar todas las páginas por defecto */
            div[data-testid="stSidebarNav"] ul {
                display: none !important;
            }

            /* Mostrar solo las primeras tres páginas */
            div[data-testid="stSidebarNav"] ul li:nth-child(1),
            div[data-testid="stSidebarNav"] ul li:nth-child(2),
            div[data-testid="stSidebarNav"] ul li:nth-child(3) {
                display: block !important;
            }

            /* Ocultar páginas adicionales */
            div[data-testid="stSidebarNav"] ul li:nth-child(n+4) {
                display: none !important;
            }

            /* Fondo del sidebar */
            div[data-testid="stSidebar"],
            div[data-testid="stSidebar"] > div,
            div[data-testid="stSidebar"] .sidebar-content,
            section[data-testid="stSidebar"],
            section[data-testid="stSidebar"] > div {
                background-color: #5b7d9e !important;
            }

            /* Título del sidebar con fondo igual y letras negras */
            div[data-testid="stSidebar"] h1,
            div[data-testid="stSidebar"] h1 span {
                color: black !important;
                background-color: #5b7d9e !important;
                margin-top: -10px !important;
                padding: 15px !important;
                font-family: 'Poppins', sans-serif !important;
                border-radius: 10px;
                text-shadow: none !important;
            }

            /* Estilo general del sidebar */
            div[data-testid="stSidebar"] * {
                color: white !important;
                font-family: 'Poppins', sans-serif !important;
            }

            /* Botones del sidebar */
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

            /* Estilo de enlaces de navegación */
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

    # Contenido del sidebar
    with st.sidebar:
        st.title("Navegación")

        if st.button("🏠 Inicio", key="nav_inicio", use_container_width=True):
            st.switch_page("Inicio.py")

        pages_dir = "pages"
        allowed_pages = ["Registro", "Tu Super online"]

        if os.path.exists(pages_dir):
            for page_name in allowed_pages:
                file_path = f"{pages_dir}/{page_name}.py"
                if os.path.exists(file_path):
                    icon = "📝" if page_name == "Registro" else "🛒"
                    if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
                        st.switch_page(f"pages/{page_name}.py")
