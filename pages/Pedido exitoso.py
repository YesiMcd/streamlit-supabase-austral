import streamlit as st
from conexion import get_supabase_client
from datetime import datetime
import time

# Configuración de la página
st.set_page_config(
    page_title="¡Pedido Exitoso!",
    page_icon="🛍️",
    layout="centered"
)

# Inicializar cliente de Supabase
supabase = get_supabase_client()

def obtener_datos_producto(nombre, marca):
    try:
        response = supabase.table("Productos").select("id_productos, precio").eq("nombre_producto", nombre).eq("marca", marca).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Error al obtener datos del producto: {str(e)}")
        return None

def obtener_siguiente_id_carrito():
    try:
        response = supabase.table("Carrito").select("id_carrito").order("id_carrito", desc=True).limit(1).execute()
        if response.data and len(response.data) > 0:
            return int(response.data[0]['id_carrito']) + 1
        return 1
    except Exception as e:
        st.error(f"Error al obtener el siguiente ID de carrito: {str(e)}")
        return None

def guardar_carrito():
    try:
        # Obtener el email del usuario de la sesión
        email = st.session_state.get('user_email')
        if not email:
            st.error("No se encontró la sesión del usuario")
            return False

        # Obtener el ID del cliente
        response = supabase.table("Cliente").select("id_cliente").eq("email", email).execute()
        if not response.data:
            st.error("No se encontró el cliente")
            return False
        
        id_cliente = response.data[0]['id_cliente']
        
        # Obtener los datos del carrito de la sesión
        carrito = st.session_state.get('carrito', [])
        if not carrito:
            st.error("No hay productos en el carrito")
            return False

        # Obtener datos adicionales de cada producto
        carrito_completo = []
        total = 0
        for item in carrito:
            datos_producto = obtener_datos_producto(item['nombre'], item['marca'])
            if datos_producto:
                item_completo = {
                    'id_producto': datos_producto['id_productos'],
                    'nombre': item['nombre'],
                    'marca': item['marca'],
                    'precio': float(datos_producto['precio']),
                    'cantidad': 1
                }
                carrito_completo.append(item_completo)
                total += item_completo['precio'] * item_completo['cantidad']
            else:
                st.error(f"No se encontraron datos para el producto: {item['nombre']} - {item['marca']}")
                return False

        # Obtener el siguiente ID de carrito
        id_carrito = obtener_siguiente_id_carrito()
        if id_carrito is None:
            st.error("No se pudo generar un ID para el carrito")
            return False

        # Insertar en la tabla Carrito
        carrito_data = {
            'id_carrito': id_carrito,
            'id_cliente': id_cliente,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total': float(total)
        }
        
        response = supabase.table("Carrito").insert(carrito_data).execute()
        if not response.data:
            st.error("Error al guardar el carrito")
            return False

        # Insertar los detalles del carrito
        detalles_guardados = []
        for item in carrito_completo:
            id_detalle = int(time.time() * 1000) + len(detalles_guardados)
            
            detalle_data = {
                'id_detcarrito': id_detalle,
                'id_carrito': id_carrito,
                'id_producto': int(item['id_producto']),
                'unidades': int(item['cantidad']),
                'precio /u': float(item['precio'])
            }
            
            try:
                response = supabase.table("Det Carrito").insert(detalle_data).execute()
                if response.data:
                    detalles_guardados.append(detalle_data)
                else:
                    st.error(f"Error al guardar el detalle del producto {item['nombre']}")
                    return False
            except Exception as e:
                st.error(f"Error al guardar el detalle del producto {item['nombre']}: {str(e)}")
                return False

        # Verificar que se guardaron todos los detalles
        if len(detalles_guardados) != len(carrito_completo):
            st.error("No se guardaron todos los detalles del carrito")
            return False

        # Limpiar el carrito de la sesión
        st.session_state['carrito'] = []
        return True

    except Exception as e:
        st.error(f"Error al guardar el carrito: {str(e)}")
        return False

# Guardar el carrito cuando se carga la página
if guardar_carrito():
    st.success("¡Tu pedido se ha guardado correctamente!")

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    .main {
        background: #D4DFF0 !important;
        min-height: 100vh;
    }
    
    .stApp {
        background: #D4DFF0 !important;
    }
    
    .block-container {
        background: #D4DFF0 !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #D4DFF0 !important;
    }
    
    [data-testid="stMain"] {
        background: #D4DFF0 !important;
    }
    
    [data-testid="stHeader"] {
        background: #D4DFF0 !important;
    }
    
    [data-testid="stToolbar"] {
        background: #D4DFF0 !important;
    }
    
    .main > div {
        background: #D4DFF0 !important;
    }
    
    .element-container {
        background: #D4DFF0 !important;
    }
    
    .stMarkdown {
        background: #D4DFF0 !important;
    }
    
    body {
        background: #D4DFF0 !important;
    }
    
    html {
        background: #D4DFF0 !important;
    }
    
    .success-container {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem auto;
        max-width: 500px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    
    .success-icon {
        font-size: 4rem;
        margin: 1rem 0;
        animation: bounce 2s infinite;
    }
    
    .success-title {
        color: #2B3674;
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .success-message {
        color: #707EAE;
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 1rem 0;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    .stButton > button {
        background-color: #2B3674 !important;
        color: white !important;
        padding: 0.8rem 2rem;
        border-radius: 10px;
        border: none;
        font-size: 1.1rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        margin-top: 1.5rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #1A2156 !important;
        box-shadow: 0 4px 12px rgba(43, 54, 116, 0.15);
        transform: translateY(-2px);
    }

    /* Animación para las frutas y verduras */
    .falling-items {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        opacity: 0.7;
    }

    .falling-item {
        position: absolute;
        font-size: 1.8rem;
        animation: fall 3s linear infinite;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }

    @keyframes fall {
        0% {
            transform: translateY(-100%) rotate(0deg);
            opacity: 0.8;
        }
        100% {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0.4;
        }
    }

    /* Fondo decorativo */
    .background-decoration {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #D4DFF0;
        z-index: -1;
    }

    .background-circles {
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }

    .circle {
        position: absolute;
        border-radius: 50%;
        background: linear-gradient(135deg, rgba(43, 54, 116, 0.1), rgba(43, 54, 116, 0.05));
    }

    .circle-1 {
        width: 300px;
        height: 300px;
        top: -100px;
        right: -100px;
    }

    .circle-2 {
        width: 200px;
        height: 200px;
        bottom: -50px;
        left: -50px;
    }
    </style>

    <div class="background-decoration">
        <div class="background-circles">
            <div class="circle circle-1"></div>
            <div class="circle circle-2"></div>
        </div>
    </div>

    <div class="falling-items">
        <div class="falling-item" style="left: 10%; animation-delay: 0s;">🍎</div>
        <div class="falling-item" style="left: 20%; animation-delay: 1s;">🥕</div>
        <div class="falling-item" style="left: 30%; animation-delay: 2s;">🍌</div>
        <div class="falling-item" style="left: 40%; animation-delay: 0.5s;">🥬</div>
        <div class="falling-item" style="left: 50%; animation-delay: 1.5s;">🍅</div>
        <div class="falling-item" style="left: 60%; animation-delay: 2.5s;">🥑</div>
        <div class="falling-item" style="left: 70%; animation-delay: 0.7s;">🥦</div>
        <div class="falling-item" style="left: 80%; animation-delay: 1.7s;">🍊</div>
    </div>

    <div class="success-container">
        <div class="success-icon">🛍️</div>
        <div class="success-title">¡Tu pedido se realizó con éxito!</div>
        <div class="success-message">
            Gracias por tu compra. Estamos preparando tu pedido con mucho cuidado.
        </div>
    </div>
""", unsafe_allow_html=True)

# Botón para volver al inicio
if st.button("Volver al Inicio", use_container_width=True):
    st.switch_page("Inicio.py")  # O usa "pages/Inicio.py" si está dentro de esa carpeta