#CREADO POR GEMINI AI 2.5 PRO
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os

# --- Configuración de la Página ---
st.set_page_config(page_title="Calculadora Ley de Ohm", page_icon="⚡")

# --- Constantes y Mapas de Colores ---
VALORES_DIGITOS = {
    "negro": 0, "cafe": 1, "rojo": 2, "naranja": 3, "amarillo": 4,
    "verde": 5, "azul": 6, "violeta": 7, "gris": 8, "blanco": 9
}

VALORES_MULTIPLICADOR = {
    "plateado": 0.01, "dorado": 0.1, "negro": 1, "cafe": 10,
    "rojo": 100, "naranja": 1000, "amarillo": 10000, "verde": 100000,
    "azul": 1000000, "violeta": 10000000, "gris": 100000000, "blanco": 1000000000
}

COLORES_DIGITOS_INV = {v: k for k, v in VALORES_DIGITOS.items()}

# --- Funciones Auxiliares ---
def calcular_resistencia_desde_colores(c1, c2, c3):
    val1 = VALORES_DIGITOS[c1]
    val2 = VALORES_DIGITOS[c2]
    multi = VALORES_MULTIPLICADOR[c3]
    return (val1 * 10 + val2) * multi

def formatear_resistencia(valor):
    if valor >= 1000000:
        return f"{valor/1000000:.2f} MΩ"
    elif valor >= 1000:
        return f"{valor/1000:.2f} kΩ"
    else:
        return f"{valor:.2f} Ω"

# --- Interfaz Principal ---
st.title("⚡ Calculadora Interactiva: Ley de Ohm")
st.markdown("Esta aplicación te permite calcular Voltaje, Corriente o Resistencia. Con la fórmula dada para hallar la incógnita y la gráfica, se puede evidenciar el comportamiento de relación directa o inversamente directa")

# --- Carga de Imagen ---
directorio_script = os.path.dirname(os.path.abspath(__file__))
ruta_completa = os.path.join(directorio_script, "Resistencias.jpg")

if os.path.exists(ruta_completa):
    st.image(ruta_completa, caption="Código de Colores", use_container_width=True)
else:
    st.warning(f"No se encontró la imagen en: {directorio_script}")

st.markdown("---")

# --- Lógica de la Aplicación ---
modo = st.radio("¿Qué deseas calcular?", ["Voltaje (V)", "Corriente (I)", "Resistencia (R)"], horizontal=True)

st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎛️ Controles")

    # -----------------------------------------
    # MODO 1: Calcular VOLTAJE (V = I * R)
    # -----------------------------------------
    if modo == "Voltaje (V)":
        st.info("Fórmula: V = I * R")
        
        # CORRECCIÓN 1: step=1.0 para enteros
        corriente = st.slider("Corriente (Amperios)", min_value=0.0, max_value=500.0, value=1.0, step=1.0)
        
        st.markdown("**Resistencia (Código de Colores):**")
        c1 = st.selectbox("Banda 1", list(VALORES_DIGITOS.keys()), index=2) 
        c2 = st.selectbox("Banda 2", list(VALORES_DIGITOS.keys()), index=0) 
        c3 = st.selectbox("Multiplicador", list(VALORES_MULTIPLICADOR.keys()), index=2) 
        
        resistencia = calcular_resistencia_desde_colores(c1, c2, c3)
        st.success(f"Resistencia: {formatear_resistencia(resistencia)}")
        
        voltaje = corriente * resistencia
        st.metric(label="Voltaje Resultante", value=f"{voltaje:.2f} V")

        # CORRECCIÓN 2: La gráfica ahora va hasta 500 (igual que el slider)
        x_data = np.linspace(0, 500, 100) 
        y_data = x_data * resistencia
        x_label, y_label = "Corriente (A)", "Voltaje (V)"
        current_x, current_y = corriente, voltaje

    # -----------------------------------------
    # MODO 2: Calcular CORRIENTE (I = V / R)
    # -----------------------------------------
    elif modo == "Corriente (I)":
        st.info("Fórmula: I = V / R")
        
        # CORRECCIÓN 1: step=1.0 para enteros
        voltaje = st.slider("Voltaje (Voltios)", min_value=0.0, max_value=5000.0, value=12.0, step=1.0)
        
        st.markdown("**Resistencia (Código de Colores):**")
        c1 = st.selectbox("Banda 1", list(VALORES_DIGITOS.keys()), index=1) 
        c2 = st.selectbox("Banda 2", list(VALORES_DIGITOS.keys()), index=0) 
        c3 = st.selectbox("Multiplicador", list(VALORES_MULTIPLICADOR.keys()), index=2) 
        
        resistencia = calcular_resistencia_desde_colores(c1, c2, c3)
        st.success(f"Resistencia: {formatear_resistencia(resistencia)}")

        if resistencia > 0:
            corriente = voltaje / resistencia
            st.metric(label="Corriente Resultante", value=f"{corriente:.4f} A")
            
            # CORRECCIÓN 2: La gráfica ahora va hasta 5000 (igual que el slider)
            x_data = np.linspace(0, 5000, 100)
            y_data = x_data / resistencia
            x_label, y_label = "Voltaje (V)", "Corriente (I)"
            current_x, current_y = voltaje, corriente
        else:
            st.error("La resistencia no puede ser 0.")
            x_data, y_data = [], []

    # -----------------------------------------
    # MODO 3: Calcular RESISTENCIA (R = V / I)
    # -----------------------------------------
    elif modo == "Resistencia (R)":
        st.info("Fórmula: R = V / I")
        
        # CORRECCIÓN 1: step=1.0 para enteros
        voltaje = st.slider("Voltaje (Voltios)", min_value=0.0, max_value=5000.0, value=10.0, step=1.0)
        corriente = st.slider("Corriente (Amperios)", min_value=1.0, max_value=500.0, value=1.0, step=1.0)
        
        resistencia = voltaje / corriente
        st.metric(label="Resistencia Calculada", value=f"{formatear_resistencia(resistencia)}")
        
        # CORRECCIÓN 2: La gráfica (Eje X es corriente) va hasta 500
        x_data = np.linspace(0, 500, 100)
        y_data = x_data * resistencia
        x_label, y_label = "Corriente (A)", "Voltaje (V)"
        current_x, current_y = corriente, voltaje

# --- Gráfica ---
with col2:
    st.subheader("📈 Gráfica de Comportamiento")
    
    if len(x_data) > 0:
        fig, ax = plt.subplots()
        ax.plot(x_data, y_data, color='blue', label='Ley de Ohm')
        ax.scatter([current_x], [current_y], color='red', zorder=5, s=100, label='Valor Actual')
        
        # Líneas guía
        ax.axvline(x=current_x, color='gray', linestyle='--', alpha=0.5)
        ax.axhline(y=current_y, color='gray', linestyle='--', alpha=0.5)
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(f"Relación {y_label} vs {x_label}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)