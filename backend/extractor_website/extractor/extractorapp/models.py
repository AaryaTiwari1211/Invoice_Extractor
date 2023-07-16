from django.contrib.auth.models import AbstractBaseUser, BaseUserManager , PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, gstin, password=None, **extra_fields):
        if not gstin:
            raise ValueError('GSTIN must be set')

        user = self.model(gstin=gstin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, gstin, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(gstin, password, **extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    gstin = models.CharField(max_length=15, unique=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'gstin'

    def __str__(self):
        return self.gstin

    def has_perm(self, perm, obj=None):
        # Override the default has_perm method to customize permissions
        return self.is_superuser

    def has_module_perms(self, app_label):
        # Override the default has_module_perms method to allow access to all modules
        return self.is_superuser


class PDFDocument(models.Model):
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdf_documents/')

    def __str__(self):
        return self.name
