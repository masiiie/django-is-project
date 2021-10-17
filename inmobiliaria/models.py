from django.db import models
import django.utils.timezone as tz
from django.contrib.auth.models import AbstractUser, Group, User
from django.contrib.auth import get_user_model
import datetime

ubicationChoice=(
    ('CI','Ciudad'),
    ('CP','Campo'),
    ('PL','Playa'),
    ('PE','Periferia'),
)

provinceChoice = (
    ("HA","La Habana"),
    ("MA","Matanzas"),
    ("PR","Pinar del Río"),
    ("VC","Villa Clara"),
    ("CI","Cienfuegos"),
    ("SE","Sancti Espíritus"),
    ("MY","Mayabeque"),
    ("AR","Artemisa"),
    ("TU","Las Tunas"),
    ("CA","Camaguey"),
    ("HO","Holguín"),
    ("GR","Granma"),
    ("SC","Santiago de Cuba"),
    ("GU","Guantánamo"),
    ("IJ","Isla de la Juventud"),
    )

typeChoices = (
    ("CL","Cliente"),
    ("AD","Administrador"),
    ("GE","Gerente"),
    )

mailChoices = (
    ("PE","Pendiente"),
    ("AS","Analizándose"),
    ("A","Analizado"),
    )

actChoice = (
    ("VE","Vender"),
    ("CM","Comprar"),
    ("SP","Solicitar Publicacion"),
    )

sellChoices = (
    ("Venta","Venta"),
    ("Renta linear","Renta linear"),
    ("Renta de cuartos","Renta de cuartos"),
    )

negChoices = (
    ("Compra","Compra"),
    ("Renta","Renta"),
    ("Renta de cuarto","Renta de cuarto"),
    )

tagChoice = (
    ("CU","Tag de Cuarto"),
    ("CA","Tag de Casa"),
    )

provinces = dict(provinceChoice)
sell_action = dict(sellChoices)
ubication = dict(ubicationChoice)

# class Publicador(models.Model):
#     user = models.OneToOneField(models.OneToOneField(User, on_delete=models.CASCADE)

class Lugar(models.Model):
    nombre = models.CharField(max_length=30, default = "Hogar",blank = True)
    perito = models.ForeignKey(get_user_model(), on_delete = models.CASCADE,related_name = 'lugar_insertado')
    agente = models.ForeignKey(get_user_model(), on_delete = models.CASCADE,related_name = 'lugar_asignado')
    propietario = models.ForeignKey(get_user_model(), on_delete = models.CASCADE,related_name = 'tu_lugar')
    disponible = models.BooleanField(default = True)

    calle_principal = models.CharField(default = "calle principal", max_length = 60, blank = False,verbose_name = "calle principal")
    calle_secundaria = models.CharField(default = "calle secundaria" ,max_length = 60, blank = False,verbose_name = "calle secundaria")
    calle_secundaria_opcional = models.CharField(max_length = 60, blank = True,verbose_name = "calle secundaria (opcional)")
    ubicacion = models.CharField(choices=ubicationChoice,max_length=2)
    descripcion = models.TextField(blank = True)

    lat = models.CharField(default = "",max_length = 25)
    lng = models.CharField(default = "",max_length = 25)

    foto1 = models.ImageField(upload_to = "imagen_casa")
    foto2 = models.ImageField(upload_to = "imagen_casa")
    foto3 = models.ImageField(upload_to = "imagen_casa")

    cantidad_de_bannos = models.IntegerField(default = 1,verbose_name = "cantidad de bannos")
    cantidad_de_cuartos = models.IntegerField(default = 1,verbose_name = "cantidad de cuartos")
    cantidad_de_plantas = models.IntegerField(default = 1,verbose_name = "cantidad de plantas")
    numero_de_vivienda = models.IntegerField(default = 202,verbose_name = "numero de vivienda")
    precio_de_alquiler = models.IntegerField(default = 100,verbose_name = "precio de alquiler")
    precio_de_venta = models.IntegerField(default = 10000,verbose_name = "precio de venta")
    precio_de_subasta = models.IntegerField(default = 10000,verbose_name = "precio de subasta")
    #tiempo_restante = models.IntegerField(default = 1000,verbose_name = "tiempo restante")
    fecha_finalizacion = models.DateField(auto_now_add = False)

    evaluacion = models.IntegerField(default = 1)

    tiene_calle_secundaria_opcional = models.BooleanField(default = True,verbose_name = "tiene calle secundaria opcional")
    municipio = models.CharField(max_length = 21, default = "10 de Octubre")
    provincia = models.CharField(max_length = 21, choices = provinceChoice, default = "LH") 
    venta_o_renta = models.CharField(max_length = 20 , choices = sellChoices, default = "Venta",verbose_name = "venta o renta")
    subastable = models.BooleanField(default = True)
    chequeado = models.BooleanField(default = False)
    tags = models.ManyToManyField('Tag')
    
    ultimo_cambio = models.DateField(auto_now_add = True)

    def __str__(self):
        if self.nombre:
            return self.nombre
        if self.tiene_calle_secundaria_opcional:
            return str("calle %s, No. %d Entre %s, %s, %s" %(self.calle_principal,self.numero_de_vivienda,self.calle_secundaria,provinces[self.provincia],self.municipio))
        return str("calle %s, No. %d Entre %s y %s, %s, %s" %(self.calle_principal,self.numero_de_vivienda,self.calle_secundaria,self.calle_secundaria_opcional,provinces[self.provincia],self.municipio))

    class Meta:
        managed = True
        unique_together = (('calle_principal','calle_secundaria','calle_secundaria_opcional','numero_de_vivienda'),)
        verbose_name_plural = "Lugares"
        permissions = (
                    ("view_profile","can see personal profile"),
                    ("view_data","can see the data"),
                    )

class Cuarto(models.Model):
    casa = models.ForeignKey('Lugar', on_delete = models.CASCADE)
    cantidad_de_camas = models.IntegerField(default = 1,verbose_name = 'cantidad de camas')
    banno_compartido = models.BooleanField(default = False,verbose_name = 'banno compartido')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return str("%s--%d" %(str(self.casa),self.id))

    class Meta:
        managed = True
        verbose_name_plural = "Cuartos"

class Alquiler(models.Model):
    casa = models.ForeignKey('Lugar', on_delete = models.CASCADE)
    es_linear = models.BooleanField(default = False)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()

    class Meta:
        unique_together = (('casa','fecha_inicio','fecha_final'),)
        verbose_name_plural = "Alquileres"
        pass

class Disponibilidad_de_cuarto(models.Model):
    cuarto = models.ForeignKey('Cuarto', on_delete = models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()

    def __str__(self):
        return str("%s -> %s, habitacion %d" %(str(self.fecha_inicio),str(self.fecha_final),self.cuarto.id))

    class Meta:
        unique_together = (('cuarto','fecha_inicio','fecha_final'),)
        verbose_name_plural = "Disponibilidad de cuartos"
        pass

class Correo(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    texto = models.TextField(default = "")
    estado = models.CharField(choices = mailChoices, default = "PE", max_length = 2)
    fecha_tiempo = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.usuario +" "+ str(self.fecha_tiempo)

    class Meta:
        verbose_name_plural = "Correos"

class Log(models.Model):
    nombre = models.ForeignKey('Lugar', on_delete = models.CASCADE)
    usuario = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    accion = models.CharField(choices = actChoice,default = "VE",max_length = 2)
    texto = models.TextField(default = "")
    tiempo = models.DateField(auto_now_add = True, blank = False)

    class Meta:
        verbose_name_plural = "Logs"
    
class Puja(models.Model):
    lugar = models.ForeignKey('Lugar', on_delete = models.CASCADE)
    tamanno_de_puja = models.IntegerField()
    usuario = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    tiempo = models.DateTimeField(auto_now_add = True, blank = False)

    def __str__(self):
        return self.usuario.username + " : " + str(self.tiempo)

    class Meta:
        unique_together = (('lugar','tamanno_de_puja','usuario','tiempo'),)
        verbose_name_plural = "Pujas"

class Tag(models.Model):
    nombre = models.CharField(max_length = 20,default = "algo")
    tipo = models.CharField(choices = tagChoice,default = "CA",max_length = 2)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

class Solicitud(models.Model):
    nombre_de_publicacion = models.CharField(max_length = 30,blank = True,verbose_name = 'nombre de publicación',unique = True)
    usuario = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    venta_o_renta = models.CharField(max_length = 10 , choices = sellChoices, default = "Venta",verbose_name = "venta o renta")
    perito = models.ForeignKey(get_user_model(), on_delete = models.CASCADE,related_name = 'solicitud_asignado',null = True,blank = True)
    
    calle_principal = models.CharField(default = "calle principal", max_length = 60, blank = False,verbose_name = "calle principal")
    calle_secundaria = models.CharField(default = "calle secundaria" ,max_length = 60, blank = False,verbose_name = "calle secundaria")
    calle_secundaria_opcional = models.CharField(max_length = 60, blank = True,verbose_name = "calle secundaria opcional")
    tiene_calle_secundaria_opcional = models.BooleanField(default = True,verbose_name = "tiene calle secundaria opcional")
    numero_de_vivienda = models.IntegerField(default = 202,verbose_name = "numero de vivienda")
    municipio = models.CharField(max_length = 21, default = "10 de Octubre")
    provincia = models.CharField(max_length = 21, choices = provinceChoice, default = "LH")
    chequeado = models.BooleanField(default = False)
    tiempo = models.DateTimeField(auto_now_add = True, blank = False)
    lat = models.CharField(default = "",max_length = 25)
    lng = models.CharField(default = "",max_length = 25)

    def __str__(self):
        if self.nombre_de_publicacion:
            return self.nombre_de_publicacion
        return "Solicitud: " + self.__adrs__()

    def __adrs__(self):
        return self.calle_principal +" "+ str(self.numero_de_vivienda) +", "+ provinces[self.provincia]
        
    class Meta:
        verbose_name = "Solicitud de publicacion"
        verbose_name_plural = "Solicitudes de publicacion"
        
class SolicitudDeNegociacion(models.Model):
    solicitante = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    tipo = models.CharField(max_length = 4 , choices = negChoices, default = "Compra")
    lugar = models.ForeignKey('Lugar', on_delete = models.CASCADE)
    cuarto = models.ForeignKey('Cuarto',null = True, on_delete = models.CASCADE)
    estado = models.CharField(max_length = 1 , default = "Pendiente")
    tiempo = models.DateTimeField(auto_now_add = True, blank = False)
    fecha = models.DateField(auto_now_add = False,null = True)
    
    
    def __str__(self):
        return str(self.solicitante) + ' solicita ' + self.tipo + ' a ' + str(self.lugar.propietario)
        
    class Meta:
        unique_together = (('solicitante','tipo','lugar','tiempo'),)
        verbose_name = "Solicitud de negociación"
        verbose_name_plural = "Solicitudes de negociación"
