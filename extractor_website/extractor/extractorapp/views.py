from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import datetime
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PDFUploadForm
from django.contrib.auth.decorators import login_required
import io
import re
import PyPDF2
from .qr_code_gen import qr_code_generator
from .extractor import extract_text_from_pdf, extract_invoice_data, extract_material_info
import tempfile
import os
import shutil


# Disabling CSRF protection for simplicity (not recommended in production)
# @csrf_exempt
from django.http import HttpResponse


from .models import PDFDocument


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('file_upload')  # Redirect to your home page
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'extractorapp/login.html')
    else:
        return render(request, 'extractorapp/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        try:
            user = User.objects.create_user(
                username=username, password=password, email=email)
            login(request, user)
            messages.success(request, "User created successfully.")
            return redirect('file_upload')  # Redirect to your home page
        except IntegrityError:
            messages.error(
                request, "Username already exists. Please choose a different username.")
            return render(request, 'extractorapp/signup.html')

    return render(request, 'extractorapp/signup.html')


@login_required(login_url='login')
def file_upload(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            extracted_text = extract_text_from_pdf(pdf_file)
            materials = extract_material_info(extracted_text)
            invoice_data = extract_invoice_data(extracted_text, materials)
            output_file = qr_code_generator(invoice_data, pdf_file)
            pdf_document = PDFDocument()
            pdf_document.name = pdf_file.name
            pdf_document.pdf_file.save(
                pdf_file.name, output_file)  # Save the PDF content
            # Redirect to the download page
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
