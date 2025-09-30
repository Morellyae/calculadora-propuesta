from fpdf import FPDF
import os

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        # Registrar fuente DejaVu para UTF-8
        font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
        self.add_font("DejaVu", "", font_path, uni=True)
        self.set_font("DejaVu", "", 12)

    def header(self):
        # Logo
        if os.path.exists("logo.png"):
            self.image("logo.png", 10, 8, 25)
        self.set_font("DejaVu", "", 12)
        self.cell(0, 10, "Sistema de Recetas – Chef More's", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, "© Chef More's – Sistema de Recetas", 0, 0, "C")

def export_to_pdf(receta, data, porcion, nota):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, f"Receta: {receta}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 10, f"Porción: {porcion}", ln=True)

    pdf.ln(5)
    pdf.multi_cell(0, 10, "Ingredientes:")
    for item in data:
        pdf.multi_cell(0, 10, f"- {item}")

    if nota:
        pdf.ln(5)
        pdf.multi_cell(0, 10, f"Nota: {nota}")

    # Exportar como bytes (para Streamlit)
    return pdf.output(dest="S").encode("latin-1", "replace")
