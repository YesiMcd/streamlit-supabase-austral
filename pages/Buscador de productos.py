import streamlit as st
from conexion import get_supabase_client

st.set_page_config(page_title="Buscador de Productos", page_icon="🛒", layout="centered")
supabase = get_supabase_client()

# 🎨 Estilo visual azul (no cambia el layout ni sidebar)
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    h1, h2, h3, h4 { color: #003366; }
    .stButton>button {
        color: white;
        background-color: #007BFF;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Buscador de Productos")
st.caption("Seleccioná tus productos y encontrá el supermercado con el **menor precio total** en tu zona.")

# 🧑 Obtener email desde sesión
if "email" not in st.session_state:
    st.error("🔐 Debés iniciar sesión para usar esta página.")
    st.stop()

usuario_email = st.session_state["email"]

@st.cache_data
def obtener_codigo_postal(email):
    result = supabase.table("cliente").select("código postal").eq("email", email).execute()
    if result.data and len(result.data) > 0:
        return result.data[0]["código postal"]
    return None

@st.cache_data
def obtener_productos_unicos():
    result = supabase.table("Productos").select("id,nombre").execute()
    return result.data if result.data else []

@st.cache_data
def obtener_precios_de_productos(productos_ids):
    result = supabase.table("Precios").select("producto_id,precio,supermercado_id").in_("producto_id", productos_ids).execute()
    return result.data if result.data else []

@st.cache_data
def obtener_supermercados_por_cp(cp):
    result = supabase.table("Supermercados").select("id,nombre").eq("código postal", cp).execute()
    return result.data if result.data else []

# 1️⃣ Obtener código postal del cliente
codigo_postal = obtener_codigo_postal(usuario_email)
if not codigo_postal:
    st.error("⚠️ No se encontró el código postal para este usuario.")
    st.stop()

# 2️⃣ Mostrar productos únicos
productos = obtener_productos_unicos()
productos_dict = {p["nombre"]: p["id"] for p in productos}
seleccionados = st.multiselect("🛍️ Seleccioná productos para tu carrito:", list(productos_dict.keys()))

if not seleccionados:
    st.info("🔹 Seleccioná al menos un producto para continuar.")
    st.stop()

# 3️⃣ Obtener precios para esos productos
productos_ids = [productos_dict[nombre] for nombre in seleccionados]
precios = obtener_precios_de_productos(productos_ids)
supermercados = obtener_supermercados_por_cp(codigo_postal)

supermercado_nombres = {s["id"]: s["nombre"] for s in supermercados}
supermercado_totales = {s["id"]: 0 for s in supermercados}

# 4️⃣ Calcular total por supermercado (solo los que tienen todos los productos)
for supermercado_id in supermercado_totales:
    total = 0
    disponible = True
    for pid in productos_ids:
        precios_dispo = [
            p["precio"] for p in precios 
            if p["producto_id"] == pid and p["supermercado_id"] == supermercado_id
        ]
        if precios_dispo:
            total += min(precios_dispo)
        else:
            disponible = False
            break
    if disponible:
        supermercado_totales[supermercado_id] = total
    else:
        supermercado_totales[supermercado_id] = None  # No lo muestres

# 5️⃣ Mostrar resultados ordenados
st.subheader("🔍 Supermercados disponibles en tu zona:")

ordenados = sorted(
    [(k, v) for k, v in supermercado_totales.items() if v is not None],
    key=lambda x: x[1]
)

if ordenados:
    for supermercado_id, total in ordenados:
        nombre = supermercado_nombres[supermercado_id]
        st.markdown(f"""
        <div style="background-color: #ffffff; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border-left: 5px solid #007BFF;">
            <h4>🏬 {nombre}</h4>
            <p>Total estimado: <strong style="color:#007BFF">${total:.2f}</strong></p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("😢 No se encontraron supermercados que tengan todos los productos seleccionados.")
