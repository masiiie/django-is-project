from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Solicitud)

@admin.register(Puja)
class PujaAdmin(admin.ModelAdmin):
    date_hierarchy = 'tiempo'
    exclude = ('tiempo',)
    pass

@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    exclude = ('precio_de_subasta','tiempo_restante','ultimo_cambio')
    # filter_horizontal = ('tags',)
    pass
    
@admin.register(Cuarto)
class CuartoAdmin(admin.ModelAdmin):
    pass
    
@admin.register(SolicitudDeNegociacion)
class SolicitudDeNegociacionAdmin(admin.ModelAdmin):
    pass

@admin.register(Alquiler)
class AlquilerAdmin(admin.ModelAdmin):
    pass

@admin.register(Correo)
class CorreoAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    pass
    
@admin.register(Disponibilidad_de_cuarto)
class Disponibilidad_de_cuartoAdmin(admin.ModelAdmin):
    pass
