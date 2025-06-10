import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Buscador de Productos",
    page_icon="🔍",
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
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
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
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        font-size: 16px;
        transition: all 0.3s ease;
        margin: 5px;
    }
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .nav-button {
        position: fixed;
        bottom: 20px;
        width: 45%;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar la lista de productos en session_state si no existe
if 'productos' not in st.session_state:
    st.session_state.productos = [
        "Manzanas",
        "Bananas",
        "Leche",
        "Pan",
        "Huevos",
        "Arroz",
        "Yogur",
        "Queso",
        "Pollo",
        "Pasta"
    ]

if 'seleccionados' not in st.session_state:
    st.session_state.seleccionados = []

# Buscador con placeholder
busqueda = st.text_input(
    "",
    placeholder="🔍 Buscar producto",
)

# Filtrar productos basado en la búsqueda
productos_filtrados = [
    producto for producto in st.session_state.productos
    if busqueda.lower() in producto.lower()
] if busqueda else st.session_state.productos

# Mostrar resultados con botones de selección
for producto in productos_filtrados:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(producto)
    with col2:
        if st.button("Seleccionar", key=f"btn_{producto}"):
            if producto not in st.session_state.seleccionados:
                st.session_state.seleccionados.append(producto)
                st.success(f"¡{producto} agregado a la lista!")

# Espacio para separar los resultados de los botones de navegación
st.markdown("<br>" * 3, unsafe_allow_html=True)

# Botones de navegación en la parte inferior
col1, col2 = st.columns(2)

with col1:
    if st.button("← Atrás", use_container_width=True):
        # Aquí puedes agregar la lógica para volver atrás
        st.session_state["page"] = "anterior"

with col2:
    if st.button("Terminar y ver lista ✓", use_container_width=True):
        # Mostrar los productos seleccionados
        st.write("Productos seleccionados:")
        for producto in st.session_state.seleccionados:
            st.write(f"- {producto}")
        st.session_state["page"] = "lista"