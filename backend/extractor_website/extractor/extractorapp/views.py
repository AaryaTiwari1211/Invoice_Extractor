from .models import PDFDocument
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PDFUploadForm
from django.contrib.auth.decorators import login_required
from .luxmi.luxmi_qr_code_gen import luxmi_qr_code_generator
from .luxmi.luxmi_extractor import extract_text_from_luxmi_pdf, luxmi_invoice_data, luxmi_material_info
User = get_user_model()
import random
# Disabling CSRF protection for simplicity (not recommended in production)
# @csrf_exempt

def login_view(request):
    if request.method == 'POST':
        gstin = request.POST['gstin']
        password = request.POST['password']
        user = authenticate(request, gstin=gstin, password=password)
        if user is not None:
            login(request, user)
            return redirect('file_upload')  # Redirect to your home page
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'extractorapp/login.html')
    else:
        return render(request, 'extractorapp/login.html')

def random_id(length):
    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = ''
    for i in range(0,length,2):
        id += random.choice(number)
        id += random.choice(alpha)
    return id

def signup_view(request):
    if request.method == 'POST':
        gstin = request.POST['gstin']
        password = request.POST['password']
        try:
            user = User.objects.create_user(
                gstin=gstin, password=password,)
            login(request, user)
            messages.success(request, "User created successfully.")
            return redirect('file_upload')  # Redirect to your home page
        except IntegrityError:
            messages.error(
                request, "GSTIN already exists. Please choose a different GSTIN.")
            return render(request, 'extractorapp/signup.html')

    return render(request, 'extractorapp/signup.html')

@login_required(login_url='login')
def file_upload(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # gstin = request.user.gstin
            pdf_file = request.FILES['pdf_file']
            extracted_text = extract_text_from_luxmi_pdf(pdf_file)
            print(extracted_text)
            materials = luxmi_material_info(extracted_text)
            invoice_data = luxmi_invoice_data(extracted_text, materials)
            print(invoice_data)
            output_file = luxmi_qr_code_generator(invoice_data, pdf_file)
            pdf_document = PDFDocument()
            pdf_document.name = pdf_file.name[:-4] + random_id(6) + ".pdf"
            pdf_document.pdf_file.save(
                pdf_document.name, output_file)
            return redirect('file_download', document_name=pdf_document.name)
    else:
        form = PDFUploadForm()
    return render(request, 'extractorapp/file_upload.html', {'form': form})


@login_required(login_url='login')
def file_download(request, document_name):
    try:
        # Retrieve the first matching PDF document from the database based on the document name
        pdf_document = PDFDocument.objects.filter(name=document_name).first()

        if pdf_document:
            # Create a response with the PDF file
            response = HttpResponse(
                pdf_document.pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{document_name}"'
            return response
        else:
            # Handle case when PDF document is not found
            return HttpResponse("PDF document not found.")
    except ObjectDoesNotExist:
        # Handle exception when PDF document is not found
        return HttpResponse("PDF document not found.")


# views.py
# views.py
# import logging
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# import io
# from .luxmi.luxmi_extractor import extract_text_from_luxmi_pdf, luxmi_invoice_data, luxmi_material_info, luxmi_qr_code_generator

# logger = logging.getLogger(__name__)


# class PDFProcessView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, *args, **kwargs):
#         pdf_file = request.FILES.get('pdf_file')

#         if not pdf_file:
#             return Response({'error': 'PDF file is required.'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Process the received PDF file using the Luxmi functions
#             text = extract_text_from_luxmi_pdf(pdf_file)
#             materials = luxmi_material_info(text)
#             formatted_data = luxmi_invoice_data(text, materials)
#             modified_pdf_file = luxmi_qr_code_generator(
#                 formatted_data, pdf_file)

#             # Create a BytesIO object to hold the modified PDF file
#             output_file = io.BytesIO()
#             output_file.write(modified_pdf_file.read())
#             output_file.seek(0)

#             # Return the modified PDF file as a response
#             response = Response(output_file.getvalue(
#             ), content_type='application/pdf', status=status.HTTP_200_OK)
#             response['Content-Disposition'] = 'attachment; filename="modified_pdf.pdf"'
#             return response
#         except Exception as e:
#             logger.exception(e)
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
