from fpdf import FPDF
from docx import Document
from docx.shared import Inches, Pt
from datetime import datetime
import os

LOGO_PATH = "logo.png"

# -----------------------
# PDF Export
# -----------------------
def export_to_pdf(receta, data, porciones, nota):
    pdf = FPDF()
    pdf.add_page()

    # Fuente que soporte UTF-8
    pdf.add_font("DejaVu", "", fname="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", "", 12)

    # Logo arriba a la derecha
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=160, y=8, w=30)

    # Título
    pdf.set_font("DejaVu", "", 16)
    pdf.cell(0, 10, receta, ln=True, align="L")

    # Descripción
    pdf.set_font("DejaVu", "", 12)
    pdf.multi_cell(0, 10, data.get("descripcion", ""))

    # Ingredientes
    pdf.set_font("DejaVu", "B", 14)
    pdf.cell(0, 10, "Ingredientes", ln=True)
    pdf.set_font("DejaVu", "", 12)

    ingredientes = data.get("ingredientes", {})
    if isinstance(ingredientes, dict) and ingredientes:
        for ing, det in ingredientes.items():
            cantidad_total = det["cantidad"] * porciones / data["base_porciones"]
            costo_total = det["costo"] * cantidad_total
            pdf.cell(0, 8, f"- {ing}: {cantidad_total:.2f} {det['unidad']} | ₡{costo_total:.2f}", ln=True)
    else:
        pdf.cell(0, 8, "⚠️ No hay ingredientes definidos.", ln=True)

    # Notas
    if nota:
        pdf.set_font("DejaVu", "B", 14)
        pdf.cell(0, 10, "Notas:", ln=True)
        pdf.set_font("DejaVu", "", 12)
        pdf.multi_cell(0, 8, nota)

    # Pie de página
    pdf.set_y(-30)
    pdf.set_font("DejaVu", "I", 10)
    fecha = datetime.now().strftime("%d/%m/%Y")
    pdf.multi_cell(0, 6, f"Calculadora de Pastelería Profesional – Chef More’s\nFecha de exportación: {fecha}", align="C")

    filename = f"{receta.replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename


# -----------------------
# Word Export
# -----------------------
def export_to_docx(receta, data, porciones, nota):
    doc = Document()

    # Logo arriba derecha
    if os.path.exists(LOGO_PATH):
        header = doc.sections[0].header
        paragraph = header.paragraphs[0]
        run = paragraph.add_run()
        run.add_picture(LOGO_PATH, width=Inches(1))
        paragraph.alignment = 2

    # Título
    doc.add_heading(receta, level=1)

    # Descripción
    doc.add_paragraph(data.get("descripcion", ""))

    # Ingredientes
    doc.add_heading("Ingredientes", level=2)
    ingredientes = data.get("ingredientes", {})
    if isinstance(ingredientes, dict) and ingredientes:
        for ing, det in ingredientes.items():
            cantidad_total = det["cantidad"] * porciones / data["base_porciones"]
            costo_total = det["costo"] * cantidad_total
            doc.add_paragraph(f"- {ing}: {cantidad_total:.2f} {det['unidad']} | ₡{costo_total:.2f}")
    else:
        doc.add_paragraph("⚠️ No hay ingredientes definidos.")

    # Notas
    if nota:
        doc.add_heading("Notas", level=2)
        doc.add_paragraph(nota)

    # Pie de página
    section = doc.sections[0]
    footer = section.footer.paragraphs[0]
    fecha = datetime.now().strftime("%d/%m/%Y")
    footer.text = f"Calculadora de Pastelería Profesional – Chef More’s\nFecha de exportación: {fecha}"
    footer.runs[0].font.size = Pt(9)

    filename = f"{receta.replace(' ', '_')}.docx"
    doc.save(filename)
    return filename

    

