import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="¡Pedido Exitoso!",
    page_icon="🛍️",
    layout="centered"
)

# Estilo personalizado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    .main {
        background: linear-gradient(135deg, #E8F0FE, #F8FAFF);
        min-height: 100vh;
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
        background: linear-gradient(45deg, #E8F0FE 0%, #F8FAFF 100%);
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
    st.session_state["page"] = "inicio"