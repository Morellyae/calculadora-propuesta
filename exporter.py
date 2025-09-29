import os
from fpdf import FPDF
from docx import Document
from docx.shared import Inches
from io import BytesIO
from datetime import datetime
import streamlit as st


# -----------------------------
# Exportar a PDF
# -----------------------------
def export_to_pdf(nombre_receta, data, porciones, notas):
    pdf = FPDF()
    pdf.add_page()

    # Logo en esquina superior derecha
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=170, y=8, w=30)

    # Título
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, nombre_receta, ln=True, align="C")

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, f"Porciones: {porciones}", ln=True)

    # Ingredientes
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(80, 10, "Ingrediente", 1, 0, "C")
    pdf.cell(40, 10, "Cantidad", 1, 1, "C")

    pdf.set_font("Helvetica", "", 12)
    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porciones / data["porciones"]
        pdf.cell(80, 10, ing["nombre"], 1, 0)
        pdf.cell(40, 10, f"{cantidad_total:.2f} {ing['unidad']}", 1, 1)

    # Notas
    if notas:
        pdf.ln(10)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "Notas:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 8, notas)

    # Pie de página
    pdf.set_y(-20)
    pdf.set_font("Helvetica", "I", 8)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.multi_cell(0, 5, f"Calculadora de Pastelería Profesional – Chef More's\nFecha de exportación: {fecha}", align="C")

    # Devolver descarga en Streamlit
    pdf_output = pdf.output(dest="S").encode("latin-1")
    st.download_button(
        label="📄 Descargar PDF",
        data=pdf_output,
        file_name=f"{nombre_receta}.pdf",
        mime="application/pdf"
    )


# -----------------------------
# Exportar a Word
# -----------------------------
def export_to_docx(nombre_receta, data, porciones, notas):
    doc = Document()

    # Logo
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        doc.add_picture(logo_path, width=Inches(1.0))

    # Título
    doc.add_heading(nombre_receta, 0)
    doc.add_paragraph(f"Porciones: {porciones}")

    # Ingredientes
    doc.add_heading("Ingredientes", level=1)
    table = doc.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Ingrediente"
    hdr_cells[1].text = "Cantidad"

    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porciones / data["porciones"]
        row_cells = table.add_row().cells
        row_cells[0].text = ing["nombre"]
        row_cells[1].text = f"{cantidad_total:.2f} {ing['unidad']}"

    # Notas
    if notas:
        doc.add_heading("Notas", level=1)
        doc.add_paragraph(notas)

    # Pie de página
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    doc.add_paragraph("\n")
    doc.add_paragraph("Calculadora de Pastelería Profesional – Chef More's", style="Intense Quote")
    doc.add_paragraph(f"Fecha de exportación: {fecha}", style="Intense Quote")

    # Guardar en memoria
    bio = BytesIO()
    doc.save(bio)
    bio.seek(0)

    # Devolver descarga en Streamlit
    st.download_button(
        label="📝 Descargar Word",
        data=bio,
        file_name=f"{nombre_receta}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

