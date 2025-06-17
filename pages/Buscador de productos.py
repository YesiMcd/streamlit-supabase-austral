import streamlit as st
from conexion import get_supabase_client

st.set_page_config(page_title="Buscador de Productos", page_icon="🛒", layout="wide")

# Inicializar cliente de Supabase
supabase = get_supabase_client()

# 🎨 Estilo visual
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    h1, h2, h3, h4 { color: #003366; }
    .stButton>button {
        color: white;
        background-color: #007BFF;
    }
    .cart-item {
        background-color: white;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        border-left: 3px solid #007BFF;
    }
    .cheapest {
        background-color: #e6ffe6;
        border-left: 3px solid #28a745;
    }
    .comprar-button {
        background-color: #28a745 !important;
        color: white !important;
        padding: 0.5rem 1rem !important;
        border-radius: 5px !important;
        border: none !important;
        font-weight: bold !important;
        width: 100% !important;
        margin-top: 10px !important;
        transition: all 0.3s ease !important;
    }
    .comprar-button:hover {
        background-color: #218838 !important;
        transform: translateY(-2px) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Buscador de Productos")
st.caption("Seleccioná tus productos y encontrá el supermercado con el **menor precio total** en tu zona.")

# 🧑 Obtener email desde sesión
if "user_email" not in st.session_state:
    st.error("🔐 Debés iniciar sesión para usar esta página.")
    st.stop()

usuario_email = st.session_state["user_email"]

def obtener_codigo_postal(email):
    try:
        result = supabase.table("Cliente").select('"código postal"').eq("email", email).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]["código postal"]
        return None
    except Exception as e:
        st.error(f"Error al obtener código postal: {e}")
        return None

@st.cache_data
def obtener_productos_unicos():
    try:
        result = supabase.table("Productos").select("nombre_producto,marca").execute()
        if result.data:
            productos_unicos = set((p.get('nombre_producto', ''), p.get('marca', '')) for p in result.data)
            return [{'nombre': nombre, 'marca': marca} for nombre, marca in productos_unicos]
        return []
    except Exception as e:
        st.error(f"Error al obtener productos: {e}")
        return []

@st.cache_data
def obtener_precios_producto(nombre, marca):
    try:
        result = supabase.table("Productos").select("id_supermercado,precio").eq("nombre_producto", nombre).eq("marca", marca).execute()
        return result.data if result.data else []
    except Exception as e:
        st.error(f"Error al obtener precios: {e}")
        return []

@st.cache_data
def obtener_supermercados_por_cp(cp):
    try:
        result = supabase.table("Supermercados").select("id_supermercado,nombre").eq("código postal", cp).execute()
        return result.data if result.data else []
    except Exception as e:
        st.error(f"Error al obtener supermercados: {e}")
        return []

# Inicializar el carrito
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# 1️⃣ Obtener código postal del cliente
codigo_postal = obtener_codigo_postal(usuario_email)
if not codigo_postal:
    st.error("⚠️ No se encontró el código postal para este usuario.")
    st.stop()

# 2️⃣ Búsqueda de productos
productos = obtener_productos_unicos()
if not productos:
    st.error("No se pudieron cargar los productos. Por favor, intenta nuevamente.")
    st.stop()

busqueda = st.text_input("🔍 Buscar por producto o marca:", "").lower()

productos_filtrados = [
    p for p in productos 
    if busqueda in p.get("nombre", "").lower() or busqueda in p.get("marca", "").lower()
]

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Productos Disponibles")
    for producto in productos_filtrados:
        key = f"prod_{producto.get('nombre', '')}_{producto.get('marca', '')}"
        if st.checkbox(f"{producto.get('nombre', '')} - {producto.get('marca', '')}", key=key):
            if producto not in st.session_state.carrito:
                st.session_state.carrito.append(producto)
        elif producto in st.session_state.carrito:
            st.session_state.carrito.remove(producto)

with col2:
    st.subheader("🛒 Mi Carrito")
    if not st.session_state.carrito:
        st.info("Tu carrito está vacío")
    else:
        for producto in st.session_state.carrito:
            st.markdown(f"""
            <div class="cart-item">
                <strong>{producto.get('nombre', '')}</strong><br>
                <small>{producto.get('marca', '')}</small>
            </div>
            """, unsafe_allow_html=True)

        if st.button("Calcular Precios", type="primary"):
            supermercados = obtener_supermercados_por_cp(codigo_postal)
            if not supermercados:
                st.error(f"No hay supermercados disponibles en tu zona (CP: {codigo_postal}).")
                st.stop()

            supermercado_nombres = {str(s['id_supermercado']): s['nombre'] for s in supermercados}
            supermercado_totales = {str(s['id_supermercado']): 0 for s in supermercados}

            for supermercado_id in supermercado_totales:
                total = 0
                disponible = True
                for producto in st.session_state.carrito:
                    precios = obtener_precios_producto(producto['nombre'], producto['marca'])
                    precios_super = [p['precio'] for p in precios if str(p['id_supermercado']) == supermercado_id]
                    if precios_super:
                        total += min(precios_super)
                    else:
                        disponible = False
                        break
                supermercado_totales[supermercado_id] = total if disponible else None

            st.subheader("💰 Precios por Supermercado")
            ordenados = sorted(
                [(k, v) for k, v in supermercado_totales.items() if v is not None],
                key=lambda x: x[1]
            )

            if ordenados:
                supermercado_mas_barato = ordenados[0]
                
                # Guardar datos en session_state
                st.session_state["supermercado_seleccionado"] = supermercado_nombres[supermercado_mas_barato[0]]
                st.session_state["total_compra"] = supermercado_mas_barato[1]
                st.session_state["productos_compra"] = st.session_state.carrito.copy()

                for i, (supermercado_id, total) in enumerate(ordenados):
                    nombre = supermercado_nombres[supermercado_id]
                    es_mas_barato = i == 0
                    clase = "cheapest" if es_mas_barato else ""
                    st.markdown(f"""
                    <div class="cart-item {clase}">
                        <h4>🏬 {nombre}</h4>
                        <p>Total: <strong style="color:#007BFF">${total:.2f}</strong></p>
                        {"<p style='color:#28a745'>¡El más barato! 💰</p>" if es_mas_barato else ""}
                    </div>
                    """, unsafe_allow_html=True)

                # Botón único de compra
                if st.button("🛒 Comprar en el supermercado más barato", key="comprar", use_container_width=True):
                    st.session_state["supermercado_seleccionado"] = supermercado_nombres[supermercado_mas_barato[0]]
                    st.session_state["total_compra"] = supermercado_mas_barato[1]
                    st.session_state["productos_compra"] = st.session_state.carrito.copy()
                    st.switch_page("Forma de Pago.py")

            else:
                st.warning("😢 No se encontraron supermercados que tengan todos los productos seleccionados.")

# Verificar si hay que mostrar página de pago o redirección
if "redirect_to_payment" in st.session_state and st.session_state["redirect_to_payment"]:
    st.session_state["redirect_to_payment"] = False
    
    # Mostrar página de pago directamente o mensaje de redirección
    st.info("🔄 Procesando compra...")
    
    # Opción 1: Mostrar la página de pago aquí mismo
    st.subheader("💳 Forma de Pago")
    st.write(f"**Supermercado:** {st.session_state.get('supermercado_seleccionado', 'N/A')}")
    st.write(f"**Total:** ${st.session_state.get('total_compra', 0):.2f}")
    
    if st.button("Volver al buscador"):
        del st.session_state["redirect_to_payment"]
        st.rerun()
    
    # Opción 2: JavaScript más fuerte para redirección
    st.markdown("""
    <script>
    // Redirección más agresiva
    setTimeout(function() {
        console.log('Intentando redirección...');
        var methods = [
            function() { window.location.replace('/Forma_de_Pago'); },
            function() { window.location.href = '/Forma_de_Pago'; },
            function() { window.top.location = '/Forma_de_Pago'; },
            function() { window.parent.location = '/Forma_de_Pago'; },
            function() { 
                // Si nada funciona, recargar con parámetro
                window.location.href = window.location.origin + '/?page=forma_de_pago';
            }
        ];
        
        for(let i = 0; i < methods.length; i++) {
            try {
                methods[i]();
                break;
            } catch(e) {
                console.log('Método ' + i + ' falló:', e);
                if(i === methods.length - 1) {
                    console.log('Todos los métodos de redirección fallaron');
                }
            }
        }
    }, 1000);
    </script>
    """, unsafe_allow_html=True)
    
    st.stop()  # Detener la ejecución del resto de la página