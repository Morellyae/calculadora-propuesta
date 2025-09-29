from fpdf import FPDF
from docx import Document
import streamlit as st
import os

# Ruta a la fuente DejaVuSans
FONT_PATH = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")

# ---------------- PDF ---------------- #
def export_to_pdf(receta, data, porcion, nota):
    pdf = FPDF()
    pdf.add_page()

    # Registrar fuente
    if os.path.exists(FONT_PATH):
        pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
        pdf.set_font("DejaVu", "B", 16)
    else:
        pdf.set_font("Arial", "B", 16)

    pdf.cell(0, 10, receta, ln=True, align="C")

    # Descripción
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, data.get("descripcion", "Sin descripción disponible."))

    # Ingredientes
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Ingredientes", ln=True)

    pdf.set_font("Arial", "", 12)
    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porcion / data["porciones"]
        linea = f"- {ing['nombre']}: {cantidad_total:.2f} {ing['unidad']}"
        pdf.multi_cell(0, 10, linea)

    # Notas
    if nota:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Notas", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, nota)

    # Guardar en memoria
    filename = f"{receta}.pdf"
    pdf.output(filename)

    # Botón de descarga
    with open(filename, "rb") as f:
        st.download_button(
            label="⬇️ Descargar PDF",
            data=f,
            file_name=filename,
            mime="application/pdf"
        )

    return filename


# ---------------- WORD ---------------- #
def export_to_docx(receta, data, porcion, nota):
    doc = Document()
    doc.add_heading(receta, 0)

    doc.add_paragraph(data.get("descripcion", "Sin descripción disponible."))

    doc.add_heading("Ingredientes", level=1)
    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porcion / data["porciones"]
        doc.add_paragraph(
            f"- {ing['nombre']}: {cantidad_total:.2f} {ing['unidad']}"
        )

    if nota:
        doc.add_heading("Notas", level=1)
        doc.add_paragraph(nota)

    filename = f"{receta}.docx"
    doc.save(filename)

    with open(filename, "rb") as f:
        st.download_button(
            label="⬇️ Descargar Word",
            data=f,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    return filename

