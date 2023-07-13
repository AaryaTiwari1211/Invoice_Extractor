from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class PDFDocument(models.Model):
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdf_documents/')

    def __str__(self):
        return self.name