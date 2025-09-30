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
st.write(data.get("descripcion", "Sin descripción disponible."))

st.markdown("### Ingredientes")
tabla = []
# Se calcula la cantidad total de ingredientes ajustada por la porción
for ing in data["ingredientes"]:
    # Se asegura que la clave 'porciones' exista en data
    porciones_originales = data.get("porciones", 1) 
    
    # Manejo de división por cero si la receta no tiene porciones definidas (default a 1)
    if porciones_originales == 0:
        factor = porcion
    else:
        factor = porcion / porciones_originales
        
    cantidad_total = ing["cantidad"] * factor
    tabla.append([ing["nombre"], f"{cantidad_total:.2f} {ing['unidad']}"])

st.table(tabla)

# Notas
st.markdown("### 📝 Notas")
nota = st.text_area("Escribe tus observaciones aquí", value=data.get("notas", ""))

# Exportar
st.markdown("### 📂 Exportar Receta")
col1, col2 = st.columns(2)

# --- CORRECCIÓN 1: Pasar data["ingredientes"] y usar st.download_button ---
with col1:
    st.write("PDF")
    # 1. Llamamos a la función con el argumento correcto: data["ingredientes"]
    pdf_bytes = export_to_pdf(receta, data["ingredientes"], porcion, nota)
    
    # 2. Usamos st.download_button para que el usuario pueda descargar los bytes devueltos
    st.download_button(
        label="Descargar PDF",
        data=pdf_bytes,
        file_name=f"{receta}.pdf",
        mime="application/pdf"
    )

with col2:
    st.write("DOCX")
    # 1. Llamamos a la función con el argumento correcto: data["ingredientes"]
    docx_bytes = export_to_docx(receta, data["ingredientes"], porcion, nota)

    # 2. Usamos st.download_button para que el usuario pueda descargar los bytes devueltos
    st.download_button(
        label="Descargar DOCX",
        data=docx_bytes,
        file_name=f"{receta}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
