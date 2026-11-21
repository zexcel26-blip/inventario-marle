import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Inventario Marle", page_icon="💛", layout="wide")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #fff5f7 0%, #ffe4ec 100%); }
    h1 { color: #b76e79 !important; text-align: center; font-family: serif; }
    [data-testid="stSidebar"] { background-color: #fff0f5; }
    div[data-testid="stMetric"] {
        background: white; padding: 15px; border-radius: 15px;
        box-shadow: 0 4px 10px rgba(183,110,121,0.15);
        border-left: 5px solid #d4af37;
    }
    .stButton>button {
        background: linear-gradient(90deg, #b76e79, #d4af37);
        color: white; border-radius: 20px; border: none; font-weight: bold; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

ARCHIVO = "productos.csv"

if os.path.exists(ARCHIVO):
    df = pd.read_csv(ARCHIVO)
else:
    df = pd.DataFrame({
        "Producto": ["Collar Corazón", "Anillo Estrella", "Pulsera Luna"],
        "Stock": [15, 20, 10],
        "Precio": [450000, 320000, 280000]
    })
    df.to_csv(ARCHIVO, index=False)

if "df" not in st.session_state:
    st.session_state.df = df

df = st.session_state.df

# SOLO TU NOMBRE
st.markdown("<h1>✨ Inventario Marle ✨</h1><p style='text-align:center; color:#b76e79;'>Una marca de joyas con propósito</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("Total Productos", len(df))
c2.metric("Stock Total", int(df["Stock"].sum()) if len(df)>0 else 0)
valor_total = (df["Stock"] * df["Precio"]).sum() if len(df)>0 else 0
c3.metric("Valor Total", f"${valor_total:,.0f}")

st.divider()
st.subheader("📿 Inventario Actual")
st.dataframe(df, use_container_width=True, hide_index=True)

# BARRA IZQUIERDA
with st.sidebar:
    st.markdown("## 💛 Gestionar")
    
    with st.expander("➕ Agregar Producto"):
        with st.form("agregar"):
            nombre = st.text_input("Nombre del producto")
            stock = st.number_input("Stock", min_value=0, step=1)
            precio = st.number_input("Precio", min_value=0, step=1000)
            if st.form_submit_button("Agregar"):
                if nombre:
                    nuevo = pd.DataFrame({"Producto": [nombre], "Stock": [stock], "Precio": [precio]})
                    st.session_state.df = pd.concat([st.session_state.df, nuevo], ignore_index=True)
                    st.session_state.df.to_csv(ARCHIVO, index=False)
                    st.success(f"¡{nombre} agregado!")
                    st.rerun()

    with st.expander("✏️ Editar Producto"):
        if len(df) > 0:
            producto_editar = st.selectbox("Selecciona el producto", df["Producto"].tolist())
            idx = df[df["Producto"] == producto_editar].index[0]
            nuevo_nombre = st.text_input("Nombre", value=df.loc[idx, "Producto"], key="edit_nombre")
            nuevo_stock = st.number_input("Nuevo Stock", value=int(df.loc[idx, "Stock"]), min_value=0, key="edit_stock")
            nuevo_precio = st.number_input("Nuevo Precio", value=int(df.loc[idx, "Precio"]), min_value=0, key="edit_precio")
            if st.button("Guardar Cambios"):
                st.session_state.df.loc[idx, "Producto"] = nuevo_nombre
                st.session_state.df.loc[idx, "Stock"] = nuevo_stock
                st.session_state.df.loc[idx, "Precio"] = nuevo_precio
                st.session_state.df.to_csv(ARCHIVO, index=False)
                st.success("¡Actualizado!")
                st.rerun()

    with st.expander("🗑️ Eliminar Producto"):
        if len(df) > 0:
            producto_eliminar = st.selectbox("Selecciona para eliminar", df["Producto"].tolist(), key="del_select")
            if st.button("Eliminar Definitivamente"):
                st.session_state.df = st.session_state.df[st.session_state.df["Producto"] != producto_eliminar]
                st.session_state.df.to_csv(ARCHIVO, index=False)
                st.warning(f"¡{producto_eliminar} eliminado!")
                st.rerun()
