import re
import PyPDF2
from .qr_code_gen import qr_code_generator

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    print(text)
    return text


def extract_invoice_data(text,materials):
    # Extract PO No
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

    # Extract Invoice No
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

    # Extract Vehicle No
    vehicle_no_match = re.search(
        r"Vehicle No.\s*:\s*([A-Z]{2}\d{1,2}\s?[A-Z]{1,3}\s?\d{1,4})", text)
    vehicle_no = vehicle_no_match.group(1) if vehicle_no_match else ""
    print(vehicle_no)

    # Set fixed values
    driver_name = ""
    vehicle_type = ""
    transporter_name = ""

    # Extract Material Codes, Quantities, Batch Numbers, Manufacturing Dates, and Expiry Dates
    # materials = extract_material_info(text)

    # Format the extracted information
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


def extract_material_info(text):
    material_info = []

    # Find the start and end indices of the material information section
    start_index = text.find("S.N.Description of Goods")
    end_index = text.find("Rupees")

    # Extract the material information
    material_section = text[start_index:end_index].strip()

    # Split the material section into lines
    lines = material_section.split("\n")

    # Process each line to extract material data
    for line in lines[2:]:  # Skip the header line
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

    # Print the formatted material info
    for material in material_info:
        print("Material Code:", material['code'])
        print("Quantity:", material['qty'])
        print()

    return material_info


# pdf_path = "files/HARIDWAR BILL.pdf"

# extracted_text = extract_text_from_pdf(
#     r"files\HARIDWAR BILL.pdf")
# extract_invoice_data(extracted_text)
# invoice_data = extract_invoice_data(extracted_text)
# print(invoice_data)
# qr_code_generator(invoice_data, pdf_path)

# formatted_data2 = extract_material_info(extracted_text)
