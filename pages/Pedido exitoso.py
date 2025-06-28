import streamlit as st
from conexion import get_supabase_client
from datetime import datetime
import time
import os

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

        # Verificar si es un carrito guardado que se está comprando
        carrito_original_id = st.session_state.get('carrito_original_id')
        
        if carrito_original_id:
            # Es un carrito guardado - actualizar el estado a "comprado"
            try:
                response = supabase.table("Carrito").update({
                    'estado': 'comprado'
                }).eq('id_carrito', carrito_original_id).execute()
                
                if response.data:
                    st.success("✅ Carrito guardado actualizado a comprado")
                    # Limpiar el carrito de la sesión
                    st.session_state['carrito'] = []
                    st.session_state.pop('carrito_original_id', None)
                    return True
                else:
                    st.error("Error al actualizar el carrito guardado")
                    return False
            except Exception as e:
                st.error(f"Error al actualizar el carrito guardado: {str(e)}")
                return False
        else:
            # Es un carrito nuevo - crear uno nuevo con estado "comprado"
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
                        'cantidad': item.get('cantidad', 1)  # Usar la cantidad real del carrito
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
                'total': float(total),
                'estado': 'comprado'
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

def configure_sidebar():
    """Configura el sidebar para mostrar solo las páginas principales."""
    
    # Aplicar CSS para ocultar todas las páginas excepto las principales
    st.markdown("""
        <style>
            /* Ocultar todas las páginas por defecto */
            div[data-testid="stSidebarNav"] ul {
                display: none !important;
            }
            
            /* Mostrar solo las páginas permitidas */
            div[data-testid="stSidebarNav"] ul li:nth-child(1), /* Inicio */
            div[data-testid="stSidebarNav"] ul li:nth-child(2), /* Registro */
            div[data-testid="stSidebarNav"] ul li:nth-child(3) { /* Tu Super online */
                display: block !important;
            }
            
            /* Ocultar específicamente las páginas no deseadas */
            div[data-testid="stSidebarNav"] ul li:nth-child(n+4) {
                display: none !important;
            }
            
            /* Estilo del sidebar - fondo completo */
            div[data-testid="stSidebar"] {
                background-color: #5b7d9e !important;
            }
            
            div[data-testid="stSidebar"] > div {
                background-color: #5b7d9e !important;
            }
            
            div[data-testid="stSidebar"] .sidebar-content {
                background-color: #5b7d9e !important;
            }
            
            section[data-testid="stSidebar"] {
                background-color: #5b7d9e !important;
            }
            
            section[data-testid="stSidebar"] > div {
                background-color: #5b7d9e !important;
            }
            
            /* Estilo del título de navegación - posicionado más arriba */
            div[data-testid="stSidebar"] h1 {
                margin-top: -10px !important;
                padding-top: 15px !important;
                color: white !important;
                font-family: 'Poppins', sans-serif !important;
            }
            
            div[data-testid="stSidebar"] * {
                color: white !important;
                font-family: 'Poppins', sans-serif !important;
            }
            
            /* Estilo de los botones del sidebar - IMPORTANTE: asegurar que sean visibles */
            div[data-testid="stSidebar"] .stButton {
                display: block !important;
                visibility: visible !important;
            }
            
            div[data-testid="stSidebar"] .stButton > button {
                background-color: #4b6783 !important;
                color: white !important;
                font-size: 16px !important;
                font-weight: 600 !important;
                padding: 12px 20px !important;
                margin: 8px 0 !important;
                border-radius: 10px !important;
                transition: all 0.3s ease !important;
                width: 100% !important;
                border: none !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
                display: block !important;
                visibility: visible !important;
            }
            
            div[data-testid="stSidebar"] .stButton > button:hover {
                background-color: #3a5570 !important;
                transform: translateX(5px) !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }
            
            /* Asegurar que el contenedor del sidebar sea visible */
            div[data-testid="stSidebar"] .element-container {
                display: block !important;
                visibility: visible !important;
            }
            
            /* Estilo para los enlaces de navegación */
            div[data-testid="stSidebarNav"] ul li a {
                font-size: 18px !important;
                font-weight: 600 !important;
                padding: 12px 20px !important;
                margin: 8px 0 !important;
                border-radius: 10px !important;
                transition: all 0.3s ease !important;
                display: block !important;
                text-decoration: none !important;
            }
            div[data-testid="stSidebarNav"] ul li a:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
                transform: translateX(5px) !important;
            }
            div[data-testid="stSidebarNav"] ul li a.active {
                background-color: rgba(255, 255, 255, 0.2) !important;
                font-weight: 700 !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Configurar el sidebar
    with st.sidebar:
        st.title("Navegación")
        

        
        # Obtener páginas disponibles en la carpeta pages
        pages_dir = "pages"
        allowed_pages = ["Tu Super online"]  # Páginas permitidas sin incluir Inicio
        
        if os.path.exists(pages_dir):
            for page_name in allowed_pages:  # Usar orden específico
                file_path = f"{pages_dir}/{page_name}.py"
                if os.path.exists(file_path):
                    # Agregar iconos para hacer más visual
                    icon = "🛒"
                    if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
                        st.switch_page(f"pages/{page_name}.py")
        
        # Agregar botón para Cerrar sesión al final
        if st.button("🚪 Cerrar sesión", key="nav_cerrar_sesion", use_container_width=True):
            # Limpiar la sesión
            st.session_state.clear()
            st.switch_page("Inicio.py")

# EJECUTAR LA CONFIGURACIÓN DEL SIDEBAR
configure_sidebar()

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

# ESTILOS CSS GLOBALES PARA FORZAR EL COLOR BLANCO DEL TÍTULO
st.markdown("""
    <style>
    /* ESTILOS NUCLEARES PARA EL SIDEBAR */
    [data-testid="stSidebar"] div span {
        color: white !important;
    }
    
    [data-testid="stSidebar"] div div span {
        color: white !important;
    }
    
    [data-testid="stSidebar"] * span {
        color: white !important;
    }
    
    /* Forzar color blanco en cualquier elemento del sidebar */
    [data-testid="stSidebar"] div[style*="font-size: 1.5rem"] span {
        color: white !important;
        background-color: transparent !important;
    }
    
    /* Sobrescribir cualquier color heredado */
    [data-testid="stSidebar"] span {
        color: white !important;
        color: white !important;
        color: white !important;
    }
    
    /* Forzar color blanco en el título h1 del sidebar */
    [data-testid="stSidebar"] h1 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .st-emotion-cache-n14c82 h1 {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Botón para volver al inicio
if st.button("Volver a Tu Super Online", use_container_width=True):
    st.switch_page("pages/Tu Super online.py")

