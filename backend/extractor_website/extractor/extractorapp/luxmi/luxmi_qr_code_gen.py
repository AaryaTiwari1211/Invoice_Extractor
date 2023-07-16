import io
import pyqrcode
import matplotlib.pyplot as plt
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def luxmi_qr_code_generator(qr_text, pdf_file):
    url = 'http://64.227.156.31/'
    qr_txt = qr_text

    lst = qr_txt.split('\n')
    invno = str(qr_txt.split('|')[1]) + ".png"
    qrtxt = ''
    for v in lst:
        if qrtxt:
            qrtxt = '{0}\n{1}'.format(qrtxt, v)
        else:
            qrtxt = '{0}'.format(v)

    # Generate QR code
    url = pyqrcode.create(qrtxt)
    url.png(invno, scale=6)

    # Create a PDF with the QR code image
    c = canvas.Canvas("qr_code.pdf", pagesize=letter)
    # parameters are: image, x-pos, y-pos, width and height
    c.drawImage(invno, 60, 300, width=60, height=60)
    c.save()

    # Merge the QR code PDF with the original PDF
    with open("qr_code.pdf", "rb") as qr_code_file:
        original = PyPDF2.PdfReader(pdf_file)
        qr_code = PyPDF2.PdfReader(qr_code_file)

        original_page = original.pages[0]
        qr_code_page = qr_code.pages[0]

        original_page.merge_page(qr_code_page)

        writer = PyPDF2.PdfWriter()
        writer.add_page(original_page)

        # Create a BytesIO object to hold the merged PDF file
        output_file = io.BytesIO()
        writer.write(output_file)

    # Reset the file position to the beginning
    output_file.seek(0)

    return output_file
