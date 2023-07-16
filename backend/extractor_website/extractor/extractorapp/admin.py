from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import PDFDocument


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('gstin', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('gstin', 'password')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('gstin', 'password1', 'password2', 'is_staff'),
        }),
    )
    search_fields = ('gstin',)
    ordering = ('gstin',)
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(PDFDocument)
