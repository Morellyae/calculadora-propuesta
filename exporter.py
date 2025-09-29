from fpdf import FPDF
from docx import Document
from docx.shared import Inches
from datetime import datetime
import streamlit as st
import os

# -------------------------------
# Exportar a PDF
# -------------------------------
def export_to_pdf(nombre_receta, data, porciones, nota):
    fecha = datetime.now().strftime("%d/%m/%Y")

    pdf = FPDF()
    pdf.add_page()

    # Registrar fuente compatible con tildes y ₡
    pdf.add_font("DejaVu", "", fname=os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf"), uni=True)
    pdf.set_font("DejaVu", "B", 14)

    # Logo en la esquina superior derecha
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=160, y=8, w=30)

    # Título
    pdf.cell(0, 10, nombre_receta, ln=True, align="C")
    pdf.ln(5)

    # Descripción
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(0, 10, data.get("descripcion", "Sin descripción disponible."))
    pdf.ln(5)

    # Ingredientes
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 10, "Ingredientes:", ln=True)
    pdf.set_font("DejaVu", "", 12)
    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porciones / data["porciones"]
        pdf.cell(0, 10, f"- {ing['nombre']}: {cantidad_total:.2f} {ing['unidad']}", ln=True)

    pdf.ln(5)

    # Notas
    if nota:
        pdf.set_font("DejaVu", "B", 12)
        pdf.cell(0, 10, "Notas:", ln=True)
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0, 10, nota)

    # Pie de página
    pdf.set_y(-15)
    pdf.set_font("DejaVu", "I", 8)
    pdf.cell(0, 10, f"Calculadora de Pastelería Profesional – Chef More’s | {fecha}", 0, 0, "C")

    # Guardar archivo temporal y devolver para descarga
    filename = f"{nombre_receta}.pdf"
    pdf.output(filename)
    with open(filename, "rb") as f:
        st.download_button("⬇️ Descargar PDF", f, file_name=filename, mime="application/pdf")


# -------------------------------
# Exportar a Word
# -------------------------------
def export_to_docx(nombre_receta, data, porciones, nota):
    fecha = datetime.now().strftime("%d/%m/%Y")

    doc = Document()

    # Encabezado con logo
    section = doc.sections[0]
    header = section.header
    paragraph = header.paragraphs[0]
    run = paragraph.add_run()

    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        run.add_picture(logo_path, width=Inches(1.0))

    # Título
    doc.add_heading(nombre_receta, 0)

    # Descripción
    doc.add_paragraph(data.get("descripcion", "Sin descripción disponible."))

    # Ingredientes
    doc.add_heading("Ingredientes", level=1)
    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porciones / data["porciones"]
        doc.add_paragraph(f"- {ing['nombre']}: {cantidad_total:.2f} {ing['unidad']}")

    # Notas
    if nota:
        doc.add_heading("Notas", level=1)
        doc.add_paragraph(nota)

    # Pie de página
    footer = section.footer
    footer.paragraphs[0].text = f"Calculadora de Pastelería Profesional – Chef More’s | {fecha}"

    # Guardar archivo temporal y devolver para descarga
    filename = f"{nombre_receta}.docx"
    doc.save(filename)
    with open(filename, "rb") as f:
        st.download_button("⬇️ Descargar Word", f, file_name=filename, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


      


