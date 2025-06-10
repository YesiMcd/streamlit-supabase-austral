import streamlit as st
import re

# Configuración de la página
st.set_page_config(page_title="Registro", page_icon="🛒", layout="centered")

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



# --- Estilo personalizado ---
st.markdown("""
    <style>
        h1, h3, .stTextInput > label, .stCheckbox > label, .stPassword > label {
            color: #FFA500; /* Naranja */
        }
        .stButton > button {
            background-color: #FFA500;
            color: white;
            border: none;
            border-radius: 5px;
        }
        .stButton > button:hover {
            background-color: #e69500;
        }
        .stMarkdown hr {
            border: 1px solid #FFA500;
        }
    </style>
""", unsafe_allow_html=True)

# --- Título principal ---
st.markdown("""
    <h1 style='text-align: center;'>🛒 Registra tu Cuenta</h1>
    <p style='text-align: center; color: gray;'>Completa el formulario para crear tu cuenta en <strong style='color: #FFA500;'>Super Listo</strong></p>
    <hr>
""", unsafe_allow_html=True)

# --- Validaciones ---
def es_email_valido(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def es_codigo_postal_valido(cp):
    return cp.isdigit() and len(cp) >= 4

# --- Formulario ---
with st.form("form_registro", clear_on_submit=False):
    st.subheader("🧍 Datos personales")

    nombre = st.text_input("Nombre completo")
    email = st.text_input("Correo electrónico")
    direccion = st.text_input("Dirección")
    codigo_postal = st.text_input("Código Postal")
    mayor_edad = st.checkbox("Soy mayor de edad")

    st.subheader("🔐 Seguridad")
    password = st.text_input("Contraseña", type="password")
    confirmar_password = st.text_input("Confirmar contraseña", type="password")

    registrar = st.form_submit_button("Crear cuenta")

    if registrar:
        if not all([nombre, email, direccion, codigo_postal, password, confirmar_password]):
            st.error("❗ Todos los campos son obligatorios.")
        elif not es_email_valido(email):
            st.error("❗ Correo electrónico inválido.")
        elif not es_codigo_postal_valido(codigo_postal):
            st.error("❗ Código postal inválido (mínimo 4 dígitos numéricos).")
        elif password != confirmar_password:
            st.error("❗ Las contraseñas no coinciden.")
        elif len(password) < 6:
            st.error("❗ La contraseña debe tener al menos 6 caracteres.")
        elif not mayor_edad:
            st.error("❗ Debes ser mayor de edad para registrarte.")
        else:
            st.success("✅ Cuenta creada exitosamente!.")
            st.balloons()
            # Aquí puedes guardar los datos o redirigir al usuario