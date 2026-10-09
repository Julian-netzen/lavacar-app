import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="Lavacar Los Ángeles",
    page_icon="🧼",
    layout="centered"
)

# Estilo personalizado para celular
st.markdown("""
    <style>
    .main { padding: 1rem; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "LavacarDatos.json"

# Cargar y guardar datos
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "registros" not in st.session_state:
    st.session_state.registros = load_data()

st.title("🧼 Lavacar Los Ángeles")
st.subheader("Registro y Control de Lavados")

# Precios sugeridos
SERVICIOS = {
    "Lavado Sencillo (Auto)": 5000,
    "Lavado Completo (Auto)": 8000,
    "Lavado Sencillo (SUV/Pick-up)": 7000,
    "Lavado Completo (SUV/Pick-up)": 10000,
    "Lavado de Motor": 6000,
    "Lustrado / Encerado": 12000
}

# Formulario de Registro
with st.form("form_registro", clear_on_submit=True):
    st.markdown("### 🚘 Nuevo Servicio")
    placa = st.text_input("Placa o Modelo del Vehículo").strip().upper()
    servicio_sel = st.selectbox("Tipo de Servicio", list(SERVICIOS.keys()))
    precio_default = SERVICIOS[servicio_sel]
    precio = st.number_input("Monto en Colones (₡)", min_value=0, value=precio_default, step=500)
    notas = st.text_input("Observaciones / Notas (Opcional)")
    
    submitted = st.form_submit_button("✅ Registrar Lavado")
    
    if submitted:
        if not placa:
            st.error("Por favor ingresa la placa o descripción del vehículo.")
        else:
            nuevo_registro = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "placa": placa,
                "servicio": servicio_sel,
                "monto": precio,
                "notas": notas
            }
            st.session_state.registros.append(nuevo_registro)
            save_data(st.session_state.registros)
            st.success(f"¡Servicio registrado para {placa} por ₡{precio:,}!")

# Resumen y Reporte
st.divider()
st.markdown("### 📊 Resumen de Ingresos")

if st.session_state.registros:
    df = pd.DataFrame(st.session_state.registros)
    total_vehiculos = len(df)
    total_ingresos = df["monto"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Vehículos Lavados", f"{total_vehiculos}")
    col2.metric("Total Recaudado", f"₡{total_ingresos:,}")

    with st.expander("👀 Ver historial detallado de lavados"):
        st.dataframe(df.sort_values(by="fecha", ascending=False), use_container_width=True)

    # Botón para descargar datos en CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte (CSV)",
        data=csv,
        file_name=f"reporte_lavacar_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
else:
    st.info("Aún no hay servicios registrados el día de hoy.")
