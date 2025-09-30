# Este archivo contiene las funciones para exportar la receta a PDF (usando fpdf) y DOCX (usando python-docx).
# Ambas funciones devuelven el archivo como bytes en memoria, lo cual es necesario para st.download_button en Streamlit.

from fpdf import FPDF
from docx import Document
from docx.shared import Inches
from io import BytesIO

# Nueva importación para manejar la carga del logo
try:
    # Intenta cargar el logo una sola vez al inicio en memoria (BytesIO)
    with open("logo.png", "rb") as f:
        LOGO_DATA = BytesIO(f.read())
except FileNotFoundError:
    # Si falla, establecemos LOGO_DATA a None para que las funciones lo ignoren
    LOGO_DATA = None
    print("Advertencia: 'logo.png' no encontrado. La exportación funcionará sin logo.")


# Exportar a PDF (usa fpdf, devuelve bytes)
def export_to_pdf(nombre_receta, ingredientes, porciones, notas):
    """Genera un archivo PDF con la receta, incluyendo el logo, y lo devuelve como objeto Bytes."""
    # Usamos FPDF en modo vertical, con unidad milímetros, y formato A4
    pdf = FPDF(orientation='P', unit='mm', format='A4') 
    
    # Usamos 'Times', una fuente interna de fpdf que está garantizada para funcionar 
    # y soporta acentos en español.
    FONT_NAME = 'Times'
    pdf.add_page()
    
    # === HEADER: Logo y Título ===
    if LOGO_DATA:
        # Volvemos al inicio del buffer para que pueda leerse de nuevo en cada llamada
        LOGO_DATA.seek(0) 
        # Añadir la imagen al PDF (x, y, ancho)
        pdf.image(LOGO_DATA, x=10, y=10, w=30)
        # Posicionar el título a la derecha del logo
        pdf.set_xy(45, 15)
        pdf.set_font(FONT_NAME, "B", 18)
        pdf.cell(0, 10, nombre_receta, 0, 1, "L")
        pdf.ln(5) # Espacio después del título
    else:
        pdf.ln(10) # Si no hay logo, dejamos espacio
        pdf.set_font(FONT_NAME, "B", 16) 
        pdf.cell(0, 12, nombre_receta, 0, 1, "C") # Título centrado
    
    pdf.set_font(FONT_NAME, "", 12)
    pdf.cell(0, 8, f"Porciones: {porciones}", 0, 1)

    pdf.ln(5) # Salto de línea

    # Encabezados de la tabla de ingredientes
    pdf.set_font(FONT_NAME, "B", 12)
    pdf.set_fill_color(200, 220, 255) # Color de fondo
    pdf.cell(60, 10, "Ingrediente", 1, 0, "C", 1)
    pdf.cell(30, 10, "Cantidad", 1, 0, "C", 1)
    pdf.cell(30, 10, "Unidad", 1, 1, "C", 1) # 1 al final para salto de línea
    
    # Contenido de la tabla
    pdf.set_font(FONT_NAME, "", 11)
    for ing in ingredientes:
        # Aseguramos que la celda se dibuje incluso si los datos son strings largos
        pdf.cell(60, 8, ing["nombre"], 1, 0)
        pdf.cell(30, 8, str(ing["cantidad"]), 1, 0, "R") # Alineación a la derecha para números
        pdf.cell(30, 8, ing["unidad"], 1, 1)

    # Notas
    if notas:
        pdf.ln(10)
        pdf.set_font(FONT_NAME, "B", 12)
        pdf.cell(0, 8, "Notas:", 0, 1)
        pdf.set_font(FONT_NAME, "", 10)
        # multi_cell permite saltos de línea automáticos
        pdf.multi_cell(0, 5, notas)
        
    # Usar BytesIO para forzar la salida a bytes (más robusto para Streamlit)
    pdf_output_buffer = BytesIO()
    pdf_output_buffer.write(pdf.output()) 
    
    # Devolvemos el contenido del buffer como bytes
    return pdf_output_buffer.getvalue()

# Exportar a DOCX (usa python-docx, devuelve bytes)
def export_to_docx(nombre_receta, ingredientes, porciones, notas):
    """Genera un archivo DOCX con la receta, incluyendo el logo, y lo devuelve como objeto Bytes."""
    doc = Document()
    
    # === HEADER: Logo y Título ===
    if LOGO_DATA:
        # Volvemos al inicio del buffer para que python-docx lo pueda leer
        LOGO_DATA.seek(0)
        
        # Añadir logo
        # Usamos una copia del BytesIO para evitar conflictos de lectura/escritura si se llama muchas veces
        logo_copy = BytesIO(LOGO_DATA.read())
        doc.add_picture(logo_copy, width=Inches(0.75))
        
        # Después del logo, añadir el título
        doc.add_heading(nombre_receta, 0)
    else:
        # Si no hay logo, solo añadir el título
        doc.add_heading(nombre_receta, 0)

    doc.add_paragraph(f"Porciones: {porciones}")
    doc.add_paragraph() # Salto de línea

    # Ingredientes
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Light Shading Accent 1' # Estilo de tabla
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

    # Guardar en memoria (BytesIO) y devolver los bytes (ESENCIAL para Streamlit)
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()




   


 


 
