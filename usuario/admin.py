from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
from django.utils.translation import gettext, gettext_lazy as _
# from django.contrib import admin
# from django.contrib.auth.models import Group

class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'cNombres', 'turno', 'is_staff','is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Suscription dates'), {'fields': ('cNombres', 'turno','is_active', 'is_staff', 'is_superuser')}),
    )
    list_filter = ()

admin.site.register(Usuario, UsuarioAdmin)