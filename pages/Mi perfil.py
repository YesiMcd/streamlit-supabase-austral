import streamlit as st
from conexion import get_supabase_client
import plotly.express as px
import pandas as pd

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

# Función para obtener los productos más frecuentes del usuario
def obtener_productos_frecuentes(id_cliente):
    try:
        # Obtener todos los carritos del usuario
        response = supabase.table('Carrito').select('id_carrito').eq('id_cliente', id_cliente).execute()
        if not response.data:
            return []
        
        id_carritos = [carrito['id_carrito'] for carrito in response.data]
        
        # Obtener los detalles de los carritos
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

# Función para obtener los últimos carritos del usuario
def obtener_ultimos_carritos(id_cliente, limite=3):
    try:
        # Obtener los últimos carritos del usuario
        response = supabase.table('Carrito').select('*').eq('id_cliente', id_cliente).execute()
        
        if not response.data:
            return []
        
        carritos_completos = []
        for carrito in response.data:
            # Obtener los detalles del carrito
            detalles_response = supabase.table('Det Carrito').select('*').eq('id_carrito', carrito['id_carrito']).execute()
            
            if detalles_response.data:
                # Obtener información de los productos
                productos = []
                for detalle in detalles_response.data:
                    producto_response = supabase.table('Productos').select('nombre_producto, marca').eq('id_productos', detalle['id_producto']).execute()
                    
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
                    'productos': productos
                })
        
        return carritos_completos
    except Exception as e:
        st.error(f"Error al obtener últimos carritos: {str(e)}")
        return []

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

    /* Estilos para las tarjetas de carrito */
    .cart-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .cart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        padding-bottom: 10px;
        border-bottom: 1px solid #eee;
    }
    .cart-product {
        padding: 8px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    .cart-total {
        margin-top: 10px;
        text-align: right;
        font-weight: bold;
        color: #2B3674;
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
    # Crear pestañas
    tab1, tab2, tab3 = st.tabs(["📝 Datos Personales", "📊 Productos Frecuentes", "🛒 Últimos Carritos"])
    
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
        st.markdown("### 🛒 Tus Últimos Carritos")
        ultimos_carritos = obtener_ultimos_carritos(datos_usuario['id_cliente'])
        
        if ultimos_carritos:
            for carrito in ultimos_carritos:
                st.markdown(f"""
                <div class="cart-card">
                    <div class="cart-header">
                        <strong>Carrito #{carrito['id_carrito']}</strong>
                        <span>{carrito['fecha']}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                for producto in carrito['productos']:
                    st.markdown(f"""
                    <div class="cart-product">
                        <strong>{producto['nombre']}</strong> - {producto['marca']}<br>
                        <small>Cantidad: {producto['cantidad']} | Precio: ${producto['precio']:.2f}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div class="cart-total">
                        Total: ${carrito['total']:.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aún no tienes carritos guardados. ¡Comienza a comprar!")
else:
    st.error("No se pudieron cargar los datos del usuario. Por favor, intenta nuevamente.")
