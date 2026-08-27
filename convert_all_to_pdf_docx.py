import os
import sys
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

sys.stdout.reconfigure(encoding='utf-8')

md_files = [
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\08\01. Unidad 1 Fundamentos de BI y Obtención de Datos\Desafío_1_Presentacion_y_Conexion_SmartRetail.md",
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\08\02. Unidad 2 Preparación, Modelado y DAX\Desafío_2_Modelado_y_DAX_SmartRetail.md",
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\08\03. Unidad 3 Visualización, Reportes y DashboardsCarpeta\Prueba_3_Dashboard_Ejecutivo_SmartRetail.md",
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\09\01. Unidad 1 Elementos y técnicas de la narrativa de datosCarpeta\Desafío_Narrativa_FastDelivery.md",
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\09\02. Unidad 2 Representación de datos\01_Estructura_Narrativa_TechCorp.md",
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\09\02. Unidad 2 Representación de datos\02_Presentacion_Transformacion_Digital.md",
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\09\02. Unidad 2 Representación de datos\03_Storyboard_y_Script_Ejecutivo.md",
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\10\01. Unidad 1 Portafolio de productosCarpeta\Desafío_Portafolio_Virtual_Planificacion.md",
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\10\02. Unidad 2 Portafolio de producto digitalCarpeta\Prueba_Portafolio_Producto_Digital.md",
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\11. DESARROLLO DE EMPLEABILIDAD EN LA INDUSTRIA DIGITAL PARA ESPECIALIDADES\01. Unidad 1 Desarrollo de empleabilidad en la industria digitalCarpeta\Prueba_QuickShop_Informe_Ejecutivo.md",
    r"c:\Users\VN\Downloads\ANALISIS DE DATOS\11. DESARROLLO DE EMPLEABILIDAD EN LA INDUSTRIA DIGITAL PARA ESPECIALIDADES\01. Unidad 1 Desarrollo de empleabilidad en la industria digitalCarpeta\Prueba_Elevator_Pitch.md"
]

def clean_md_tags(text):
    # Escape XML entities for ReportLab
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Convert markdown bold **text** to ReportLab <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Convert markdown italic *text* to ReportLab <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Convert markdown code `text` to ReportLab <font name="Courier">text</font>
    text = re.sub(r'`(.*?)`', r'<font name="Courier" size="9" color="#1A202C">\1</font>', text)
    return text

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(612 - 54, 36, page_text)
        self.drawString(54, 36, "Análisis de Datos - Documento Oficial de Entrega")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 612 - 54, 48)
        self.restoreState()

def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1F497D"),
        spaceAfter=12
    )
    
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=10,
        spaceAfter=6
    )
    
    h3_style = ParagraphStyle(
        'DocH3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        alignment=4, # Justified
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        'DocCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A202C"),
        backColor=colors.HexColor("#F7FAFC"),
        borderColor=colors.HexColor("#E2E8F0"),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=8
    )

    story = []
    in_code = False
    code_lines = []
    
    for line in lines:
        raw_line = line
        line = line.strip()
        
        if line.startswith("```"):
            if in_code:
                in_code = False
                c_formatted = "<br/>".join([c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(" ", "&nbsp;") for c in code_lines])
                story.append(Paragraph(c_formatted, code_style))
                code_lines = []
            else:
                in_code = True
            continue
            
        if in_code:
            code_lines.append(raw_line.rstrip())
            continue
            
        if not line or line.startswith("|") or "---" in line and not line.startswith("#"):
            continue
            
        if line.startswith("# "):
            story.append(Paragraph(clean_md_tags(line[2:]), title_style))
            story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1F497D"), spaceAfter=10))
        elif line.startswith("## "):
            story.append(Paragraph(clean_md_tags(line[3:]), h2_style))
        elif line.startswith("### "):
            story.append(Paragraph(clean_md_tags(line[4:]), h3_style))
        elif line.startswith("- ") or line.startswith("* "):
            story.append(Paragraph("• " + clean_md_tags(line[2:]), body_style))
        elif line.startswith("> "):
            story.append(Paragraph("<i>" + clean_md_tags(line[2:]) + "</i>", body_style))
        else:
            story.append(Paragraph(clean_md_tags(line), body_style))
            
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {pdf_path}")

for md in md_files:
    if os.path.exists(md):
        pdf_path = os.path.splitext(md)[0] + ".pdf"
        try:
            md_to_pdf(md, pdf_path)
        except Exception as e:
            print(f"Error PDF for {md}: {e}")
