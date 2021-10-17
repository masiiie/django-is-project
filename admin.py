from django.contrib import admin
from .models import *

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Puja)
class PujaAdmin(admin.ModelAdmin):
    date_hierarchy = 'tiempo'
    exclude = ('tiempo',)
    pass

@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    exclude = ('precio_de_subasta','tiempo_restante','último_cambio')
    pass

@admin.register(Cuarto)
class CuartoAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Alquiler)
class AlquilerAdmin(admin.ModelAdmin):
    pass

@admin.register(Correo)
class CorreoAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Tag_de_casa)
class Tag_de_casaAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Tag_de_cuarto)
class Tag_de_cuartoAdmin(admin.ModelAdmin):
    pass

@admin.register(Disponibilidad_de_cuarto)
class Disponibilidad_de_cuartoAdmin(admin.ModelAdmin):
    pass
