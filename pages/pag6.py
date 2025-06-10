import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Datos de la Tarjeta",
    page_icon="💳",
    layout="centered"
)

# Estilo personalizado
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        border: none;
        font-size: 16px;
        transition: all 0.3s ease;
        margin: 10px 0;
    }
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .tipo-tarjeta {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .pagar-button > button {
        background-color: #2196F3;
        font-size: 18px;
        padding: 20px 40px;
    }
    .pagar-button > button:hover {
        background-color: #1976D2;
    }
    </style>
""", unsafe_allow_html=True)

# Título de la página
st.title("💳 Datos de la Tarjeta")

# Crear un formulario para los datos
with st.form("formulario_tarjeta"):
    # Número de tarjeta
    numero_tarjeta = st.text_input(
        "Número de la Tarjeta",
        max_chars=16,
        help="Ingrese los 16 dígitos de su tarjeta"
    )

    # Fila para fecha y código
    col1, col2 = st.columns(2)
    
    with col1:
        fecha_vencimiento = st.text_input(
            "Fecha de Vencimiento",
            placeholder="MM/AA",
            max_chars=5,
            help="Formato: MM/AA"
        )
    
    with col2:
        codigo_seguridad = st.text_input(
            "Código de Seguridad",
            type="password",
            max_chars=4,
            help="3 o 4 dígitos en el reverso de su tarjeta"
        )

    # Nombre en la tarjeta
    nombre_tarjeta = st.text_input(
        "Nombre en la Tarjeta",
        help="Como aparece en la tarjeta"
    )

    # Tipo de tarjeta (Crédito/Débito)
    st.markdown("### Tipo de Tarjeta")
    tipo_tarjeta = st.radio(
        "Seleccione el tipo de tarjeta",
        options=["Débito", "Crédito"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # Espacio para separar
    st.markdown("<br>", unsafe_allow_html=True)

    # Botón de pagar
    submitted = st.form_submit_button(
        "PAGAR",
        use_container_width=True,
        type="primary"
    )

    if submitted:
        # Validaciones básicas
        if not numero_tarjeta or not fecha_vencimiento or not codigo_seguridad or not nombre_tarjeta:
            st.error("Por favor, complete todos los campos")
        else:
            # Aquí puedes agregar más validaciones específicas
            st.success("¡Pago procesado con éxito!")
            st.session_state["pago_completado"] = True

# Botón para volver atrás
if st.button("← Volver", use_container_width=True):
    st.session_state["page"] = "anterior"