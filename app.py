import streamlit as st
import pandas as pd

st.set_page_config(page_title="Inventario de MARLE", page_icon="💖", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e9c6ff 0%, #c9a6ff 40%, #ffb3d9 100%);
    }
    h1 {
        color: #d6005c !important;
        text-align: center;
        text-shadow: 0 0 10px white;
    }
    .metric-card {
        background: rgba(255,255,255,0.9);
        border: 2px solid #ffb3d9;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-number {
        font-size: 45px;
        font-weight: bold;
        color: #e9408a;
    }
    .stForm, div[data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        border: 2px solid #ffb3d9;
        padding: 15px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff8cc6, #a678ff);
        color: white;
        border: none;
        border-radius: 15px;
        font-weight: bold;
        font-size: 18px;
        height: 50px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💖 Mi Control de Inventario</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#6a3fb5;'>Proyecto de MARLE</h3>", unsafe_allow_html=True)

if "inventario" not in st.session_state:
    st.session_state.inventario = pd.DataFrame([
        ["Cuaderno kawaii", "Papelería", 10, 25.50],
        ["Plumas gel", "Escritura", 3, 12.00],
        ["Notas adhesivas", "Oficina", 20, 8.75],
        ["Pegatinas", "Decoración", 2, 5.00],
    ], columns=["Producto", "Categoría", "Cantidad", "Precio"])

# Métricas arriba
total = len(st.session_state.inventario)
bajo = len(st.session_state.inventario[st.session_state.inventario["Cantidad"] <= 5])
categorias = st.session_state.inventario["Categoría"].nunique()

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='metric-card'>📦 Productos Totales<br><span class='metric-number'>{total}</span><br>registrados</div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'>⚠️ Stock Bajo<br><span class='metric-number'>{bajo}</span><br>requiere reposición</div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'>🏷️ Categorías<br><span class='metric-number'>{categorias}</span><br>activas</div>", unsafe_allow_html=True)

st.write("")

col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("➕ Agregar nuevo producto")
    with st.form("form"):
        prod = st.text_input("Producto", placeholder="Ej. Cuaderno kawaii")
        cant = st.number_input("Cantidad", min_value=1, value=10)
        cat = st.selectbox("Categoría", ["Papelería", "Escritura", "Oficina", "Decoración", "Otra"])
        precio = st.number_input("Precio ($)", min_value=0.0, value=25.50)
        btn = st.form_submit_button("💜 Agregar al inventario 💜")
        if btn and prod:
            nuevo = pd.DataFrame([[prod, cat, cant, precio]], columns=["Producto", "Categoría", "Cantidad", "Precio"])
            st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)
            st.balloons()
            st.success(f"¡{prod} agregado!")

with col_der:
    st.subheader("📋 Inventario Actual")
    # Agregar estado
    df_show = st.session_state.inventario.copy()
    df_show["Estado"] = df_show["Cantidad"].apply(lambda x: "En stock" if x > 5 else "Stock bajo")
    st.dataframe(df_show, use_container_width=True, hide_index=True)

st.caption("✨ Última actualización: Hoy • Hecho con Streamlit ✨")