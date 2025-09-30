# app.py
import streamlit as st
import os
from recetas import RECETAS
from costos import COSTOS_UNITARIOS
from exporter import export_to_pdf, export_to_docx

st.set_page_config(page_title="Calculadora de Pastelería Profesional", layout="wide")

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.header("Chef More's")

# 1. Mostrar Logo (Verificamos si el archivo existe)
try:
    st.sidebar.image("logo.png", use_column_width=True)
except FileNotFoundError:
    st.sidebar.warning("Logo (logo.png) no encontrado en el repositorio.")

st.sidebar.markdown("---")
st.sidebar.header("Configuración")

# 2. Selector de Receta
receta = st.sidebar.selectbox("Selecciona una receta", list(RECETAS.keys()))

# 3. Input de Porciones
# Usamos el valor por defecto de la receta para el input
data = RECETAS[receta]
default_porciones = data.get("porciones", 10) # Usar 10 como fallback si no está en la receta
porcion = st.sidebar.number_input("Número de porciones", min_value=1, value=default_porciones)
st.sidebar.markdown("---")

# --- CUERPO PRINCIPAL ---
st.title("🍰 Calculadora de Pastelería Profesional - Chef More's")

st.subheader(f"📌 {receta}")
st.write(data.get("descripcion", "Sin descripción disponible."))

st.markdown("### Ingredientes")
tabla_ingredientes = []
tabla_costos = []
costo_total_receta = 0.0

# Calcular y mostrar tabla
try:
    factor_escala = porcion / data["porciones"]
    for ing in data["ingredientes"]:
        nombre_ingrediente = ing["nombre"]
        cantidad_original = ing.get("cantidad", 0)
        unidad_receta = ing.get("unidad", "")
        cantidad_total = cantidad_original * factor_escala

        # --- Lógica de Costos ---
        costo_info = COSTOS_UNITARIOS.get(nombre_ingrediente)
        costo_unitario_ing = 0.0
        costo_total_ing = 0.0

        if costo_info:
            costo_unitario_ing = costo_info["costo"]
            costo_total_ing = cantidad_total * costo_unitario_ing
            costo_total_receta += costo_total_ing
            
            tabla_costos.append([
                nombre_ingrediente,
                f"{cantidad_total:.2f} {unidad_receta}",
                f"${costo_unitario_ing:.3f}",
                f"${costo_total_ing:.2f}"
            ])
        else:
            tabla_costos.append([nombre_ingrediente, "Costo no definido", "", ""])
        # --- Fin Lógica de Costos ---


        # Formatear la cantidad para la tabla de ingredientes
        if unidad_receta.lower() in ["unid", "unidad"]:
            cantidad_str = f"{int(round(cantidad_total))}"
        else:
            cantidad_str = f"{cantidad_total:.2f}"

        tabla_ingredientes.append([nombre_ingrediente, f"{cantidad_str} {unidad_receta}"])

    # Mostrar Tabla de Ingredientes
    st.table(tabla_ingredientes)

except KeyError as e:
    st.error(f"Error en la estructura de la receta: falta la clave {e}. Verifica recetas.py")
except ZeroDivisionError:
    st.error("La receta base no puede tener cero porciones.")


# 4. Mostrar Costos
st.markdown("---")
st.markdown("### 💰 Costo Detallado de la Receta")

if costo_total_receta > 0:
    costo_por_porcion = costo_total_receta / porcion
    st.markdown(f"""
        **Costo Total de la Receta ({porcion} porciones):** **${costo_total_receta:.2f}** **Costo por Porción:** **${costo_por_porcion:.2f}**
    """)

    # Tabla de Costos
    st.table(
        [['Ingrediente', 'Cantidad Usada', 'Costo Unitario', 'Costo Total']] + tabla_costos
    )

else:
    st.info("Aún no se han definido los costos unitarios para todos los ingredientes.")


# 5. Notas
st.markdown("---")
st.markdown("### 📝 Notas")
nota = st.text_area("Escribe tus observaciones aquí", value=data.get("notas", ""))

# 6. Exportar
st.markdown("### 📂 Exportar Receta")
col1, col2 = st.columns(2)

# Variables para almacenar los bytes de los archivos
pdf_bytes = b''
docx_bytes = b''
pdf_file_name = f"{receta.replace(' ', '_')}_x{porcion}.pdf"
docx_file_name = f"{receta.replace(' ', '_')}_x{porcion}.docx"

# --- GENERAR PDF ---
with col1:
    try:
        pdf_bytes = export_to_pdf(receta, data["ingredientes"], porcion, nota, costo_total_receta, costo_por_porcion)
        st.download_button(
            label="Descargar PDF",
            data=pdf_bytes,
            file_name=pdf_file_name,
            mime="application/pdf",
            type="primary"
        )
    except Exception as e:
        st.warning(f"Error interno al generar el PDF. El botón está deshabilitado. Detalles: {e}")
        st.download_button(
            label="Descargar PDF (Error)",
            data=b'',
            file_name="error.pdf",
            mime="application/pdf",
            disabled=True
        )

# --- GENERAR DOCX ---
with col2:
    try:
        docx_bytes = export_to_docx(receta, data["ingredientes"], porcion, nota, costo_total_receta, costo_por_porcion)
        st.download_button(
            label="Descargar Word (DOCX)",
            data=docx_bytes,
            file_name=docx_file_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="secondary"
        )
    except Exception as e:
        st.warning(f"Error interno al generar el DOCX. El botón está deshabilitado. Detalles: {e}")
        st.download_button(
            label="Descargar Word (Error)",
            data=b'',
            file_name="error.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            disabled=True
        )

