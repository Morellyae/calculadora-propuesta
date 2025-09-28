from fpdf import FPDF
from docx import Document
from docx.shared import Inches
from io import BytesIO
import os

# Exportar a PDF
def export_to_pdf(nombre_receta, ingredientes, porciones, notas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Título
    pdf.cell(0, 10, nombre_receta, 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Porciones: {porciones}", 0, 1)

    # Ingredientes (Tabla simple)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 10, "Ingrediente", 1, 0, "C")
    pdf.cell(30, 10, "Cantidad", 1, 0, "C")
    pdf.cell(30, 10, "Unidad", 1, 1, "C")
    
    pdf.set_font("Arial", "", 12)
    for ing in ingredientes:
        pdf.cell(60, 10, ing["nombre"], 1, 0)
        pdf.cell(30, 10, str(ing["cantidad"]), 1, 0)
        pdf.cell(30, 10, ing["unidad"], 1, 1)

    # Notas
    if notas:
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Notas:", 0, 1)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, notas)
        
    # Devuelve el PDF como bytes (para Streamlit)
    return pdf.output(dest='S').encode('latin-1')


# Exportar a DOCX
def export_to_docx(nombre_receta, ingredientes, porciones, notas):
    doc = Document()

    # Logo (opcional, si existe)
    if os.path.exists("logo.png"):
        doc.add_picture("logo.png", width=Inches(1.5))

    doc.add_heading(nombre_receta, 0)
    doc.add_paragraph(f"Porciones: {porciones}")

    # Ingredientes
    table = doc.add_table(rows=1, cols=3)
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

    # Devuelve el DOCX como bytes
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

