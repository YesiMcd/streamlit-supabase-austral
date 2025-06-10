import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Forma de Pago",
    page_icon="💳",
    layout="centered"
)

# Estilo personalizado
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 20px 30px;
        border-radius: 10px;
        border: none;
        font-size: 18px;
        transition: all 0.3s ease;
        margin: 10px 0;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    div.stButton {
        text-align: center;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Título de la página
st.title("💰 Forma de Pago")

# Mensaje informativo
st.markdown("### Selecciona tu método de pago preferido")

# Espacio para separar
st.markdown("<br>", unsafe_allow_html=True)

# Contenedor para los botones
container = st.container()

with container:
    # Botón de Efectivo
    if st.button("💵 Efectivo", use_container_width=True):
        st.session_state["metodo_pago"] = "efectivo"
        st.success("Has seleccionado pago en efectivo")
        # Aquí puedes agregar la lógica adicional para el pago en efectivo

    # Espacio entre botones
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Botón de Tarjeta
    if st.button("💳 Tarjeta", use_container_width=True):
        st.session_state["metodo_pago"] = "tarjeta"
        st.success("Has seleccionado pago con tarjeta")
        # Aquí puedes agregar la lógica adicional para el pago con tarjeta

# Espacio para separar
st.markdown("<br>" * 2, unsafe_allow_html=True)

# Botón para volver atrás
if st.button("← Volver", use_container_width=True):
    st.session_state["page"] = "anterior"