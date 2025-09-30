# app.py
import streamlit as st
import os
import pandas as pd
from recetas import RECETAS
from costos import COSTOS_UNITARIOS
from exporter import export_to_pdf, export_to_docx

st.set_page_config(page_title="Calculadora de Pastelería Profesional", layout="wide")

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.header("Chef More's")

# 1. Mostrar Logo (Corregida la advertencia de Streamlit)
try:
    # Usamos use_container_width en lugar de use_column_width
    st.sidebar.image("logo.png", use_container_width=True) 
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


# =========================================================================
# 4. EDICIÓN DE COSTOS (NUEVO MÓDULO)
# =========================================================================
st.sidebar.header("Ajustar Costos Unitarios (Editable)")

# Convertir el diccionario de costos en un DataFrame de pandas para facilitar la edición
# Creamos una copia para no modificar el original, y agregamos el nombre como columna.
costos_df = pd.DataFrame([
    {"Ingrediente": k, "Costo (por g/ml/unid)": v["costo"], "Unidad Base": v["unidad_base"]}
    for k, v in COSTOS_UNITARIOS.items()
])

# Permitir al usuario editar el DataFrame, enfocándose solo en la columna 'Costo'
# Usamos st.data_editor para permitir la edición en la barra lateral
edited_costos_df = st.sidebar.data_editor(
    costos_df,
    column_config={
        "Costo (por g/ml/unid)": st.column_config.NumberColumn(
            "Costo (por g/ml/unid)",
            help="Costo por gramo, mililitro o unidad base del ingrediente.",
            min_value=0.0,
            format="$%.5f", # Mostrar hasta 5 decimales para precisión
        ),
        "Ingrediente": st.column_config.TextColumn(disabled=True),
        "Unidad Base": st.column_config.TextColumn(disabled=True),
    },
    hide_index=True,
    num_rows="fixed",
)

# Convertir el DataFrame editado de vuelta a un diccionario para usar en la lógica
# Usamos un nuevo diccionario (COSTOS_ACTUALES) para el cálculo
COSTOS_ACTUALES = {}
for index, row in edited_costos_df.iterrows():
    nombre = row["Ingrediente"]
    costo = row["Costo (por g/ml/unid)"]
    unidad_base = row["Unidad Base"]
    COSTOS_ACTUALES[nombre] = {"costo": costo, "unidad_base": unidad_base}


# --- CUERPO PRINCIPAL ---
st.title("🍰 Calculadora de Pastelería Profesional - Chef More's")

st.subheader(f"📌 {receta}")
st.write(data.get("descripcion", "Sin descripción disponible."))

st.markdown("### Ingredientes")
tabla_ingredientes = []
tabla_costos = []
costo_total_receta = 0.0
costo_por_porcion = 0.0 # Inicializamos para el ámbito de exportación

# Calcular y mostrar tabla
try:
    # Usamos la cantidad de porciones de la receta original para el factor de escala
    porciones_base = data.get("porciones", 10)
    factor_escala = porcion / porciones_base
    
    # Creamos una lista temporal para guardar los ingredientes escalados, que se usa en la exportación
    ingredientes_escalados_para_exportar = []

    for ing in data["ingredientes"]:
        nombre_ingrediente = ing["nombre"]
        cantidad_original = ing.get("cantidad", 0)
        unidad_receta = ing.get("unidad", "")
        cantidad_total = cantidad_original * factor_escala

        # --- Lógica de Costos (Usando COSTOS_ACTUALES editables) ---
        costo_info = COSTOS_ACTUALES.get(nombre_ingrediente)
        costo_unitario_ing = 0.0
        costo_total_ing = 0.0

        if costo_info:
            costo_unitario_ing = costo_info["costo"]
            costo_total_ing = cantidad_total * costo_unitario_ing
            costo_total_receta += costo_total_ing
            
            # Añadir fila a la tabla de costos
            tabla_costos.append([
                nombre_ingrediente,
                f"{cantidad_total:.2f} {unidad_receta}",
                f"${costo_unitario_ing:.5f}",
                f"${costo_total_ing:.2f}"
            ])
        else:
            # Si el ingrediente no está en la lista de costos
            tabla_costos.append([nombre_ingrediente, "Costo no definido", "", ""])
        # --- Fin Lógica de Costos ---


        # Formatear la cantidad para la tabla de ingredientes
        if unidad_receta.lower() in ["unid", "unidad"]:
            cantidad_str = f"{int(round(cantidad_total))}"
        else:
            cantidad_str = f"{cantidad_total:.2f}"

        tabla_ingredientes.append([nombre_ingrediente, f"{cantidad_str} {unidad_receta}"])
        
        # Guardar la información escalada para pasarla a la función de exportación
        ingredientes_escalados_para_exportar.append({
            "nombre": nombre_ingrediente,
            "cantidad": cantidad_original, # Mantenemos el original para referencia
            "cantidad_escalada": cantidad_total, # NUEVO: Valor escalado
            "unidad": unidad_receta
        })

    # Mostrar Tabla de Ingredientes
    st.table(tabla_ingredientes)

except KeyError as e:
    st.error(f"Error en la estructura de la receta: falta la clave {e}. Verifica recetas.py")
except ZeroDivisionError:
    st.error("La receta base no puede tener cero porciones.")


# 5. Mostrar Costos
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
    st.info("Aún no se han definido los costos unitarios para algunos ingredientes o la cantidad de porciones es cero.")


# 6. Notas
st.markdown("---")
st.markdown("### 📝 Notas")
nota = st.text_area("Escribe tus observaciones aquí", value=data.get("notas", ""))

# 7. Exportar
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
        # Pasamos la lista de ingredientes_escalados_para_exportar, que ya contiene la cantidad final
        pdf_bytes = export_to_pdf(receta, ingredientes_escalados_para_exportar, porcion, nota, costo_total_receta, costo_por_porcion)
        st.download_button(
            label="Descargar PDF",
            data=pdf_bytes,
            file_name=pdf_file_name,
            mime="application/pdf",
            type="primary"
        )
    except Exception as e:
        # Aseguramos que el error se muestre en la consola para depuración
        print(f"Error al generar PDF: {e}")
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
        # Pasamos la lista de ingredientes_escalados_para_exportar
        docx_bytes = export_to_docx(receta, ingredientes_escalados_para_exportar, porcion, nota, costo_total_receta, costo_por_porcion)
        st.download_button(
            label="Descargar Word (DOCX)",
            data=docx_bytes,
            file_name=docx_file_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="secondary"
        )
    except Exception as e:
        # Aseguramos que el error se muestre en la consola para depuración
        print(f"Error al generar DOCX: {e}")
        st.warning(f"Error interno al generar el DOCX. El botón está deshabilitado. Detalles: {e}")
        st.download_button(
            label="Descargar Word (Error)",
            data=b'',
            file_name="error.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            disabled=True
        )

