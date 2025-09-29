import os
from fpdf import FPDF
from docx import Document
import streamlit as st

LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.png")

# === PDF ===
def export_to_pdf(nombre, data, porciones, nota):
    pdf = FPDF()
    pdf.add_page()

    # Logo
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=10, y=8, w=30)

    # Encabezado
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Chef More's - Calculadora de Pastelería Profesional", ln=True, align="C")
    pdf.ln(10)

    # Título receta
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, nombre, ln=True)

    # Descripción
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 10, data.get("descripcion", "Sin descripción disponible."))
    pdf.ln(5)

    # Ingredientes
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Ingredientes:", ln=True)
    pdf.set_font("Helvetica", "", 12)

    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porciones / data["porciones"]
        linea = f"- {ing['nombre']}: {cantidad_total:.2f} {ing['unidad']}"
        pdf.multi_cell(0, 8, linea)

    pdf.ln(5)

    # Notas
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Notas:", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, nota if nota else "Sin notas.")

    # Pie de página
    pdf.set_y(-20)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 10, "Chef More's © 2025 - Hecho con amor en Costa Rica", 0, 0, "C")

    # Exportar como descarga
    pdf_output = pdf.output(dest="S").encode("latin-1", "ignore")
    st.download_button(
        label="📄 Descargar PDF",
        data=pdf_output,
        file_name=f"{nombre}.pdf",
        mime="application/pdf",
    )

# === WORD ===
def export_to_docx(nombre, data, porciones, nota):
    doc = Document()

    # Encabezado
    doc.add_heading("Chef More's - Calculadora de Pastelería Profesional", level=0)
    doc.add_heading(nombre, level=1)

    # Descripción
    doc.add_paragraph(data.get("descripcion", "Sin descripción disponible."))

    # Ingredientes
    doc.add_heading("Ingredientes", level=2)
    for ing in data["ingredientes"]:
        cantidad_total = ing["cantidad"] * porciones / data["porciones"]
        doc.add_paragraph(
            f"{ing['nombre']}: {cantidad_total:.2f} {ing['unidad']}", style="List Bullet"
        )

    # Notas
    doc.add_heading("Notas", level=2)
    doc.add_paragraph(nota if nota else "Sin notas.")

    # Pie
    doc.add_paragraph("\nChef More's © 2025 - Hecho con amor en Costa Rica")

    # Exportar como descarga
    from io import BytesIO
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="📝 Descargar Word",
        data=buffer,
        file_name=f"{nombre}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

