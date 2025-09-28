import streamlit as st
from recetas import RECETAS
from exporter import export_to_pdf, export_to_docx

st.set_page_config(page_title="Calculadora de Pastelería Profesional", layout="wide")

st.title("🍰 Calculadora de Pastelería Profesional - Chef More's")

# Sidebar
st.sidebar.header("Configuración")
receta = st.sidebar.selectbox("Selecciona una receta", list(RECETAS.keys()))
porcion = st.sidebar.number_input("Número de porciones", min_value=1, value=10)

# Mostrar receta seleccionada
data = RECETAS[receta]
st.subheader(f"📌 {receta}")
st.write(data["descripcion"])

st.markdown("### Ingredientes")
tabla = []
for ing, det in data["ingredientes"].items():
    cantidad_total = det["cantidad"] * porcion / data["base_porciones"]
    tabla.append([ing, f"{cantidad_total:.2f} {det['unidad']}", f"₡{det['costo'] * cantidad_total:.2f}"])

st.table(tabla)

# Notas
st.markdown("### 📝 Notas")
nota = st.text_area("Escribe tus observaciones aquí")

# Exportar
st.markdown("### 📂 Exportar Receta")
col1, col2 = st.columns(2)
with col1:
    if st.button("📄 Exportar a PDF"):
        export_to_pdf(receta, data, porcion, nota)
with col2:
    if st.button("📝 Exportar a Word"):
        export_to_docx(receta, data, porcion, nota)
