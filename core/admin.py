from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Cliente

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Informações adicionais', {'fields': ('cargo', 'empresa')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações adicionais', {'fields': ('cargo', 'empresa')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Cliente)