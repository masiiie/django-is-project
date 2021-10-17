from django.db import models
import django.utils.timezone as tz
import datetime

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
    )

sellChoices = (
    ("VE","Venta"),
    ("RL","Renta linear"),
    ("RC","Renta por cuartos"),
    ("RLC","Renta linear o Renta por cuartos"),
    ("VRL","Venta y Renta linear"),
    ("VRC","Venta y Renta por cuartos"),
    ("VRLC","Venta y Renta linear o Renta por cuartos"),
    )

class Lugar(models.Model):
    calle_principal = models.CharField(default = "calle principal", max_length = 60, blank = False)
    calle_secundaria = models.CharField(default = "calle secundaria" ,max_length = 60, blank = False)
    calle_secundaria_opcional = models.CharField(max_length = 60, blank = True)

    propietario = models.ForeignKey('Usuario', on_delete = models.CASCADE)

    tags_de_casa = models.TextField(blank = True)
    descripcion = models.TextField(blank = True)

    foto1 = models.ImageField(upload_to = "imagen_casa",blank = True)
    foto2 = models.ImageField(upload_to = "imagen_casa",blank = True)
    foto3 = models.ImageField(upload_to = "imagen_casa",blank = True)

    cantidad_de_bannos = models.IntegerField(default = 1)
    cantidad_de_cuartos = models.IntegerField(default = 1)
    cantidad_de_plantas = models.IntegerField(default = 1)
    número_de_vivienda = models.IntegerField(default = 202, blank = False)
    precio_de_alquiler = models.IntegerField(default = 100)
    precio_de_venta = models.IntegerField(default = 10000)
    precio_de_subasta = models.IntegerField(default = 10000)
    fecha_final_subasta = models.DateField(default = 1000)

    evaluacion = models.IntegerField(default = 1)
    

    tiene_calle_secundaria_opcional = models.BooleanField(default = True, blank = False)
    municipio = models.CharField(max_length = 21, blank = False, default = "10 de Octubre")
    provincia = models.CharField(max_length = 21, choices = provinceChoice, blank = False, default = "LH") 
    venta_o_renta = models.CharField(max_length = 4 , choices = sellChoices, default = "VE")
    disponible_para_alquiler_por_cuartos = models.BooleanField(default = True)
    disponible_para_alquiler_linear = models.BooleanField(default = True)
    subastable = models.BooleanField(default = True)
    
    último_cambio = models.DateField(auto_now_add = True, blank = False)

    def __str__(self):
        return self.calle_principal +" "+ str(self.número_de_vivienda) +", "+ self.provincia

    class Meta:
        managed = True
        unique_together = (('calle_principal','calle_secundaria','calle_secundaria_opcional','número_de_vivienda'),)
        verbose_name_plural = "Lugares"

class Cuarto(models.Model):
    casa = models.ForeignKey('Lugar', on_delete = models.CASCADE)
    cantidad_de_camas = models.IntegerField(default = 1)
    banno_compartido = models.BooleanField(default = False)
    tags_de_cuarto = models.TextField(blank = True)

    def __str__(self):
        return self.casa.calle_principal +" "+ str(self.casa.número_de_vivienda) +", "+ self.casa.provincia

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

    class Meta:
        unique_together = (('cuarto','fecha_inicio','fecha_final'),)
        verbose_name_plural = "Disponibilidad de cuartos"
        pass

class Correo(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete = models.CASCADE)
    texto = models.TextField(default = "")
    estado = models.CharField(choices = mailChoices, default = "PE", max_length = 2)
    fecha_tiempo = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = "Correos"

class Log(models.Model):
    lugar = models.ForeignKey('Lugar', on_delete = models.CASCADE)
    usuario = models.ForeignKey('Usuario', on_delete = models.CASCADE)
    accion = models.CharField(choices = actChoice,default = "VE",max_length = 2)
    texto = models.TextField(default = "")

    class Meta:
        verbose_name_plural = "Logs"

class Usuario(models.Model):
    nombre = models.CharField(max_length = 20, default = "Jonh")
    apellidos = models.CharField(max_length = 20, default = "Doe")
    contrasenna = models.CharField(max_length = 20, default = "Doe")
    satisfaccion = models.IntegerField(default = 0)
    confianza = models.IntegerField(default = 5)
    teléfono_móvil = models.CharField(max_length = 11, blank = True)
    teléfono_fijo = models.CharField(max_length = 15, blank = True)
    correo_electrónico = models.EmailField(blank = True)
    tipo = models.CharField(choices = typeChoices, default = "Cliente", max_length = 20)

    def __str__(self):
        return self.nombre + " " + self.apellidos

    class Meta:
        verbose_name_plural = "Usuarios"
    
class Puja(models.Model):
    lugar = models.ForeignKey('Lugar', on_delete = models.CASCADE)
    tamanno_de_puja = models.IntegerField(default = 0)
    nuevo_precio = models.IntegerField(default = 0)
    usuario = models.ForeignKey('Usuario', on_delete = models.CASCADE)
    tiempo = models.DateTimeField(auto_now_add = True, blank = False)

    def __str__(self):
        return self.usuario.nombre + " : " + str(self.tiempo)

    class Meta:
        unique_together = (('lugar','tamanno_de_puja','usuario','tiempo'),)
        verbose_name_plural = "Pujas"

class Tag_de_casa(models.Model):
    posicion = models.AutoField("ID",primary_key = True)
    nombre = models.CharField(max_length = 20,default = "")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tags_de_casas"

class Tag_de_cuarto(models.Model):
    posicion = models.AutoField("ID",primary_key = True)
    nombre = models.CharField(max_length = 20,default = "")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tags_de_cuartos"