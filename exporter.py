# Este archivo contiene las funciones para exportar la receta a PDF (usando fpdf) y DOCX (usando python-docx).
# Ambas funciones devuelven el archivo como bytes en memoria, lo cual es necesario para st.download_button en Streamlit.

from fpdf import FPDF
from docx import Document
from docx.shared import Inches
from io import BytesIO

# Exportar a PDF (usa fpdf, devuelve bytes)
def export_to_pdf(nombre_receta, ingredientes, porciones, notas):
    """Genera un archivo PDF con la receta y lo devuelve como objeto Bytes."""
    pdf = FPDF()
    
    # Usamos 'Times', una fuente interna de fpdf que está garantizada para funcionar 
    # y soporta acentos en español.
    FONT_NAME = 'Times'
    pdf.add_page()
    
    # Configuración de fuente y título
    pdf.set_font(FONT_NAME, "B", 16) 
    pdf.cell(0, 12, nombre_receta, 0, 1, "C") # Título centrado
    
    pdf.set_font(FONT_NAME, "", 12)
    pdf.cell(0, 8, f"Porciones: {porciones}", 0, 1)

    pdf.ln(5) # Salto de línea

    # Encabezados de la tabla de ingredientes
    pdf.set_font(FONT_NAME, "B", 12)
    pdf.set_fill_color(200, 220, 255) # Color de fondo
    pdf.cell(60, 10, "Ingrediente", 1, 0, "C", 1)
    pdf.cell(30, 10, "Cantidad", 1, 0, "C", 1)
    pdf.cell(30, 10, "Unidad", 1, 1, "C", 1) # 1 al final para salto de línea
    
    # Contenido de la tabla
    pdf.set_font(FONT_NAME, "", 11)
    for ing in ingredientes:
        pdf.cell(60, 8, ing["nombre"], 1, 0)
        pdf.cell(30, 8, str(ing["cantidad"]), 1, 0, "R") # Alineación a la derecha para números
        pdf.cell(30, 8, ing["unidad"], 1, 1)

    # Notas
    if notas:
        pdf.ln(10)
        pdf.set_font(FONT_NAME, "B", 12)
        pdf.cell(0, 8, "Notas:", 0, 1)
        pdf.set_font(FONT_NAME, "", 10)
        # multi_cell permite saltos de línea automáticos
        pdf.multi_cell(0, 5, notas)
        
    # === CORRECCIÓN CRÍTICA: Asegura que el tipo devuelto es 'bytes' para Streamlit. ===
    output_data = pdf.output(dest='S')
    if isinstance(output_data, str):
        # Si devuelve una cadena, la codificamos a bytes (necesario para fpdf con Times y acentos)
        return output_data.encode('latin-1')
    # Si ya es bytes o bytearray, lo devolvemos directamente.
    return output_data

# Exportar a DOCX (usa python-docx, devuelve bytes)
def export_to_docx(nombre_receta, ingredientes, porciones, notas):
    """Genera un archivo DOCX con la receta y lo devuelve como objeto Bytes."""
    doc = Document()

    # Título y porciones
    doc.add_heading(nombre_receta, 0)
    doc.add_paragraph(f"Porciones: {porciones}")
    doc.add_paragraph() # Salto de línea

    # Ingredientes
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Light Shading Accent 1' # Estilo de tabla
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Ingrediente'
    hdr_cells[1].text = 'Cantidad'
    hdr_cells[2].text = 'Unidad'

    for ing in ingredientes:
        row_cells = table.add_row().cells
        row_cells[0].text = ing["nombre"]
        row_cells[1].text = str(ing["cantidad"])
        row_cells[2].text = ing["unidad"]

    # Notas
    if notas:
        doc.add_heading('Notas', level=1)
        doc.add_paragraph(notas)

    # Guardar en memoria (BytesIO) y devolver los bytes (ESENCIAL para Streamlit)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

