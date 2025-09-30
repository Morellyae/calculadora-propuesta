import streamlit as st
from recetas import RECETAS
from exporter import export_to_pdf, export_to_docx

st.set_page_config(page_title="Calculadora de Pastelería Profesional", layout="wide")

st.title("🍰 Calculadora de Pastelería Profesional - Chef More's")

# --- Configuración de Sidebar ---
st.sidebar.header("Configuración")
receta = st.sidebar.selectbox("Selecciona una receta", list(RECETAS.keys()))
porcion = st.sidebar.number_input("Número de porciones", min_value=1, value=10)

# Obtener datos de la receta seleccionada
data = RECETAS[receta]

# --- Presentación de la Receta ---
st.subheader(f"📌 {receta}")
st.write(data.get("descripcion", "Sin descripción disponible."))

st.markdown("### Ingredientes")
tabla = []

# Lógica para recalcular ingredientes
for ing in data["ingredientes"]:
    # Se asegura que la clave 'porciones' exista en data (por defecto 1)
    porciones_originales = data.get("porciones", 1) 
    
    if porciones_originales == 0:
        factor = porcion
    else:
        factor = porcion / porciones_originales
        
    cantidad_total = ing["cantidad"] * factor
    tabla.append([ing["nombre"], f"{cantidad_total:.2f} {ing['unidad']}"])

st.table(tabla)

# --- Sección de Notas ---
st.markdown("### 📝 Notas")
nota = st.text_area("Escribe tus observaciones aquí", value=data.get("notas", ""))

# --- Sección de Exportación y Botones ---
st.markdown("### 📂 Exportar Receta")
col1, col2 = st.columns(2)

# Botón de Descarga PDF
with col1:
    st.write("Generar PDF")
    
    # Llamamos a la función de exportación, pasando solo la lista de ingredientes
    pdf_bytes = export_to_pdf(receta, data["ingredientes"], porcion, nota)
    
    # Usamos st.download_button para que Streamlit gestione la descarga
    st.download_button(
        label="Descargar PDF",
        data=pdf_bytes,
        file_name=f"{receta}.pdf",
        mime="application/pdf"
    )

# Botón de Descarga DOCX
with col2:
    st.write("Generar Word (DOCX)")
    
    # Llamamos a la función de exportación
    docx_bytes = export_to_docx(receta, data["ingredientes"], porcion, nota)

    # Usamos st.download_button
    st.download_button(
        label="Descargar DOCX",
        data=docx_bytes,
        file_name=f"{receta}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
