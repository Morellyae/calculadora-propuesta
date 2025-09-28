from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from docx import Document
from docx.shared import Inches
import os

# Exportar a PDF
def export_to_pdf(nombre_receta, ingredientes, porciones, notas):
    doc = SimpleDocTemplate(f"{nombre_receta}.pdf")
    styles = getSampleStyleSheet()
    story = []

    # Logo
    if os.path.exists("assets/logo.png"):
        story.append(Image("assets/logo.png", width=100, height=100))
        story.append(Spacer(1, 12))

    # Título
    story.append(Paragraph(f"<b>{nombre_receta}</b>", styles['Title']))
    story.append(Paragraph(f"Porciones: {porciones}", styles['Normal']))
    story.append(Spacer(1, 12))

    # Ingredientes en tabla
    data = [["Ingrediente", "Cantidad", "Unidad"]] + [
        [ing["nombre"], ing["cantidad"], ing["unidad"]] for ing in ingredientes
    ]
    table = Table(data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    # Notas
    if notas:
        story.append(Paragraph(f"<b>Notas:</b> {notas}", styles['Normal']))

    doc.build(story)

# Exportar a DOCX
def export_to_docx(nombre_receta, ingredientes, porciones, notas):
    doc = Document()

    # Logo
    if os.path.exists("assets/logo.png"):
        doc.add_picture("assets/logo.png", width=Inches(1.5))

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

    doc.save(f"{nombre_receta}.docx")
