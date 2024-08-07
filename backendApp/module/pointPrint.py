from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, PageBreak, Spacer
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.fonts import addMapping

def header(canvas, doc):
    canvas.saveState()
    page_width = A4[0]
    logo_path = "static/img/logo.png"
    logo_width = 50
    logo_height = 50
    total_width = logo_width + 350
    logo_x = (page_width - total_width) / 2 + 30
    canvas.drawImage(logo_path, logo_x, A4[1] - 60, width=logo_width, height=logo_height, mask='auto')
    canvas.setFont('SimSun', 20)
    canvas.setFillColorRGB(0, 0, 0)
    text = "MediMate - 運輸站點QRCode列印"
    text_x = logo_x + logo_width + 10
    canvas.drawString(text_x, A4[1] - 40, text)
    canvas.restoreState()

def create_point_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    pdfmetrics.registerFont(TTFont('SimSun', 'static/font/SimSun.ttf'))
    addMapping('SimSun', 0, 0, 'SimSun')

    styles = getSampleStyleSheet()
    styleN = ParagraphStyle(name='Normal', fontName='SimSun', fontSize=12, textColor=colors.black, alignment=1)

    image_path = "media/3d02aad6-930d-465d-bc5c-3bd49137af89.png"
    
    text_image_pairs = [
        ["文字 1", image_path],
        ["文字 2", image_path],
        ["文字 3", image_path],
        ["文字 4", image_path],
        ["文字 5", image_path],
        ["文字 6", image_path],
        ["文字 7", image_path],
        ["文字 8", image_path]
    ]
    
    elements = []
    elements.append(Spacer(1, 20))
    
    row_data = []
    row_count = 0
    
    for idx in range(0, len(text_image_pairs), 2):
        text_1, image_1 = text_image_pairs[idx]
        if idx + 1 < len(text_image_pairs):
            text_2, image_2 = text_image_pairs[idx + 1]
        else:
            text_2, image_2 = "", ""
        
        row_data.append([Paragraph(text_1, styleN), Paragraph(text_2, styleN)])
        row_data.append([Image(image_1, width=1.5*inch, height=1.5*inch), 
                         Image(image_2, width=1.5*inch, height=1.5*inch) if image_2 else ""])
        row_count += 1

        if row_count == 3:
            table = Table(row_data, colWidths=[2.5*inch]*2, rowHeights=[0.5*inch, 2*inch]*3)
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
            ]))
            elements.append(table)
            elements.append(PageBreak())
            row_data = []
            row_count = 0
    
    if row_data:
        row_heights = [0.5*inch if i % 2 == 0 else 2*inch for i in range(len(row_data))]
        table = Table(row_data, colWidths=[2.5*inch]*2, rowHeights=row_heights)
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        elements.append(table)
    
    doc.build(elements, onFirstPage=header, onLaterPages=header)

create_point_pdf("output_table1.pdf")
