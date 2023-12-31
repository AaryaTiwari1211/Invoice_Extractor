import re
import PyPDF2
from .luxmi_qr_code_gen import luxmi_qr_code_generator

# def extract_text_from_luxmi_pdf(file):
#     # Wrap the PDF file with io.TextIOWrapper and specify the encoding and error handling
#     with io.TextIOWrapper(file, encoding='latin-1', errors='replace') as pdf_file:
#         reader = PyPDF2.PdfReader(pdf_file)
#         text = ''
#         for page in reader.pages:
#             text += page.extract_text()
#     print(text)
#     return text


# def extract_text_from_luxmi_pdf(file):
#     # Wrap the PDF file with io.TextIOWrapper to specify the encoding and error handling
#     reader = PyPDF2.PdfReader(file)
#     text = ''
#     for page in reader.pages:
#         text += page.extract_text()
#     print(text)
#     return text
import io
import chardet


def extract_text_from_luxmi_pdf(file):
    # Read the PDF content into memory
    pdf_data = file.read()
    file.seek(0)

    # Detect the encoding of the PDF content
    result = chardet.detect(pdf_data)
    encoding = result['encoding']

    try:
        # Decode the PDF content using the detected encoding
        decoded_pdf_data = pdf_data.decode(encoding, errors='replace')

        reader = PyPDF2.PdfReader(io.BytesIO(
            decoded_pdf_data.encode('latin-1')))
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        print(text)
        return text
    except UnicodeDecodeError:
        # If decoding fails, handle the error accordingly
        print("UnicodeDecodeError: Failed to extract text from the PDF.")
        return ""


def luxmi_invoice_data(text, materials):
    po_no_match = re.search(r"PO NO.\s*:\s*([\w\d]+)", text)
    po_no = po_no_match.group(1) if po_no_match else ""

    m_code_match = re.search(r"\(([^)]+)\)", text)
    m_code = m_code_match.group(1) if m_code_match else ""

    manuf_date_match = re.search(r"Manufacturing\s*Date\s*:\s*([\d-]+)", text)
    manuf_date = manuf_date_match.group(1) if manuf_date_match else ""

    expiry_match = re.search(r"Expiry\s*Date\s*:\s*([\d-]+)", text)
    expiry_date = expiry_match.group(1) if expiry_match else ""

    batch_no_match = re.search(r"Batch\s*No.\s*:\s*([\d-]+)", text)
    batch_no = batch_no_match.group(1) if batch_no_match else ""

    invoice_no_match = re.search(r"Invoice No.\s*:\s*([\w\d]+)", text)
    invoice_no = invoice_no_match.group(1) if invoice_no_match else ""

    invoice_date_match = re.search(r"\d{2}-\d{2}-\d{4}", text)
    if invoice_date_match:
        invoice_date = invoice_date_match.group(0)
        invoice_date = invoice_date.replace("-", ".")
    else:
        invoice_date = ""

    supplier_gst_match = re.search(r"GSTIN\s*:\s*([\w\d]+)", text)
    supplier_gst = supplier_gst_match.group(1) if supplier_gst_match else ""

    buyer_gst_match = re.search(r"GSTIN \/ UIN\s*:\s*([\w\d]+)", text)
    buyer_gst = buyer_gst_match.group(1) if buyer_gst_match else ""

    vehicle_no_match = re.search(
        r"Vehicle No.\s*:\s*([A-Z]{2}\d{1,2}\s?[A-Z]{1,3}\s?\d{1,4})", text)
    vehicle_no = vehicle_no_match.group(1) if vehicle_no_match else ""
    print(vehicle_no)

    driver_name = ""
    vehicle_type = ""
    transporter_name = ""

    formatted_text = f"{po_no}|{invoice_no}|{invoice_date}|{vehicle_no}|{driver_name}|{vehicle_type}|{transporter_name}|"
    material_info = ""
    for material in materials:
        material_info += f"{material['code']}|{material['qty']}|{batch_no}|{manuf_date}|{expiry_date}|"

    print("PO No:", po_no)
    print("Vehicle Type: ", vehicle_type)
    print("Invoice No:", invoice_no)
    print("Buyer GSTIN: ", buyer_gst)
    print("Supplier GSTIN: ", supplier_gst)
    print("\n")

    return formatted_text + material_info


def luxmi_material_info(text):
    material_info = []

    start_index = text.find("S.N.Description of Goods")
    end_index = text.find("Rupees")

    material_section = text[start_index:end_index].strip()

    lines = material_section.split("\n")

    for line in lines[2:]:
        material_pattern = r"\((P.NO.\d{5}-\d{3}-\d{4})\)|\((\d{5}-[A-Z]{3}-\d{4})\)"
        material_code_match = re.search(material_pattern, line)
        print(material_code_match)
        quantity_match = re.search(r"(\d+)X(\d+)", line)

        if material_code_match and quantity_match:
            material_code = material_code_match.group(
                1) or material_code_match.group(2)
            quantity = int(quantity_match.group(1)) * \
                int(quantity_match.group(2))
            material_info.append({
                "code": material_code,
                "qty": quantity
            })

    for material in material_info:
        print("Material Code:", material['code'])
        print("Quantity:", material['qty'])
        print()

    return material_info
