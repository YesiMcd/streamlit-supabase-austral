import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Tu Super Online",
    page_icon="🛒",
    layout="centered"
)

# Aplicar estilo personalizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 30px;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Mensaje de bienvenida al principio
st.title("🛒 Tu Super Online")
st.markdown("¡Bienvenido a tu experiencia de compra!")
st.info("Selecciona una opción para comenzar")

# Espacio para separar
st.markdown("<br>", unsafe_allow_html=True)

# Título principal con emoji de carrito


# Espacio para separar el título de los botones
st.markdown("<br>", unsafe_allow_html=True)

# Crear dos columnas para los botones
col1, col2 = st.columns(2)

with col1:
    if st.button("🛒 Crear Carrito", use_container_width=True):
        st.session_state["page"] = "carrito"
        st.success("¡Creando nuevo carrito de compras!")
        # Aquí puedes agregar la lógica para crear el carrito

with col2:
    if st.button("👤 Mi Perfil", use_container_width=True):
        st.session_state["page"] = "perfil"
        st.success("Accediendo a tu perfil...")
        # Aquí puedes agregar la lógica para mostrar el perfil