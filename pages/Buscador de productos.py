import streamlit as st
from conexion import get_supabase_client
from datetime import datetime
import os
import time
from PIL import Image
import base64
from io import BytesIO

# --- Función para convertir imagen a base64 ---
def image_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

# Configuración de página
st.set_page_config(
    page_title="Buscador de Productos",
    page_icon="🛒",
    layout="wide"
)

# Inicializar cliente de Supabase
supabase = get_supabase_client()

# Estilo CSS
st.markdown("""
    <style>
    /* Color base de la página */
    #root {
        background-color: #D4DFF0 !important;
    }
    
    .stApp {
        background-color: #D4DFF0 !important;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"], .main {
        background-color: #D4DFF0 !important;
        font-family: 'Inter', sans-serif !important;
        color: #2B3674 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .block-container {
        max-width: 1200px !important;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        margin: 3rem !important;
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
        padding: 0 !important;
        margin: 0 !important;
    }
    
    .stToolbar {
        background-color: #D4DFF0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    [data-testid="stToolbar"] {
        background-color: #D4DFF0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Remover cualquier cuadro blanco en la parte superior */
    .stApp > div:first-child,
    .stApp > header,
    .stApp > div[data-testid="stHeader"] {
        background-color: #D4DFF0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Si hay un elemento con clase específica que cause el cuadro blanco */
    div[data-testid="stVerticalBlock"] > div:first-child {
        background-color: #D4DFF0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Ajustar el espacio del main container */
    .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
        background-color: #D4DFF0 !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #D4DFF0 !important;
    }

    /* Estilos para el campo de búsqueda */
    .stTextInput > div > div > input {
        background-color: white !important;
        border-radius: 10px !important;
        padding: 10px !important;
        font-size: 16px !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #666 !important;
    }

    /* Estilos para las tarjetas de productos */
    .product-card {
        background-color: white;
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .cart-item {
        background-color: #f0f8ff;
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        border-left: 4px solid #007BFF;
    }
    .best-price {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .price-comparison {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 5px 0;
    }

    /* Estilos para los títulos */
    h3 {
        text-align: center !important;
        color: #2B3674 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2) !important;
        margin-bottom: 1.5rem !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# Verificar sesión de usuario
if "user_email" not in st.session_state:
    st.error("🔐 Debes iniciar sesión para usar esta página.")
    st.stop()

usuario_email = st.session_state["user_email"]

# Funciones de base de datos
@st.cache_data
def obtener_codigo_postal_usuario(email):
    """Obtiene el código postal del usuario"""
    try:
        result = supabase.table("Cliente").select('"código postal"').eq("email", email).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]["código postal"]
        return None
    except Exception as e:
        st.error(f"Error al obtener código postal: {e}")
        return None

@st.cache_data
def obtener_todos_los_productos():
    """Obtiene todos los productos únicos disponibles"""
    try:
        result = supabase.table("Productos").select("nombre_producto, marca").execute()
        if result.data:
            productos_unicos = set()
            for producto in result.data:
                nombre = producto.get('nombre_producto', '').strip()
                marca = producto.get('marca', '').strip()
                if nombre and marca:
                    productos_unicos.add((nombre, marca))
            productos_lista = [{'nombre': nombre, 'marca': marca} for nombre, marca in productos_unicos]
            return sorted(productos_lista, key=lambda x: x['nombre'].lower())
        return []
    except Exception as e:
        st.error(f"Error al obtener productos: {e}")
        return []

@st.cache_data
def obtener_supermercados_zona(codigo_postal):
    """Obtiene supermercados en la zona del código postal"""
    try:
        result = supabase.table("Supermercados").select("id_supermercado, nombre").eq('"código postal"', codigo_postal).execute()
        if result.data:
            return result.data
        return []
    except Exception as e:
        st.error(f"Error al obtener supermercados: {e}")
        return []

@st.cache_data
def obtener_precio_producto_supermercado(nombre_producto, marca, id_supermercado):
    """Obtiene el precio de un producto específico en un supermercado específico"""
    try:
        result = supabase.table("Productos").select("precio").eq("nombre_producto", nombre_producto).eq("marca", marca).eq("id_supermercado", id_supermercado).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]["precio"]
        return None
    except Exception as e:
        st.error(f"Error al obtener precio: {e}")
        return None

def calcular_mejor_opcion(carrito, codigo_postal):
    """Calcula qué supermercado tiene el menor precio total para el carrito"""
    supermercados = obtener_supermercados_zona(codigo_postal)
    
    if not supermercados:
        return None, None
    
    resultados = []
    
    for supermercado in supermercados:
        id_super = supermercado['id_supermercado']
        nombre_super = supermercado['nombre']
        total = 0
        productos_disponibles = True
        
        for producto in carrito:
            precio = obtener_precio_producto_supermercado(
                producto['nombre'], 
                producto['marca'], 
                id_super
            )
            
            if precio is not None:
                total += precio
            else:
                productos_disponibles = False
                break
        
        if productos_disponibles:
            resultados.append({
                'id': id_super,
                'nombre': nombre_super,
                'total': total
            })
    
    if resultados:
        resultados.sort(key=lambda x: x['total'])
        return resultados, resultados[0]
    
    return None, None

# Inicializar carrito en session_state
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# --- Cargar imagen y convertir a base64 ---
logo_b64 = None
try:
    # Intentar cargar la imagen desde la raíz del proyecto
    logo_path = "fondo del titulo.jpg"
    if os.path.exists(logo_path):
        logo_img = Image.open(logo_path)
        logo_b64 = image_to_base64(logo_img)
    else:
        st.warning("No se encontró la imagen de fondo")
except Exception as e:
    st.warning(f"No se pudo cargar la imagen: {e}")

# INTERFAZ PRINCIPAL
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
            '>🛒 Buscador de Productos</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div style="
            background-color: #2B3674;
            width: 100%;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
        ">
            <h1 style='
                font-size: 1.5rem;
                color: white;
                margin: 0;
                text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
            '>🛒 Buscador de Productos</h1>
        </div>
    """, unsafe_allow_html=True)

st.markdown("**Encuentra el supermercado con menor precio total en tu zona**")

# Obtener código postal del usuario
codigo_postal = obtener_codigo_postal_usuario(usuario_email)
if not codigo_postal:
    st.error("⚠️ No se encontró tu código postal. Por favor, actualiza tu perfil.")
    st.stop()

st.info(f"📍 Buscando supermercados en tu zona: **{codigo_postal}**")

# Obtener productos disponibles
productos_disponibles = obtener_todos_los_productos()
if not productos_disponibles:
    st.error("❌ No se pudieron cargar los productos. Intenta nuevamente.")
    st.stop()

# Layout en columnas
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<h3 style="text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">📋 Seleccionar Productos</h3>', unsafe_allow_html=True)
    
    # Tipo de búsqueda
    tipo_busqueda = st.radio("Buscar por:", ["Producto", "Marca"], horizontal=True)
    
    # Inicializar busqueda
    busqueda = ""
    
    if tipo_busqueda == "Producto":
        # Buscador de productos
        busqueda = st.text_input("🔍 Buscar productos:", placeholder="Escribe el nombre del producto...", key="busqueda_input")
        
        # Filtrar productos según búsqueda
        if busqueda:
            busqueda = busqueda.lower().strip()
            productos_filtrados = []
            for p in productos_disponibles:
                nombre = p['nombre'].lower()
                if busqueda in nombre:
                    productos_filtrados.append(p)
            
            productos_filtrados.sort(key=lambda x: x['nombre'].lower())
        else:
            productos_filtrados = productos_disponibles[:20]
    else:
        # Obtener marcas únicas
        marcas = sorted(list(set(p['marca'] for p in productos_disponibles)))
        marca_seleccionada = st.selectbox("Selecciona una marca:", marcas)
        
        # Filtrar productos por marca
        productos_filtrados = [p for p in productos_disponibles if p['marca'] == marca_seleccionada]
    
    st.caption(f"Mostrando {len(productos_filtrados)} productos")
    
    # Mostrar productos con checkboxes
    for i, producto in enumerate(productos_filtrados):
        key = f"check_{producto['nombre']}_{producto['marca']}_{i}"
        
        producto_en_carrito = any(
            p['nombre'] == producto['nombre'] and p['marca'] == producto['marca'] 
            for p in st.session_state.carrito
        )
        
        nombre_display = producto['nombre']
        marca_display = producto['marca']
        if busqueda:
            nombre_display = nombre_display.replace(busqueda, f"**{busqueda}**")
            marca_display = marca_display.replace(busqueda, f"**{busqueda}**")
        
        if st.checkbox(
            f"**{nombre_display}** - {marca_display}", 
            value=producto_en_carrito,
            key=key
        ):
            if not producto_en_carrito:
                st.session_state.carrito.append(producto)
        else:
            if producto_en_carrito:
                st.session_state.carrito = [
                    p for p in st.session_state.carrito 
                    if not (p['nombre'] == producto['nombre'] and p['marca'] == producto['marca'])
                ]

with col2:
    st.markdown('<h3 style="text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">🛒 Mi Carrito</h3>', unsafe_allow_html=True)
    
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío\n\nSelecciona productos de la izquierda")
    else:
        for producto in st.session_state.carrito:
            st.markdown(f"""
            <div class="cart-item">
                <strong>{producto['nombre']}</strong><br>
                <small style="color: #666;">{producto['marca']}</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"**Total de productos:** {len(st.session_state.carrito)}")
        
        if st.button("💰 Calcular Mejor Precio", type="primary", use_container_width=True):
            with st.spinner("Calculando precios en todos los supermercados..."):
                todos_resultados, mejor_opcion = calcular_mejor_opcion(st.session_state.carrito, codigo_postal)
                
                if mejor_opcion:
                    st.success("✅ ¡Cálculo completado!")
                    
                    # Guardar datos para la compra
                    st.session_state["supermercado_seleccionado"] = mejor_opcion['nombre']
                    st.session_state["total_compra"] = mejor_opcion['total']
                    st.session_state["productos_compra"] = st.session_state.carrito.copy()
                    st.session_state["fecha_compra"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state["compra_confirmada"] = True
                    st.session_state["mostrar_resultados"] = True
                    
                    # Mostrar mejor opción destacada
                    st.markdown(f"""
                    <div class="best-price">
                        <h3>🏆 Mejor Opción</h3>
                        <h4>🏬 {mejor_opcion['nombre']}</h4>
                        <h2 style="color: #28a745;">Total: ${mejor_opcion['total']:.2f}</h2>
                        <p>¡El precio más bajo para tu carrito!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mostrar comparación con otros supermercados
                    if len(todos_resultados) > 1:
                        st.subheader("📊 Comparación de Precios")
                        for resultado in todos_resultados:
                            diferencia = resultado['total'] - mejor_opcion['total']
                            st.markdown(f"""
                            <div class="price-comparison">
                                <strong>🏬 {resultado['nombre']}</strong><br>
                                Total: <strong>${resultado['total']:.2f}</strong>
                                {f"<span style='color: #dc3545;'> (+${diferencia:.2f})</span>" if diferencia > 0 else ""}
                            </div>
                            """, unsafe_allow_html=True)
                
                else:
                    st.warning("😔 No hay supermercados en tu zona que tengan todos los productos seleccionados.")
                    st.info("Intenta con menos productos o productos diferentes.")
                    st.session_state["mostrar_resultados"] = False

# Mostrar botón de compra solo si hay resultados
if st.session_state.get("mostrar_resultados", False):
    if st.button("🛒 Realizar Compra", type="primary", use_container_width=True):
        st.switch_page("pages/Forma de Pago.py")

# Mostrar estado de compra confirmada si existe
if st.session_state.get("compra_confirmada"):
    st.markdown("---")
    st.markdown("### ✅ Compra Preparada")
    st.info(f"""
    **🏬 Supermercado:** {st.session_state.get('supermercado_seleccionado')}  
    **💰 Total:** ${st.session_state.get('total_compra', 0):.2f}  
    **📦 Productos:** {len(st.session_state.get('productos_compra', []))} items
    
    **📋 Puedes proceder al pago usando el menú lateral → 'Forma de Pago'**
    """)

# Limpiar carrito
if st.session_state.carrito:
    if st.button("🗑️ Vaciar Carrito", use_container_width=True):
        st.session_state.carrito = []
        st.session_state["mostrar_resultados"] = False
        st.rerun()

# Información adicional
with st.expander("ℹ️ Información"):
    st.markdown("""
    **¿Cómo funciona?**
    1. Selecciona los productos que quieras comprar
    2. Haz clic en "Calcular Mejor Precio"
    3. Te mostramos qué supermercado tiene el precio total más bajo
    4. Serás redirigido automáticamente a la página de pago
    
    **Nota:** Solo se muestran supermercados de tu zona que tengan todos los productos disponibles.
    """)