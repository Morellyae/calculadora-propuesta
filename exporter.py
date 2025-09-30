import os
from fpdf import FPDF

class PDF(FPDF):
    def __init__(self, logo_path="logo.png"):
        super().__init__()
        # Registrar fuente DejaVu (soporta UTF-8: ñ, tildes, símbolos)
        font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
        self.add_font("DejaVu", "", font_path, uni=True)
        self.set_font("DejaVu", "", 12)
        self.logo_path = logo_path

    def header(self):
        # Logo
        if os.path.exists(self.logo_path):
            self.image(self.logo_path, 10, 8, 25)
        # Encabezado
        self.set_font("DejaVu", "", 12)
        self.cell(0, 10, "Sistema de Recetas – Chef More's", 0, 1, "C")
        self.ln(5)

    def footer(self):
        # Posicionar desde el borde inferior
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, "© Chef More's – Sistema de Recetas", 0, 0, "C")

def export_to_pdf(receta, data, porcion, nota):
    pdf = PDF()
    pdf.add_page()

    # Título
    pdf.set_font("DejaVu", "", 16)
    pdf.cell(0, 10, f"Receta: {receta}", ln=True, align="C")

    # Porciones
    pdf.set_font("DejaVu", "", 12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Porción: {porcion}", ln=True)

    # Ingredientes
    pdf.ln(5)
    pdf.set_font("DejaVu", "", 13)
    pdf.cell(0, 10, "Ingredientes:", ln=True)
    pdf.set_font("DejaVu", "", 12)
    for item in data:
        pdf.multi_cell(0, 8, f"- {item}")

    # Nota opcional
    if nota:
        pdf.ln(5)
        pdf.set_font("DejaVu", "I", 11)
        pdf.multi_cell(0, 8, f"Nota: {nota}")

    # Exportar como bytes (UTF-8 seguro en fpdf2)
    return pdf.output(dest="S").encode("latin-1", "replace")


