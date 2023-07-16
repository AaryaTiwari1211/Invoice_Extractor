import pdfplumber
import re
import PyPDF2
from .rockman_qrcode import rockman_qr_code_generator
from pdfminer.high_level import extract_text


def extract_text_from_rockman_pdf(file):
    with pdfplumber.open(file) as pdf:
        extracted_text = ""
        for page in pdf.pages:
            extracted_text += page.extract_text()
    print(extracted_text)
    return extracted_text


def rockman_invoice_data(text):
    invoice_no_pattern = r"Invoice No\.\n(.+)"
    part_no_pattern = r"\b\d{10}\b"
    dated_pattern = r"Dated\n(\d{2}-[a-zA-Z]{3}-\d{2})"
    quantity_pattern = r"\d+,\d+\s*Nos"
    buyer_order_no_pattern = r"Buyer’s Order No\.\n(.+)"
    hsn_sac_pattern = r"HSN/SAC\n(\d+)"
    invoice_no_match = re.search(invoice_no_pattern, text)
    motor_vehicle_no_pattern = r"Motor Vehicle No\.\n(.+)"
    dispatched_through_pattern = r"Dispatched through\n(.+)"
    buyer_gstin_pattern = r"GSTIN/UIN\n\s*:\s*(\w+)[\s\S]*?State Name\s*:\s*([\w\s]+)\s*,\s*Code\s*:\s*(\d+)"
    seller_state_pattern = r"E.R.Auto Pvt\. Ltd\.[\s\S]*?State Name\s*:\s*([A-Za-z\s]+)\s*,\s*Code\s*:\s*(\d+)"

    motor_vehicle_no_match = re.search(motor_vehicle_no_pattern, text)
    if motor_vehicle_no_match:
        motor_vehicle_no = motor_vehicle_no_match.group(1)
        print("Motor Vehicle No.: ", motor_vehicle_no)
    else:
        motor_vehicle_no = ""

    dispatched_through_match = re.search(dispatched_through_pattern, text)
    if dispatched_through_match:
        dispatched_through = dispatched_through_match.group(1)
        print("Dispatched through: ", dispatched_through)
    else:
        dispatched_through = ""

    if invoice_no_match:
        invoice_no = invoice_no_match.group(1)
        print("Invoice No.: ", invoice_no)
    else:
        invoice_no = ""

    dated_match = re.search(dated_pattern, text)
    if dated_match:
        dated = dated_match.group(1)
        print("Dated: ", dated)
    else:
        dated = ""

    quantity_match = re.search(quantity_pattern, text)
    if quantity_match:
        quantity = quantity_match.group()
        quantity = quantity.replace(",", "")
        quantity = quantity.replace(" Nos", "")
        print("Quantity: ", quantity)
    else:
        quantity = ""

    part_no_match = re.findall(part_no_pattern, text)

    if part_no_match:
        part_number = part_no_match[1]
        print("Part Number:", part_number)
    else:
        print("Part Number not found.")

    buyer_order_no_match = re.search(buyer_order_no_pattern, text)
    if buyer_order_no_match:
        buyer_order_no = buyer_order_no_match.group(1)
        print("Buyer's Order No.: ", buyer_order_no)
    else:
        buyer_order_no = ""

    final = f"{invoice_no}|{dated}|{quantity}|{part_number}|{buyer_order_no}|{motor_vehicle_no}|{dispatched_through}|"
    return final
