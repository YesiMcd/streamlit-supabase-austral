import streamlit as st  
import re
import base64
from PIL import Image
from datetime import datetime
import random
from conexion import get_supabase_client

# Inicializar cliente de Supabase
supabase = get_supabase_client()

# FUNCIÓN PARA CONVERTIR IMAGEN A BASE64
def get_base64_image(image_path):
    """Convierte una imagen a string base64 para usar en CSS"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"No se encontró la imagen en la ruta: {image_path}")
        return None

# FUNCIÓN PARA INSERTAR CLIENTE
def insertar_cliente(nombre, email, direccion, codigo_postal, password):
    try:
        # Obtener todos los IDs existentes
        response = supabase.table('Cliente').select('id_cliente').execute()
        ids_existentes = [registro['id_cliente'] for registro in response.data]
        
        # Generar un nuevo ID que no exista
        while True:
            id_cliente = random.randint(100, 999)
            if id_cliente not in ids_existentes:
                break
        
        data = {
            'id_cliente': id_cliente,
            'nombre': nombre,
            'email': email,
            'dirección': direccion,
            'código postal': codigo_postal,
            'Contraseña': password
        }
        response = supabase.table('Cliente').insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error al insertar en la base de datos: {e}")
        return False

# FUNCIÓN PARA MOSTRAR REGISTROS EXISTENTES
def mostrar_registros():
    try:
        response = supabase.table('Cliente').select('*').execute()
        if response.data:
            st.write("Registros existentes en la base de datos:")
            for registro in response.data:
                st.write(f"ID: {registro['id']}, Email: {registro['email']}")
        else:
            st.write("No hay registros en la base de datos.")
    except Exception as e:
        st.error(f"Error al consultar la base de datos: {e}")

# CONVERTIR LOGO A BASE64
logo = Image.open("logo_carrito.png")
logo_b64 = get_base64_image("logo_carrito.png")

# CONFIGURACIÓN DE LA IMAGEN DE FONDO
background_image_path = "fondo del titulo.jpg"  # ← CAMBIA ESTA RUTA
background_base64 = get_base64_image(background_image_path)

# CSS CON CUADRO BLANCO MEJORADO
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* IMAGEN DE FONDO */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{background_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}

    /* AJUSTAR EL CONTENEDOR PRINCIPAL */
    .main .block-container {{
        padding-top: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 800px !important;
    }}

    /* CUADRO BLANCO PARA EL CONTENIDO - APLICADO AL CONTENEDOR PRINCIPAL */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.65) !important;
        padding: 3rem 2.5rem !important;
        border-radius: 20px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 
                    0 10px 30px rgba(0, 0, 0, 0.2), 
                    0 5px 15px rgba(0, 0, 0, 0.15) !important;
        margin: 2rem auto !important;
        max-width: 780px !important;
        border: 1px solid #E0E0E0 !important;
        backdrop-filter: blur(10px) !important;
    }}

    /* CUADRO BLANCO ALTERNATIVO */
    .cuadro-blanco {{
        background-color: rgba(255, 255, 255, 0.65) !important;
        padding: 2rem !important;
        border-radius: 15px !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25) !important;
        margin: 1rem 0 !important;
        border: 1px solid #E0E0E0 !important;
    }}

    /* ESTILO GENERAL PARA TÍTULOS */
    h1, h2, h3 {{
        color: #2B3674 !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* ETIQUETAS DE INPUTS - MÁXIMA ESPECIFICIDAD */
    div[data-testid="stForm"] div[data-baseweb="form-control"] label,
    div[data-testid="stForm"] div[data-baseweb="form-control"] div[data-baseweb="label"] {{
        color: #1A2156 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
        line-height: 1.5 !important;
    }}

    /* SOBRESCRIBIR ESTILOS DE STREAMLIT */
    .stTextInput label,
    .stPassword label,
    .stCheckbox label,
    .stTextInput div[data-baseweb="label"],
    .stPassword div[data-baseweb="label"],
    .stCheckbox div[data-baseweb="label"] {{
        color: #1A2156 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        margin-bottom: 0.5rem !important;
        display: block !important;
        line-height: 1.5 !important;
    }}

    /* BOTONES */
    .stButton > button {{
        background-color: #2B3674 !important;
        color: white !important;
        padding: 0.8rem 2rem !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        margin-top: 1rem !important;
    }}

    .stButton > button:hover {{
        background-color: #1A2156 !important;
        transform: translateY(-2px) !important;
    }}

    /* INPUTS */
    .stTextInput > div > input, .stPassword > div > input {{
        border: 1px solid #E0E0E0 !important;
        background-color: #FAFAFA !important;
        font-family: 'Inter', sans-serif !important;
        color: #2B3674 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        transition: all 0.3s ease !important;
    }}

    .stTextInput > div > input:focus, .stPassword > div > input:focus {{
        border-color: #4A90E2 !important;
        background-color: #FFFFFF !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2) !important;
    }}

    /* Asegurar que el borde celeste solo aparezca al enfocar */
    [data-baseweb="input"] {{
        border: 1px solid #E0E0E0 !important;
    }}
    [data-baseweb="input"] > div {{
        border: 1px solid #E0E0E0 !important;
    }}
    [data-baseweb="input"] > div:hover {{
        border: 1px solid #E0E0E0 !important;
    }}
    [data-baseweb="input"] > div:focus-within {{
        border: 2px solid #4A90E2 !important;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2) !important;
    }}

    /* Eliminar bordes rojos */
    .stTextInput > div > input:invalid,
    .stPassword > div > input:invalid,
    .stTextInput > div > input:required,
    .stPassword > div > input:required {{
        border-color: #4A90E2 !important;
        box-shadow: none !important;
    }}

    /* ALERTAS */
    .stAlert {{
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        margin: 0.8rem 0 !important;
    }}

    /* CHECKBOX */
    .stCheckbox > label {{
        color: #2B3674 !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* FORMULARIO */
    .stForm {{
        background: rgba(255, 255, 255, 0.4) !important;
        border: none !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1),
                    0 4px 16px rgba(0, 0, 0, 0.08),
                    0 2px 8px rgba(0, 0, 0, 0.06) !important;
        padding: 2rem !important;
        border-radius: 15px !important;
        backdrop-filter: blur(8px) !important;
        width: 100% !important;
        max-width: 780px !important;
        margin: 0 auto !important;
    }}

    /* SUBHEADERS */
    .stForm h3 {{
        color: #2B3674 !important;
        font-family: 'Inter', sans-serif !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #E0E0E0 !important;
    }}

    /* ESPACIADO ENTRE ELEMENTOS */
    .stTextInput, .stPassword, .stCheckbox {{
        margin-bottom: 1.2rem !important;
    }}

    /* BARRA LATERAL */
    [data-testid="stSidebar"] {{
        background-color: #2C3E50 !important;
    }}
    [data-testid="stSidebar"] * {{
        color: white !important;
        font-family: 'Inter', sans-serif !important;
    }}

    [data-testid="stForm"] {{
        position: relative;
        z-index: 2;
        background: rgba(255, 255, 255, 0.4);
        width: 100%;
        max-width: 780px;
        margin: 0 auto;
        margin-top: 16px;
        padding: 40px;
        border-radius: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1),
                    0 4px 16px rgba(0, 0, 0, 0.08),
                    0 2px 8px rgba(0, 0, 0, 0.06) !important;
        backdrop-filter: blur(8px) !important;
    }}
    </style>
""", unsafe_allow_html=True)

# CONTENEDOR PRINCIPAL CON CUADRO BLANCO
st.markdown(f"""
<div class="cuadro-blanco">
    <h1 style='text-align: center; color: #2B3674; font-family: Inter, sans-serif; margin-bottom: 1rem; font-weight: 600;'>
        <img src="data:image/png;base64,{logo_b64}" alt="Logo" style="height: 60px; vertical-align: middle; margin-right: 15px;"> Registra tu Cuenta
    </h1>
    <p style='text-align: center; color: #707EAE; font-family: Inter, sans-serif; margin-bottom: 2rem;'>
        Completa el formulario para crear tu cuenta en <strong style='color: #2B3674;'>Super Listo</strong>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #2B3674; margin: 1.5rem 0;'>", unsafe_allow_html=True)

# FUNCIONES DE VALIDACIÓN
def es_email_valido(email):
    """Valida si el email tiene un formato válido"""
    if not email or email.strip() == "":
        return False
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+', email) is not None

def es_codigo_postal_valido(cp):
    """Valida si el código postal es válido"""
    if not cp or cp.strip() == "":
        return False
    return cp.isdigit() and len(cp) >= 4

# FORMULARIO PRINCIPAL
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

    # VALIDACIÓN
    if registrar:
        errores = []
        
        if not all([nombre.strip(), email.strip(), direccion.strip(), codigo_postal.strip(), password.strip(), confirmar_password.strip()]):
            errores.append("❗ Todos los campos son obligatorios.")
        else:
            if not es_email_valido(email):
                errores.append("❗ Correo electrónico inválido.")
            else:
                # Verificar si el email ya existe
                try:
                    response = supabase.table('Cliente').select('*').eq('email', email).execute()
                    if response.data and len(response.data) > 0:
                        errores.append("❗ Este correo electrónico ya está registrado. Por favor, use otro email.")
                except Exception as e:
                    st.error(f"Error al verificar el email: {e}")

            if not es_codigo_postal_valido(codigo_postal):
                errores.append("❗ Código postal inválido (mínimo 4 dígitos numéricos).")
            if password != confirmar_password:
                errores.append("❗ Las contraseñas no coinciden.")
            if len(password) < 3:
                errores.append("❗ La contraseña debe tener al menos 3 caracteres.")
        
        if not mayor_edad:
            errores.append("❗ Debes ser mayor de edad para registrarte.")

        if errores:
            for e in errores:
                st.error(e)
        else:
            # Intentar insertar en la base de datos
            if insertar_cliente(nombre, email, direccion, codigo_postal, password):
                st.success("✅ Cuenta creada exitosamente!")
                # Redirigir a inicio
                st.switch_page("Inicio.py")
            else:
                st.error("❌ Error al crear la cuenta. Por favor, intente nuevamente.")

# PIE DEL FORMULARIO
st.markdown("<hr style='border: 1px solid #2B3674; margin: 1.5rem 0;'>", unsafe_allow_html=True)

# Agregar botón de inicio de sesión
st.markdown("""
<div style='text-align: center; color: #707EAE; margin-top: 1rem; font-family: Inter, sans-serif;'>
    <p style='font-size: 0.9rem;'>Al crear una cuenta, aceptas nuestros términos de servicio y política de privacidad.</p>
</div>
""", unsafe_allow_html=True)

# Botón de inicio de sesión usando Streamlit
if st.button("¿Ya tienes cuenta? Inicia sesión aquí", key="login_button"):
    st.switch_page("Inicio.py")