import streamlit as st

# --- Simulamos sesión y DB ---
# Por ejemplo, en st.session_state guardamos el usuario logueado:
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None  # None si no está logueado

# Simulamos función para traer últimas 3 compras:
def obtener_ultimas_compras(user_id):
    # Aquí iría consulta real a la base de datos
    # Retornamos lista de diccionarios como ejemplo
    return [
        {"fecha": "2025-06-01", "producto": "Manzana", "monto": 150},
        {"fecha": "2025-05-20", "producto": "Leche", "monto": 120},
        {"fecha": "2025-05-15", "producto": "Pan", "monto": 80},
    ]

# Simulamos función para actualizar usuario:
def actualizar_usuario(user_id, nombre, email, telefono, codigo_postal, direccion):
    # Aquí actualizarías en la DB los datos del usuario con user_id
    # Ejemplo solo imprime:
    print(f"Actualizando usuario {user_id} con {nombre}, {email}, {telefono}, {codigo_postal}, {direccion}")

# --- Estilos personalizados ---
st.markdown("""
    <style>
    /* NO TOCAR EL SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #2C3E50 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
        font-family: 'Poppins', sans-serif !important;
    }

    /* FONDO DE LA APP (header + body) */
    html, body, .stApp, #root, header, main, section {
        background-color: #D4DFF0 !important;
        font-family: 'Inter', sans-serif !important;
        color: #2B3674 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .block-container {
        max-width: 700px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        margin: auto !important;
    }

    h1, h2, h3, h4 {
        color: #2B3674 !important;
    }

    .stButton > button {
        background-color: #2B3674 !important;
        color: white !important;
        padding: 14px 30px !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        margin: 10px 0 !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
    }

    .stButton > button:hover {
        background-color: #1A2156 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(26, 33, 86, 0.35) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Interfaz ---

st.markdown("## Mi Perfil 👤")

if st.session_state["user_id"] is None:
    st.warning("Debes iniciar sesión para ver o modificar tu perfil.")
    st.stop()

# Si el usuario está logueado, puedes cargar sus datos de la base y mostrar:
# Aquí solo valores en blanco como ejemplo
nombre = st.text_input("Nombre", value="")
email = st.text_input("Email", value="")
telefono = st.text_input("Número de teléfono", value="")
codigo_postal = st.text_input("Código postal", value="")
direccion = st.text_input("Dirección", value="")

col1, col2 = st.columns(2)

with col1:
    if st.button("Historial de compras"):
        compras = obtener_ultimas_compras(st.session_state["user_id"])
        st.write("Últimas 3 compras:")
        for compra in compras:
            st.write(f"{compra['fecha']}: {compra['producto']} - ${compra['monto']}")

with col2:
    if st.button("Guardar cambios"):
        actualizar_usuario(st.session_state["user_id"], nombre, email, telefono, codigo_postal, direccion)
        st.success("Cambios guardados correctamente.")
