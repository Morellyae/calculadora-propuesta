# exporter.py
# Exporta recetas a PDF (fpdf2) y DOCX (python-docx), con logo en cabecera y pie de página.

from fpdf import FPDF
from docx import Document
from docx.shared import Inches
from io import BytesIO

# ---------------------------
# Cargar logo en memoria (BytesIO)
# ---------------------------
try:
    with open("logo.png", "rb") as f:
        LOGO_DATA = BytesIO(f.read())
except FileNotFoundError:
    LOGO_DATA = None
    print("Advertencia: 'logo.png' no encontrado. La exportación funcionará sin logo.")


# ---------------------------
# Clase personalizada PDF con pie de página
# ---------------------------
class PDF(FPDF):
    def footer(self):
        # Posición 15 mm desde el final
        self.set_y(-15)
        self.set_font("Times", "I", 8)
        self.cell(0, 10, "Chef More's - Recetas Profesionales", 0, 0, "C")


# ---------------------------
# Exportar a PDF
# ---------------------------
def export_to_pdf(nombre_receta, ingredientes, porciones, notas):
    """Genera un PDF con logo y pie de página."""
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    FONT_NAME = 'Times'

    # === HEADER: Logo y título ===
    if LOGO_DATA:
        LOGO_DATA.seek(0)
        pdf.image(LOGO_DATA, x=10, y=10, w=30)
        pdf.set_xy(45, 15)
        pdf.set_font(FONT_NAME, "B", 18)
        pdf.cell(0, 10, nombre_receta, 0, 1, "L")
        pdf.ln(5)
    else:
        pdf.ln(10)
        pdf.set_font(FONT_NAME, "B", 16)
        pdf.cell(0, 12, nombre_receta, 0, 1, "C")

    pdf.set_font(FONT_NAME, "", 12)
    pdf.cell(0, 8, f"Porciones: {porciones}", 0, 1)

    pdf.ln(5)

    # Tabla ingredientes
    pdf.set_font(FONT_NAME, "B", 12)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(60, 10, "Ingrediente", 1, 0, "C", 1)
    pdf.cell(30, 10, "Cantidad", 1, 0, "C", 1)
    pdf.cell(30, 10, "Unidad", 1, 1, "C", 1)

    pdf.set_font(FONT_NAME, "", 11)
    for ing in ingredientes:
        pdf.cell(60, 8, ing["nombre"], 1, 0)
        pdf.cell(30, 8, str(ing["cantidad"]), 1, 0, "R")
        pdf.cell(30, 8, ing["unidad"], 1, 1)

    # Notas
    if notas:
        pdf.ln(10)
        pdf.set_font(FONT_NAME, "B", 12)
        pdf.cell(0, 8, "Notas:", 0, 1)
        pdf.set_font(FONT_NAME, "", 10)
        pdf.multi_cell(0, 5, notas)

    # Salida a memoria
    pdf_output_buffer = BytesIO()
    pdf_output_buffer.write(pdf.output())
    return pdf_output_buffer.getvalue()


# ---------------------------
# Exportar a DOCX
# ---------------------------
def export_to_docx(nombre_receta, ingredientes, porciones, notas):
    """Genera un DOCX con logo y pie de página."""
    doc = Document()

    # === HEADER: Logo y título ===
    if LOGO_DATA:
        LOGO_DATA.seek(0)
        logo_copy = BytesIO(LOGO_DATA.read())
        doc.add_picture(logo_copy, width=Inches(0.75))
        doc.add_heading(nombre_receta, 0)
    else:
        doc.add_heading(nombre_receta, 0)

    doc.add_paragraph(f"Porciones: {porciones}")
    doc.add_paragraph()

    # Tabla ingredientes
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Light Shading Accent 1'
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

    # === FOOTER ===
    section = doc.sections[0]
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.text = "Chef More's - Recetas Profesionales"
    footer_para.alignment = 1  # 0=izq, 1=centro, 2=derecha

    # Salida a memoria
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()



 
