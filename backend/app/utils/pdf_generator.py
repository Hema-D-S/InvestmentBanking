from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_pdf_report(title: str, summary: str) -> bytes:
    """
    Generate a simple PDF report with a title and summary.
    :param title: Title of the report
    :param summary: Summary text
    :return: PDF file as bytes
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 20)
    c.drawString(72, height - 72, title)
    c.setFont("Helvetica", 12)
    text_object = c.beginText(72, height - 100)
    for line in summary.splitlines():
        text_object.textLine(line)
    c.drawText(text_object)
    c.showPage()
    c.save()
    buf.seek(0)
    return buf.getvalue()
