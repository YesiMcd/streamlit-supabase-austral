import streamlit as st
from conexion import get_supabase_client
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
import os

# Configuración de la página
st.set_page_config(
    page_title="Mi Perfil",
    page_icon="👤",
    layout="wide"
)

# Inicializar cliente de Supabase
supabase = get_supabase_client()

# Inicializar session_state si no existe
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

# --- Función para configurar el sidebar ---
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
        
        # Agregar botón para Inicio (página principal) - PRIMERO
        if st.button("🏠 Inicio", key="nav_inicio", use_container_width=True):
            st.switch_page("Inicio.py")
        
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

# --- Configurar el sidebar ---
configure_sidebar()

# CSS personalizado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    /* SIDEBAR STYLING */
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

    /* FONDO DE LA APP (header + body) */
    html, body, .stApp, #root, header, main, section {
        background-color: #D4DFF0 !important;
        font-family: 'Inter', sans-serif !important;
        color: #2B3674 !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .block-container {
        max-width: 1200px !important;
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

    /* Estilos para las tarjetas de carrito */
    .cart-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .cart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.3);
        padding-bottom: 10px;
    }
    .cart-product {
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 10px;
        margin: 8px 0;
        border-left: 4px solid #4CAF50;
    }
    .cart-total {
        text-align: right;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid rgba(255,255,255,0.3);
    }
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .status-guardado {
        background: #FFD700;
        color: #000;
    }
    .status-comprado {
        background: #4CAF50;
        color: white;
    }
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: #666;
    }
    .empty-state h3 {
        color: #333;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def agregar_columna_estado():
    """Agrega la columna Estado a la tabla Carrito si no existe"""
    try:
        # Verificar si la columna ya existe
        response = supabase.table("Carrito").select("estado").limit(1).execute()
        return True  # Si no hay error, la columna ya existe
    except:
        try:
            # Agregar la columna Estado con valor por defecto 'guardado'
            query = """
            ALTER TABLE "Carrito" 
            ADD COLUMN IF NOT EXISTS estado VARCHAR(20) DEFAULT 'guardado';
            """
            # Ejecutar la consulta usando psycopg2
            from functions import execute_query
            result = execute_query(query, is_select=False)
            if result:
                st.success("✅ Columna 'Estado' agregada exitosamente a la tabla Carrito")
                return True
            else:
                st.error("❌ Error al agregar la columna Estado")
                return False
        except Exception as e:
            st.error(f"❌ Error al agregar la columna Estado: {str(e)}")
            return False

def obtener_datos_usuario(email):
    """Obtiene los datos del usuario por email"""
    try:
        response = supabase.table("Cliente").select('*, "código postal"').eq("email", email).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Error al obtener datos del usuario: {e}")
        return None

def obtener_productos_frecuentes(id_cliente):
    """Obtiene los productos más frecuentes del usuario (solo de carritos comprados)"""
    try:
        # Obtener solo los carritos COMPRADOS del usuario
        response = supabase.table('Carrito').select('id_carrito').eq('id_cliente', id_cliente).eq('estado', 'comprado').execute()
        if not response.data:
            return []
        
        id_carritos = [carrito['id_carrito'] for carrito in response.data]
        
        # Obtener los detalles de los carritos comprados
        detalles = []
        for id_carrito in id_carritos:
            detalle_response = supabase.table('Det Carrito').select('id_producto, unidades').eq('id_carrito', id_carrito).execute()
            if detalle_response.data:
                detalles.extend(detalle_response.data)
        
        # Obtener información de los productos
        productos_frecuentes = {}
        for detalle in detalles:
            producto_response = supabase.table('Productos').select('nombre_producto, marca').eq('id_productos', detalle['id_producto']).execute()
            if producto_response.data:
                producto = producto_response.data[0]
                key = f"{producto['nombre_producto']} - {producto['marca']}"
                if key in productos_frecuentes:
                    productos_frecuentes[key] += detalle['unidades']
                else:
                    productos_frecuentes[key] = detalle['unidades']
        
        # Ordenar por frecuencia y obtener los 3 más frecuentes
        productos_ordenados = sorted(productos_frecuentes.items(), key=lambda x: x[1], reverse=True)[:3]
        return productos_ordenados
    except Exception as e:
        st.error(f"Error al obtener productos frecuentes: {e}")
        return []

def obtener_carritos_usuario():
    """Obtiene todos los carritos del usuario actual"""
    try:
        # Obtener el ID del cliente
        email = st.session_state.get('user_email')
        response = supabase.table("Cliente").select("id_cliente").eq("email", email).execute()
        if not response.data:
            return []
        
        id_cliente = response.data[0]['id_cliente']
        
        # Obtener carritos del usuario
        response = supabase.table("Carrito").select("*").eq("id_cliente", id_cliente).order("fecha", desc=True).execute()
        
        if not response.data:
            return []
        
        carritos_completos = []
        for carrito in response.data:
            # Obtener los detalles del carrito
            detalles_response = supabase.table("Det Carrito").select("*").eq("id_carrito", carrito['id_carrito']).execute()
            
            if detalles_response.data:
                # Obtener información de los productos
                productos = []
                for detalle in detalles_response.data:
                    producto_response = supabase.table("Productos").select("nombre_producto, marca").eq("id_productos", detalle['id_producto']).execute()
                    
                    if producto_response.data:
                        producto = producto_response.data[0]
                        productos.append({
                            'nombre': producto['nombre_producto'],
                            'marca': producto['marca'],
                            'cantidad': detalle['unidades'],
                            'precio': detalle['precio /u']
                        })
                
                carritos_completos.append({
                    'id_carrito': carrito['id_carrito'],
                    'fecha': carrito['fecha'],
                    'total': carrito['total'],
                    'estado': carrito.get('estado', 'guardado'),
                    'productos': productos
                })
        
        return carritos_completos
    except Exception as e:
        st.error(f"Error al obtener carritos: {str(e)}")
        return []

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

        st.success("✅ Carrito guardado exitosamente")
        return True

    except Exception as e:
        st.error(f"Error al guardar el carrito: {str(e)}")
        return False

def cargar_carrito_a_sesion(carrito_data):
    """Carga un carrito guardado a la sesión actual y prepara para la compra"""
    try:
        productos_carrito = []
        for producto in carrito_data['productos']:
            productos_carrito.append({
                'nombre': producto['nombre'],
                'marca': producto['marca'],
                'cantidad': producto['cantidad']
            })
        
        st.session_state['carrito'] = productos_carrito
        
        # Guardar información para la compra
        st.session_state["supermercado_seleccionado"] = "Supermercado seleccionado"  # Se puede mejorar obteniendo el supermercado real
        st.session_state["total_compra"] = carrito_data['total']
        st.session_state["productos_compra"] = productos_carrito.copy()
        st.session_state["fecha_compra"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["compra_confirmada"] = True
        st.session_state["mostrar_resultados"] = True
        
        # Guardar el ID del carrito original para actualizarlo después
        st.session_state["carrito_original_id"] = carrito_data['id_carrito']
        
        st.success("✅ Carrito cargado exitosamente")
        return True
    except Exception as e:
        st.error(f"Error al cargar el carrito: {str(e)}")
        return False

def eliminar_carrito(id_carrito):
    """Elimina un carrito y sus detalles"""
    try:
        # Eliminar detalles del carrito
        response = supabase.table("Det Carrito").delete().eq("id_carrito", id_carrito).execute()
        
        # Eliminar el carrito
        response = supabase.table("Carrito").delete().eq("id_carrito", id_carrito).execute()
        
        if response.data:
            st.success("✅ Carrito eliminado exitosamente")
            return True
        else:
            st.error("❌ Error al eliminar el carrito")
            return False
    except Exception as e:
        st.error(f"Error al eliminar el carrito: {str(e)}")
        return False

def actualizar_usuario(id_cliente, nombre, email, direccion, codigo_postal, password):
    """Actualiza los datos del usuario"""
    try:
        # Preparar datos para actualizar
        datos_actualizados = {
            'nombre': nombre,
            'email': email,
            'dirección': direccion,
            '"código postal"': codigo_postal
        }
        
        # Solo actualizar contraseña si se proporcionó una nueva
        if password and password.strip():
            datos_actualizados['Contraseña'] = password
        
        response = supabase.table("Cliente").update(datos_actualizados).eq("id_cliente", id_cliente).execute()
        
        if response.data:
            return True
        else:
            st.error("Error al actualizar los datos")
            return False
    except Exception as e:
        st.error(f"Error al actualizar usuario: {e}")
        return False

def recalcular_precios_carrito(carrito_data):
    """Recalcula los precios de un carrito guardado usando la misma lógica que Buscador de Productos"""
    try:
        # Obtener el código postal del usuario
        email = st.session_state.get('user_email')
        response = supabase.table("Cliente").select('"código postal"').eq("email", email).execute()
        if not response.data:
            st.error("No se pudo obtener el código postal del usuario")
            return False
        
        codigo_postal = response.data[0]['código postal']
        if not codigo_postal:
            st.error("No tienes un código postal configurado. Actualiza tu perfil.")
            return False
        
        # Obtener supermercados de la zona
        response = supabase.table("Supermercados").select("*").eq('"código postal"', codigo_postal).execute()
        if not response.data:
            st.error("No hay supermercados en tu zona")
            return False
        
        supermercados = response.data
        
        # Usar la misma lógica que Buscador de Productos
        resultados = []
        with st.spinner("Recalculando precios en todos los supermercados..."):
            for supermercado in supermercados:
                id_super = supermercado['id_supermercado']
                nombre_super = supermercado['nombre']
                total = 0
                productos_disponibles = True
                
                for producto in carrito_data['productos']:
                    # Usar la misma función que Buscador de Productos
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
        
        if not resultados:
            st.warning("😔 No hay supermercados en tu zona que tengan todos los productos de este carrito.")
            st.info("Algunos productos pueden no estar disponibles actualmente.")
            return False
        
        # Ordenar por precio total (misma lógica que Buscador de Productos)
        resultados.sort(key=lambda x: x['total'])
        mejor_opcion = resultados[0]
        
        st.success("✅ ¡Cálculo completado!")
        
        # Mostrar mejor opción destacada
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            border-radius: 15px;
            padding: 20px;
            color: white;
            margin: 15px 0;
            text-align: center;
        ">
            <h3>🏆 Mejor Opción Actualizada</h3>
            <h4>🏬 {mejor_opcion['nombre']}</h4>
            <h2 style="color: #FFD700;">Total: ${mejor_opcion['total']:.2f}</h2>
            <p>Precio actualizado para tu carrito guardado</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar comparación con otros supermercados
        if len(resultados) > 1:
            st.subheader("📊 Comparación de Precios Actualizada")
            for resultado in resultados:
                diferencia = resultado['total'] - mejor_opcion['total']
                st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.1);
                    border-radius: 8px;
                    padding: 10px;
                    margin: 8px 0;
                    border-left: 4px solid #4CAF50;
                ">
                    <strong>🏬 {resultado['nombre']}</strong><br>
                    Total: <strong>${resultado['total']:.2f}</strong>
                    {f"<span style='color: #ff6b6b;'> (+${diferencia:.2f})</span>" if diferencia > 0 else ""}
                </div>
                """, unsafe_allow_html=True)
        
        # Mostrar diferencia con el precio guardado
        precio_guardado = carrito_data['total']
        diferencia_total = mejor_opcion['total'] - precio_guardado
        
        if diferencia_total != 0:
            color_diferencia = "#28a745" if diferencia_total < 0 else "#dc3545"
            icono_diferencia = "📉" if diferencia_total < 0 else "📈"
            texto_diferencia = "bajó" if diferencia_total < 0 else "subió"
            
            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 15px;
                margin: 15px 0;
                text-align: center;
            ">
                <h4>{icono_diferencia} Cambio de Precio</h4>
                <p>El precio {texto_diferencia} desde que guardaste el carrito:</p>
                <p><strong>Precio guardado:</strong> ${precio_guardado:.2f}</p>
                <p><strong>Precio actual:</strong> ${mejor_opcion['total']:.2f}</p>
                <p style="color: {color_diferencia}; font-weight: bold;">
                    Diferencia: ${diferencia_total:.2f}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("💰 El precio se mantiene igual desde que guardaste el carrito")
        
        # ACTUALIZAR EL CARRITO EN LA BASE DE DATOS
        with st.spinner("Actualizando carrito con nuevos precios..."):
            try:
                # Actualizar solo el total del carrito
                response = supabase.table("Carrito").update({
                    'total': mejor_opcion['total']
                }).eq('id_carrito', carrito_data['id_carrito']).execute()
                
                if not response.data:
                    st.error("Error al actualizar el total del carrito")
                    return False
                
                st.success("✅ Carrito actualizado con el nuevo precio total")
                
                # Guardar información para la compra
                st.session_state["supermercado_seleccionado"] = mejor_opcion['nombre']
                st.session_state["total_compra"] = mejor_opcion['total']
                st.session_state["compra_confirmada"] = True
                
                return True
                
            except Exception as e:
                st.error(f"Error al actualizar el carrito: {str(e)}")
                return False
                
    except Exception as e:
        st.error(f"Error al recalcular precios: {str(e)}")
        return False

def obtener_precio_producto_supermercado(nombre_producto, marca, id_supermercado):
    """Obtiene el precio de un producto específico en un supermercado específico (misma función que Buscador de Productos)"""
    try:
        result = supabase.table("Productos").select("precio").eq("nombre_producto", nombre_producto).eq("marca", marca).eq("id_supermercado", id_supermercado).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]["precio"]
        return None
    except Exception as e:
        st.error(f"Error al obtener precio: {e}")
        return None

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
    # Verificar y agregar columna Estado si es necesario
    agregar_columna_estado()
    
    # Crear pestañas
    tab1, tab2, tab3 = st.tabs(["📝 Datos Personales", "📊 Productos Frecuentes", "🛒 Mis Carritos"])
    
    with tab1:
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
    
    with tab2:
        st.markdown("### 📊 Tus Productos Más Frecuentes")
        productos_frecuentes = obtener_productos_frecuentes(datos_usuario['id_cliente'])
        
        if productos_frecuentes:
            # Crear DataFrame para el gráfico
            df = pd.DataFrame(productos_frecuentes, columns=['Producto', 'Cantidad'])
            
            # Crear gráfico de torta con colores más llamativos
            fig = px.pie(df, values='Cantidad', names='Producto', 
                        title='Productos Más Comprados',
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
            
            # Personalizar el gráfico
            fig.update_traces(
                textposition='inside',
                textinfo='label',
                textfont_size=14,
                textfont_color='white',
                marker=dict(line=dict(color='white', width=2))
            )
            fig.update_layout(
                showlegend=False,
                title_font_size=20,
                title_font_color='#2B3674',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            # Mostrar el gráfico
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aún no tienes productos frecuentes. ¡Comienza a comprar!")
    
    with tab3:
        st.markdown("### 🛒 Mis Carritos")
        
        # Obtener carritos del usuario
        carritos = obtener_carritos_usuario()
        
        if not carritos:
            st.markdown("""
            <div class="empty-state">
                <h3>🛒 No tienes carritos guardados</h3>
                <p>Ve a "Buscador de Productos" para crear tu primer carrito</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Filtrar por estado
            estado_filtro = st.selectbox(
                "Filtrar por estado:",
                ["Todos", "Guardado", "Comprado"],
                key="filtro_estado"
            )
            
            carritos_filtrados = carritos
            if estado_filtro == "Guardado":
                carritos_filtrados = [c for c in carritos if c['estado'] == 'guardado']
            elif estado_filtro == "Comprado":
                carritos_filtrados = [c for c in carritos if c['estado'] == 'comprado']
            
            if not carritos_filtrados:
                st.info(f"No hay carritos con estado '{estado_filtro.lower()}'")
            else:
                st.info(f"Mostrando {len(carritos_filtrados)} carrito(s) {estado_filtro.lower()}")
                
                # Mostrar carritos en grid
                cols = st.columns(2)
                for i, carrito in enumerate(carritos_filtrados):
                    with cols[i % 2]:
                        # Determinar color del badge según estado
                        status_class = "status-guardado" if carrito['estado'] == 'guardado' else "status-comprado"
                        
                        st.markdown(f"""
                        <div class="cart-card">
                            <div class="cart-header">
                                <strong>Carrito #{carrito['id_carrito']}</strong>
                                <span class="status-badge {status_class}">{carrito['estado'].upper()}</span>
                            </div>
                            <div style="margin-bottom: 10px;">
                                <small>📅 {carrito['fecha']}</small>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Mostrar productos (máximo 3)
                        productos_mostrar = carrito['productos'][:3]
                        for producto in productos_mostrar:
                            st.markdown(f"""
                            <div class="cart-product">
                                <strong>{producto['nombre']}</strong> - {producto['marca']}<br>
                                <small>Cantidad: {producto['cantidad']} | Precio: ${producto['precio']:.2f}</small>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        if len(carrito['productos']) > 3:
                            st.markdown(f"<small>... y {len(carrito['productos']) - 3} producto(s) más</small>", unsafe_allow_html=True)
                        
                        st.markdown(f"""
                            <div class="cart-total">
                                Total: ${carrito['total']:.2f}
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Botones de acción
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if carrito['estado'] == 'guardado':
                                if st.button("🛒 Comprar", key=f"comprar_{carrito['id_carrito']}", use_container_width=True):
                                    if cargar_carrito_a_sesion(carrito):
                                        st.switch_page("pages/Forma de Pago.py")
                        
                        with col2:
                            if carrito['estado'] == 'guardado':
                                if st.button("💰 Recalcular", key=f"recalcular_{carrito['id_carrito']}", use_container_width=True):
                                    recalcular_precios_carrito(carrito)
                        
                        with col3:
                            if st.button("🗑️ Eliminar", key=f"eliminar_{carrito['id_carrito']}", use_container_width=True):
                                if eliminar_carrito(carrito['id_carrito']):
                                    st.rerun()
                        
                        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("No se pudieron cargar los datos del usuario. Por favor, intenta nuevamente.")
