import streamlit as st
from conexion import get_supabase_client

# Inicializar cliente de Supabase
supabase = get_supabase_client()

# Inicializar session_state si no existe
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

# Función para obtener datos del usuario
def obtener_datos_usuario(email):
    try:
        response = supabase.table('Cliente').select('*').eq('email', email).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Error al obtener datos del usuario: {e}")
        return None

# Función para actualizar usuario
def actualizar_usuario(id_cliente, nombre, email, direccion, codigo_postal, password):
    try:
        data = {
            'nombre': nombre,
            'email': email,
            'dirección': direccion,
            'código postal': codigo_postal,
            'Contraseña': password
        }
        response = supabase.table('Cliente').update(data).eq('id_cliente', id_cliente).execute()
        return True
    except Exception as e:
        st.error(f"Error al actualizar datos: {e}")
        return False

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

    /* Estilo para el botón de volver */
    .back-button {
        background-color: #6c757d !important;
    }
    .back-button:hover {
        background-color: #5a6268 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Interfaz ---
st.markdown("## Mi Perfil 👤")

# Botón de volver
if st.button("← Volver", key="back_button", help="Volver a la página anterior"):
    st.switch_page("pages/Tu Super online.py")

# Verificar si el usuario está logueado
if st.session_state["user_email"] is None:
    st.warning("Debes iniciar sesión para ver o modificar tu perfil.")
    st.stop()

# Obtener datos del usuario
datos_usuario = obtener_datos_usuario(st.session_state["user_email"])

if datos_usuario:
    # Mostrar formulario con datos actuales
    nombre = st.text_input("Nombre", value=datos_usuario.get('nombre', ''))
    email = st.text_input("Email", value=datos_usuario.get('email', ''))
    direccion = st.text_input("Dirección", value=datos_usuario.get('dirección', ''))
    codigo_postal = st.text_input("Código postal", value=datos_usuario.get('código postal', ''))
    password = st.text_input("Contraseña", value=datos_usuario.get('Contraseña', ''), type="password")

    if st.button("Guardar cambios"):
        if actualizar_usuario(datos_usuario['id_cliente'], nombre, email, direccion, codigo_postal, password):
            st.success("✅ Datos actualizados correctamente")
            # Actualizar email en session_state si cambió
            if email != st.session_state["user_email"]:
                st.session_state["user_email"] = email
            st.rerun()
else:
    st.error("No se pudieron cargar los datos del usuario. Por favor, intenta nuevamente.")
