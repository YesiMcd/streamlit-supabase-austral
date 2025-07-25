import streamlit as st
from conexion import get_supabase_client
from datetime import datetime
import os
import time
from PIL import Image
import base64
from io import BytesIO
from utils.sidebar_config import configure_sidebar

# --- Función para convertir imagen a base64 ---
def image_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()

# Configuración de página
st.set_page_config(
    page_title="Buscador de Productos",
    page_icon="��",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar sidebar
configure_sidebar()

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
                # Multiplicar el precio por la cantidad de unidades
                total += precio * producto['cantidad']
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

# Botón de volver después del título
if st.button("← Volver", key="back_button", help="Volver a la página anterior"):
    st.switch_page("pages/Tu Super online.py")

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
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h3 style="text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">📋 Seleccionar Productos</h3>', unsafe_allow_html=True)
    
    # Mensaje informativo sobre el orden de selección
    st.info("💡 **Recuerda:** Primero selecciona la cantidad de unidades y luego marca el checkbox para agregar al carrito.")
    
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
    
    # Mostrar productos con checkboxes y selector de cantidad
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
        
        # Crear un contenedor para cada producto
        with st.container():
            col_prod, col_cant = st.columns([4, 1])
            
            with col_prod:
                if st.checkbox(
                    f"**{nombre_display}** - {marca_display}", 
                    value=producto_en_carrito,
                    key=key
                ):
                    if not producto_en_carrito:
                        cantidad = st.session_state.get(f"cantidad_{i}", 1)
                        st.session_state.carrito.append({
                            'nombre': producto['nombre'],
                            'marca': producto['marca'],
                            'cantidad': cantidad
                        })
                else:
                    if producto_en_carrito:
                        st.session_state.carrito = [
                            p for p in st.session_state.carrito 
                            if not (p['nombre'] == producto['nombre'] and p['marca'] == producto['marca'])
                        ]
            
            with col_cant:
                # Selector de cantidad más compacto
                st.number_input(
                    "Cant.",
                    min_value=1,
                    max_value=10,
                    value=1,
                    key=f"cantidad_{i}",
                    label_visibility="collapsed"
                )

with col2:
    st.markdown('<h3 style="text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">🛒 Mi Carrito</h3>', unsafe_allow_html=True)
    
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío\n\nSelecciona productos de la izquierda")
    else:
        for producto in st.session_state.carrito:
            # Obtener la cantidad actual del producto
            cantidad = producto.get('cantidad', 1)
            st.markdown(f"""
            <div class="cart-item">
                <strong>{producto['nombre']}</strong><br>
                <small style="color: #666;">{producto['marca']}</small><br>
                <small style="color: #666;">Cantidad: {cantidad}</small>
            </div>
            """, unsafe_allow_html=True)
        
        total_productos = sum(p['cantidad'] for p in st.session_state.carrito)
        st.markdown(f"**Total de productos:** {total_productos}")
        
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
    col_limpiar, col_guardar = st.columns(2)
    
    with col_limpiar:
        if st.button("🗑️ Vaciar Carrito", use_container_width=True):
            st.session_state.carrito = []
            st.session_state["mostrar_resultados"] = False
            st.rerun()
    
    with col_guardar:
        if st.button("💾 Guardar Carrito", use_container_width=True):
            # Guardar el carrito en la base de datos
            if guardar_carrito_actual():
                st.success("✅ Carrito guardado exitosamente")
                st.switch_page("pages/Tu Super online.py")
            else:
                st.error("❌ Error al guardar el carrito")

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
        background-color: #5b7d9e !important;
    }
    [data-testid="stSidebar"] .sidebar-content {
        background-color: #5b7d9e !important;
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