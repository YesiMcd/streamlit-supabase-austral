import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import os
from conexion import get_supabase_client
from datetime import datetime
import time

# --- Configuración de la página ---
st.set_page_config(
    page_title="Forma de Pago",
    page_icon="💳",
    layout="centered"
)

# Inicializar cliente de Supabase
supabase = get_supabase_client()

def guardar_carrito_actual():
    """Guarda el carrito actual de la sesión como un carrito guardado"""
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
            st.error("No hay productos en el carrito actual")
            return False

        # Obtener datos adicionales de cada producto
        carrito_completo = []
        total = 0
        for item in carrito:
            # Obtener datos del producto
            response = supabase.table("Productos").select("id_productos, precio").eq("nombre_producto", item['nombre']).eq("marca", item['marca']).execute()
            
            if response.data and len(response.data) > 0:
                datos_producto = response.data[0]
                item_completo = {
                    'id_producto': datos_producto['id_productos'],
                    'nombre': item['nombre'],
                    'marca': item['marca'],
                    'precio': float(datos_producto['precio']),
                    'cantidad': item.get('cantidad', 1)
                }
                carrito_completo.append(item_completo)
                total += item_completo['precio'] * item_completo['cantidad']
            else:
                st.error(f"No se encontraron datos para el producto: {item['nombre']} - {item['marca']}")
                return False

        # Obtener el siguiente ID de carrito
        response = supabase.table("Carrito").select("id_carrito").order("id_carrito", desc=True).limit(1).execute()
        if response.data and len(response.data) > 0:
            id_carrito = int(response.data[0]['id_carrito']) + 1
        else:
            id_carrito = 1

        # Insertar en la tabla Carrito
        carrito_data = {
            'id_carrito': id_carrito,
            'id_cliente': id_cliente,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total': float(total),
            'estado': 'guardado'
        }
        
        response = supabase.table("Carrito").insert(carrito_data).execute()
        if not response.data:
            st.error("Error al guardar el carrito")
            return False

        # Insertar los detalles del carrito
        for item in carrito_completo:
            id_detalle = int(time.time() * 1000) + carrito_completo.index(item)
            
            detalle_data = {
                'id_detcarrito': id_detalle,
                'id_carrito': id_carrito,
                'id_producto': int(item['id_producto']),
                'unidades': int(item['cantidad']),
                'precio /u': float(item['precio'])
            }
            
            try:
                response = supabase.table("Det Carrito").insert(detalle_data).execute()
                if not response.data:
                    st.error(f"Error al guardar el detalle del producto {item['nombre']}")
                    return False
            except Exception as e:
                st.error(f"Error al guardar el detalle del producto {item['nombre']}: {str(e)}")
                return False

        return True

    except Exception as e:
        st.error(f"Error al guardar el carrito: {str(e)}")
        return False

# --- Función para convertir imagen a base64 ---
def image_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

# --- Cargar imagen y convertir a base64 ---
logo_b64 = None
try:
    # Intentar cargar la imagen desde la raíz del proyecto
    logo_path = "fondo del titulo.jpg"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        logo_b64 = image_to_base64(logo_img)
    else:
        # Si no se encuentra la imagen, usar un color de fondo sólido
        st.markdown("""
            <div style="
                background-color: #2B3674;
                width: 100%;
                height: 100px;
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                margin-bottom: 20px;
            ">
                <h1 style='
                    font-size: 2.5rem;
                    color: white;
                    margin: 0;
                    text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
                '>💰 Forma de Pago</h1>
            </div>
        """, unsafe_allow_html=True)
except Exception as e:
    # Si hay algún error, usar un color de fondo sólido
    st.markdown("""
        <div style="
            background-color: #2B3674;
            width: 100%;
            height: 100px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            margin-bottom: 20px;
        ">
            <h1 style='
                font-size: 2.5rem;
                color: white;
                margin: 0;
                text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
            '>💰 Forma de Pago</h1>
        </div>
    """, unsafe_allow_html=True)

# --- Estilos globales ---
st.markdown("""
    <style>
    html, body, .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #D4DFF0 !important;
        font-family: 'Inter', sans-serif !important;
        color: #2B3674 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .block-container {
        max-width: 700px !important;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        margin: auto !important;
        background-color: #D4DFF0 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #2C3E50 !important;
    }
    [data-testid="stSidebar"] .sidebar-content {
        background-color: #2C3E50 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
        font-family: 'Poppins', sans-serif !important;
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

    h1, h2, h3, h4 {
        color: #2B3674 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stButton > button {
        background-color: #2B3674 !important;
        color: white !important;
        padding: 14px 30px !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
        width: 100% !important;
        margin: 10px 0 !important;
    }

    .stButton > button:hover {
        background-color: #1A2156 !important;
        box-shadow: 0 6px 18px rgba(26, 33, 86, 0.35) !important;
        transform: translateY(-2px) !important;
    }

    div.stButton {
        text-align: center !important;
        padding: 10px !important;
    }

    /* Separador decorativo */
    .linea-separadora {
        border-top: 1.5px solid #A8B8D8;
        margin: 30px auto 20px auto;
        width: 80%;
    }

    /* Ocultar/cambiar color del header y toolbar */
    header[data-testid="stHeader"] {
        background-color: #D4DFF0 !important;
        height: 0px !important;
    }
    
    .stToolbar {
        background-color: #D4DFF0 !important;
    }
    
    [data-testid="stToolbar"] {
        background-color: #D4DFF0 !important;
    }
    
    /* Remover cualquier cuadro blanco en la parte superior */
    .stApp > div:first-child,
    .stApp > header,
    .stApp > div[data-testid="stHeader"] {
        background-color: #D4DFF0 !important;
    }
    
    /* Si hay un elemento con clase específica que cause el cuadro blanco */
    div[data-testid="stVerticalBlock"] > div:first-child {
        background-color: #D4DFF0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Banner con título centrado ---
if logo_b64:
    st.markdown(f"""
        <div style="
            background-image: url('data:image/jpeg;base64,{logo_b64}');
            background-size: cover;
            background-position: center;
            width: 100%;
            height: 100px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            margin-bottom: 20px;
        ">
            <h1 style='
                font-size: 2.5rem;
                color: white;
                margin: 0;
                text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
            '>💰 Forma de Pago</h1>
        </div>
    """, unsafe_allow_html=True)

# --- Frase debajo del título ---
st.markdown("### Selecciona tu método de pago preferido")
st.markdown("<br>", unsafe_allow_html=True)

# --- Mostrar resumen de la compra ---
if st.session_state.get("compra_confirmada"):
    st.markdown("### 📋 Resumen de tu compra")
    st.info(f"""
    **🏬 Supermercado:** {st.session_state.get('supermercado_seleccionado')}  
    **💰 Total:** ${st.session_state.get('total_compra', 0):.2f}  
    **📦 Productos:** {len(st.session_state.get('productos_compra', []))} items
    """)
    
    # Botón para guardar carrito antes de pagar
    if st.button("💾 Guardar Carrito Antes de Pagar", use_container_width=True):
        if guardar_carrito_actual():
            st.success("✅ Carrito guardado exitosamente")
            st.switch_page("pages/Tu Super online.py")
        else:
            st.error("❌ Error al guardar el carrito")

# --- Botones ---
if st.button("💵 Efectivo", use_container_width=True):
    st.session_state["metodo_pago"] = "efectivo"
    st.switch_page("pages/Pago en efectivo.py")

if st.button("💳 Tarjeta", use_container_width=True):
    st.session_state["metodo_pago"] = "tarjeta"
    st.switch_page("pages/Datos de la tarjeta.py")

# --- Separador decorativo ---
st.markdown('<div class="linea-separadora"></div>', unsafe_allow_html=True)

# --- Botón Volver ---
if st.button("← Volver", use_container_width=True):
    st.switch_page("pages/Buscador de productos.py")