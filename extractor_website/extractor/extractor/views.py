from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt


# Disabling CSRF protection for simplicity (not recommended in production)
# @csrf_exempt
def file_upload(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        uploaded_file = request.FILES['pdf_file']
        # Handle the uploaded PDF file (e.g., save it to disk or process it)

    return render(request, 'file_upload.html')

def file_download(request):
    # Generate the PDF file to download (replace with your logic)
    file_path = '/path/to/your/file.pdf'
    file_name = 'file.pdf'

    # Create a response with the PDF file
    response = FileResponse(open(file_path, 'rb'),
                            content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response
