import os
from datetime import datetime
import streamlit as st
from fpdf import FPDF
from docx import Document
from docx.shared import Inches

# ---------------------------
# Clase PDF personalizada
# ---------------------------
class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(
            0, 10,
            f"Calculadora de Pastelería Profesional – Chef More's | {fecha}",
            0, 0, "C"
        )

# ---------------------------
# Exportar a PDF
# ---------------------------
def export_to_pdf(nombre, data, porciones, notas):
    pdf = PDF()
    pdf.add_page()

    # Registrar fuente DejaVu (UTF-8 seguro)
    font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)
    pdf.set_font("DejaVu", "", 12)

    # Logo (arriba derecha)
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=170, y=8, w=30)

    # Título
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, nombre, ln=True, align="C")
    pdf.ln(10)

    # Ingredientes
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "Ingredientes:", ln=True)
    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porciones / data["porciones"]
        pdf.multi_cell(0, 10, f"- {ing['nombre']}: {cantidad_total:.2f} {ing['unidad']}")

    # Notas
    if notas:
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Notas: {notas}")

    # Exportar como descarga
    pdf_output = pdf.output(dest="S").encode("latin-1", "replace")
    st.download_button(
        label="📄 Descargar PDF",
        data=pdf_output,
        file_name=f"{nombre}.pdf",
        mime="application/pdf"
    )

# ---------------------------
# Exportar a Word
# ---------------------------
def export_to_docx(nombre, data, porciones, notas):
    doc = Document()

    # Logo
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        doc.add_picture(logo_path, width=Inches(1.0))

    # Título
    doc.add_heading(nombre, 0)

    # Ingredientes
    doc.add_heading("Ingredientes:", level=1)
    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porciones / data["porciones"]
        doc.add_paragraph(f"- {ing['nombre']}: {cantidad_total:.2f} {ing['unidad']}")

    # Notas
    if notas:
        doc.add_heading("Notas:", level=1)
        doc.add_paragraph(notas)

    # Pie de página (fecha y firma)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    doc.add_paragraph(
        f"Calculadora de Pastelería Profesional – Chef More's | {fecha}"
    )

    # Guardar en memoria
    from io import BytesIO
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="📝 Descargar Word",
        data=buffer,
        file_name=f"{nombre}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

