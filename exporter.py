import os
from datetime import datetime
import streamlit as st
from fpdf import FPDF
from docx import Document
from docx.shared import Inches
from io import BytesIO

LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")
FONT_PATH = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")

# -------- PDF -------- #
class PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, x=170, y=8, w=25)
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Calculadora de Pastelería Profesional", ln=1, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 9)
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(
            0,
            10,
            f"Calculadora de Pastelería Profesional – Chef More’s | Exportado: {fecha}",
            align="C",
        )

def export_to_pdf(nombre, data, porcion, nota):
    pdf = PDF()
    pdf.set_font("Arial", "", 12)
    pdf.add_page()

    # Título receta
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, nombre, ln=1, align="C")

    # Ingredientes
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Ingredientes:", ln=1)

    pdf.set_font("Arial", "", 11)
    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porcion / data["porciones"]
        pdf.cell(0, 8, f"- {ing['nombre']}: {cantidad_total:.2f} {ing['unidad']}", ln=1)

    # Notas
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Notas:", ln=1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, nota if nota else "Sin notas adicionales.")

    # Descargar
    pdf_output = pdf.output(dest="S").encode("latin-1", "replace")
    st.download_button(
        label="📄 Descargar PDF",
        data=pdf_output,
        file_name=f"{nombre}.pdf",
        mime="application/pdf",
    )

# -------- WORD -------- #
def export_to_docx(nombre, data, porcion, nota):
    doc = Document()

    if os.path.exists(LOGO_PATH):
        doc.add_picture(LOGO_PATH, width=Inches(1.0))

    doc.add_heading(nombre, level=1)

    doc.add_heading("Ingredientes:", level=2)
    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porcion / data["porciones"]
        doc.add_paragraph(f"- {ing['nombre']}: {cantidad_total:.2f} {ing['unidad']}")

    doc.add_heading("Notas:", level=2)
    doc.add_paragraph(nota if nota else "Sin notas adicionales.")

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    doc.add_paragraph(
        f"\nCalculadora de Pastelería Profesional – Chef More’s\nExportado: {fecha}"
    )

    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    st.download_button(
        label="📝 Descargar Word",
        data=file_stream,
        file_name=f"{nombre}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
