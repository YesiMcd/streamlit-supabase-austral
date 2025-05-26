import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Configuración
st.set_page_config(page_title="SuperListo", layout="wide")

# CSS
st.markdown("""
    <style>
    .block-container {
        padding-top: 2.5rem !important;
    }
    .main {
        background-color:rgb(193, 208, 209);
    }
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

    /* Flexbox para alinear imagen + texto en la misma línea sin separación */
    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 1rem;
        padding: 10px 20px;
        border-radius: 12px;
        background-image: url("data:image/png;base64,{titulo_bg_b64}");
        background-size: cover;
        background-position: center;
        box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
    }
    .header-container img {
        width: 80px;
        height: auto;
    }
    .header-container h3 {
        margin: 0;
        padding: 0;
        font-size: 34px;
        font-weight: 400;
        color:rgb(25, 81, 145);
        font-family: 'Nunito', 'Arial', sans-serif;
        letter-spacing: -0.5px;
    }

    /* Estilos base para ambas columnas */
    div[data-testid="column"] {{
        padding: 0 !important;
        margin: 0 !important;
        width: 50% !important;
    }}

    /* Primera columna */
    div[data-testid="column"]:nth-of-type(1) > div {{
        padding: 0 !important;
        margin: 0 !important;
        height: 600px !important;
    }}

    .left-column {{
        position: relative;
        height: 600px !important;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(44, 62, 80, 0.15);
        background-image: url("data:image/png;base64,{img_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        justify-content: flex-start;
        padding-top: 60px;
    }}

    /* Segunda columna */
    div[data-testid="column"]:nth-of-type(2) > div {{
        background: #FF4359 !important;
        background: linear-gradient(171deg, rgba(255, 67, 89, 1) 27%, rgba(0, 236, 194, 1) 96%) !important;
        border-radius: 20px !important;
        padding: 40px !important;
        height: 650px !important;
        box-shadow: 0 4px 40px rgba(44, 62, 80, 0.15) !important;
        position: relative !important;
        margin: 0 !important;
    }}

    /* Asegurar que el contenedor del login tenga la misma altura */
    .login-container {
        height: 100% !important;
    }

    .login-form-container {
        background: rgba(128, 128, 128, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        height: calc(100% - 40px) !important;
        box-shadow: 0 8px 32px rgba(97, 93, 93, 0.1);
        margin-top: 0 !important;
    }

    .login-title {
        color: white !important;
        font-size: 48px !important;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 500 !important;
        text-align: center !important;
        margin-top: 0 !important;
        margin-bottom: 30px !important;
        text-shadow: 2px 2px 4px rgba(104, 99, 99, 0.3) !important;
    }

    .register-text {
        color: #00ecc2 !important;
        font-size: 24px !important;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 600 !important;
        margin-bottom: 0 !important;
        text-shadow: 1px 1px 2px rgba(0, 236, 194, 0.2) !important;
        text-align: right !important;
    }

    .custom-button {
        background-color: #00ecc2 !important;
        color: white !important;
        padding: 12px 25px !important;
        border-radius: 25px !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
        transition: all 0.3s ease !important;
        display: inline-block !important;
        box-shadow: 0 4px 15px rgba(0, 236, 194, 0.3) !important;
        margin: 0 !important;
        align-self: flex-end !important;
    }

    .custom-button:hover {
        background-color: #00d4b0 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 236, 194, 0.4) !important;
    }

    .content-overlay {
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-end !important;
        gap: 10px !important;
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# Convertir logo a base64 para insertarlo en HTML
def image_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# Cargar el logo y la imagen de fondo
logo = Image.open("logo_carrito.png")
logo_b64 = image_to_base64(logo)

# Cargar y convertir la imagen de fondo del título
titulo_bg = Image.open("fondo del titulo.jpg")
titulo_bg_b64 = image_to_base64(titulo_bg)

# Mostrar logo + título en una misma línea
st.markdown(f"""
    <style>
    .header-container {{
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 1rem;
        padding: 10px 20px;
        border-radius: 12px;
        background-image: url("data:image/png;base64,{titulo_bg_b64}");
        background-size: cover;
        background-position: center;
        box-shadow: 0 2px 8px rgba(44, 62, 80, 0.08);
    }}
    .header-container img {{
        width: 80px;
        height: auto;
    }}
    .header-container h3 {{
        margin: 0;
        padding: 0;
        font-size: 34px;
        font-weight: 600;
        color:rgb(18, 68, 124);
        font-family: 'Nunito', 'Arial', sans-serif;
        letter-spacing: -0.5px;
    }}
    </style>

    <div class="header-container">
        <img src="data:image/png;base64,{logo_b64}">
        <h3>SuperListo</h3>
    </div>
""", unsafe_allow_html=True)

###columnas
import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Cargar imagen de la col izq y pasar a base64
login_image = Image.open("imagen_login3.jpg")
buffered = BytesIO()
login_image.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue()).decode()

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <style>
    .left-column {{
        position: relative;
        height: 650px !important;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 4px 40px rgba(44, 62, 80, 0.15);
        background-image: url("data:image/png;base64,{img_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        justify-content: flex-start;
        padding-top: 80px;
    }}


    </style>

    <div class="left-column">
        <div class="content-overlay">
            <p class="register-text">Todavía no tenes cuenta?</p>
            <a href="https://tu-otra-pagina.com" class="custom-button">Sign Up</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

###
import streamlit as st
import base64

# Cargar imagen de fondo como base64
with open("gradiente2.jpg", "rb") as image_file:
    bg_bytes = image_file.read()
    bg_base64 = base64.b64encode(bg_bytes).decode("utf-8")

# CSS con múltiples selectores para asegurar que funcione
st.markdown(f"""
    <style>
    /* Múltiples selectores para la segunda columna */
    div[data-testid="column"]:nth-of-type(2),
    div[data-testid="column"]:nth-child(2),
    .stColumn:nth-of-type(2) > div,
    [data-testid="column"]:last-child {{
        background-image: url("data:image/png;base64,{bg_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        border-radius: 20px !important;
        padding: 40px 30px !important;
        min-height: 600px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        position: relative !important;
        margin: 0px 10px !important;
    }}
    
    /* Forzar el fondo con una clase personalizada también */
    .login-bg-container {{
        background-image: url("data:image/png;base64,{bg_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        border-radius: 20px !important;
        padding: 40px 30px !important;
        min-height: 600px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        position: relative !important;
        margin: 20px 10px !important;
    }}
    
    /* Asegurar que todo el contenido esté sobre el fondo */
    div[data-testid="column"]:nth-of-type(2) > div,
    .login-bg-container > div {{
        position: relative !important;
        z-index: 10 !important;
    }}

    /* Título */
    .login-title {{
        color: white !important;
        font-size: 48px !important;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 500 !important;
        text-align: center !important;
        margin-bottom: 1px !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
    }}

    /* Inputs - múltiples selectores */
    div[data-testid="column"]:nth-of-type(2) .stTextInput > div > div > input,
    .login-bg-container .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #1A4B8C !important;
        padding: 15px !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        margin-bottom: 10px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }}

    /* Botón - múltiples selectores */
    div[data-testid="column"]:nth-of-type(2) .stButton > button,
    .login-bg-container .stButton > button {{
        background-color: white !important;
        color: #1A4B8C !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        font-size: 18px !important;
        width: 100% !important;
        margin-top: 20px !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }}

    /* Checkbox - múltiples selectores */
    div[data-testid="column"]:nth-of-type(2) .stCheckbox > label,
    .login-bg-container .stCheckbox > label {{
        color: white !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }}
    
    div[data-testid="column"]:nth-of-type(2) .stCheckbox > label > span,
    .login-bg-container .stCheckbox > label > span {{
        color: white !important;
    }}

    /* Elementos personalizados */
    .forgot-password {{
        color: white !important;
        font-size: 14px !important;
        text-align: right !important;
        margin: 15px 0 !important;
    }}
    
    .forgot-password a {{
        color: white !important;
        text-decoration: underline !important;
    }}

    .social-buttons {{
        display: flex !important;
        gap: 15px !important;
        justify-content: center !important;
        margin-top: 30px !important;
    }}
    
    .social-btn {{
        background-color: white !important;
        color: #1A4B8C !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        cursor: pointer !important;
        box-shadow: 0 4px 12px rgba(128, 118, 118, 0.2) !important;
        font-size: 14px !important;
    }}

    /* Checkbox y su contenedor */
    .login-form-container .stCheckbox {{
        display: flex !important;
        align-items: center !important;
        margin: 10px 0 !important;
    }}

    .login-form-container .stCheckbox input[type="checkbox"] {{
        width: 18px !important;
        height: 18px !important;
        margin-right: 8px !important;
        accent-color: #0078ff !important;
        cursor: pointer !important;
    }}

    .login-form-container .stCheckbox label {{
        color: white !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        user-select: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Contenido del login SIN div contenedor adicional
with col2:
    st.markdown(f"""
    <div class="login-container">
        <div class="login-form-container">
            <h1 class="login-title">Welcome Back!</h1>
            <form id="loginForm" onsubmit="return validateForm(event)">
                <div class="stTextInput">
                    <input type="text" id="email" placeholder="Email" />
                </div>
                <div class="stTextInput">
                    <input type="password" id="password" placeholder="Password" />
                </div>
                <div id="error-message" class="error-message"></div>
                <div class="stCheckbox">
                    <input type="checkbox" id="remember" />
                    <label for="remember">Remember me</label>
                </div>
                <div class="forgot-password">
                    <a href="#">Forgot your password?</a>
                </div>
                <button type="submit" class="login-button">SIGN IN</button>
                <div class="social-buttons">
                    <button type="button" class="social-btn">
                        <svg class="social-icon" viewBox="0 0 24 24" width="18" height="18">
                            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                        </svg>
                        Google
                    </button>
                    <button type="button" class="social-btn">
                        <svg class="social-icon" viewBox="0 0 24 24" width="18" height="18">
                            <path fill="#1877F2" d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                        </svg>
                        Facebook
                    </button>
                </div>
            </form>
        </div>
    </div>

    <script>
    function validateForm(event) {{
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const errorMessage = document.getElementById('error-message');
        
        if (!email || !password) {{
            errorMessage.textContent = 'Please fill in all fields';
            errorMessage.style.display = 'block';
            return false;
        }}
        
        errorMessage.style.display = 'none';
        return true;
    }}
    </script>

    <style>
    .error-message {{
        color: #ff4359 !important;
        font-size: 14px !important;
        margin: 10px 0 !important;
        text-align: center !important;
        font-weight: 500 !important;
        display: none;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Agregar los estilos necesarios
    st.markdown("""
    <style>
    .login-container {
        padding: 20px;
        width: 100%;
    }

    .login-form-container {
        background: rgba(128, 128, 128, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        height: calc(100% - 40px) !important;
        box-shadow: 0 8px 32px rgba(97, 93, 93, 0.1);
        margin-top: 0 !important;
    }

    .login-title {
        color: white !important;
        font-size: 48px !important;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 500 !important;
        text-align: center !important;
        margin-top: 0 !important;
        margin-bottom: 30px !important;
        text-shadow: 2px 2px 4px rgba(104, 99, 99, 0.3) !important;
    }

    .login-form-container .stTextInput input {
        background-color: rgba(226, 231, 228, 0.92) !important;
        color: rgba(49, 48, 48, 0.99) !important;
        padding: 15px !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        border: 2px solid rgb(128, 128, 128) !important;
        margin-bottom: 10px !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(166, 172, 168, 0.75) !important;
        transition: all 0.3s ease !important;
    }

    /* Estado cuando el campo está seleccionado */
    .login-form-container .stTextInput input:focus {
        border-color: #0078ff !important;
        box-shadow: 0 0 0 2px rgba(0, 120, 255, 0.2) !important;
        outline: none !important;
    }

    /* Estado de validación correcta */
    .login-form-container .stTextInput input.valid {
        border-color: #00c853 !important;
        box-shadow: 0 0 0 2px rgba(0, 200, 83, 0.2) !important;
    }

    /* Estado de validación incorrecta */
    .login-form-container .stTextInput input.invalid {
        border-color: #ff3d00 !important;
        box-shadow: 0 0 0 2px rgba(255, 61, 0, 0.2) !important;
    }

    .login-button {
        background-color: white !important;
        color: #1A4B8C !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        font-size: 18px !important;
        width: 100% !important;
        margin-top: 20px !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(139, 134, 134, 0.2) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        cursor: pointer !important;
    }

    .login-form-container .stCheckbox label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }

    .login-form-container .forgot-password {
        color: white !important;
        font-size: 14px !important;
        text-align: right !important;
        margin: 15px 0 !important;
    }

    .login-form-container .forgot-password a {
        color: white !important;
        text-decoration: underline !important;
    }

    .login-form-container .social-buttons {
        display: flex !important;
        gap: 15px !important;
        justify-content: center !important;
        margin-top: 30px !important;
    }

    .login-form-container .social-btn {
        background-color: white !important;
        color:rgb(212, 36, 66) !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        cursor: pointer !important;
        box-shadow: 0 4px 12px rgba(121, 74, 74, 0.2) !important;
        font-size: 14px !important;
    }

    .social-icon {
        margin-right: 8px;
        vertical-align: middle;
    }

    .social-btn {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background-color: white !important;
        color: #1A4B8C !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        cursor: pointer !important;
        box-shadow: 0 4px 12px rgba(128, 118, 118, 0.2) !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }

    .social-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(128, 118, 118, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)