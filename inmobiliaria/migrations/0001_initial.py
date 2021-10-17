# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-24 00:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alquiler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('es_linear', models.BooleanField(default=False)),
                ('fecha_inicio', models.DateField()),
                ('fecha_final', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Alquileres',
            },
        ),
        migrations.CreateModel(
            name='Correo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(default='')),
                ('estado', models.CharField(choices=[('PE', 'Pendiente'), ('AS', 'Analizándose'), ('A', 'Analizado')], default='PE', max_length=2)),
                ('fecha_tiempo', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Correos',
            },
        ),
        migrations.CreateModel(
            name='Cuarto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_de_camas', models.IntegerField(default=1, verbose_name='cantidad de camas')),
                ('banno_compartido', models.BooleanField(default=False, verbose_name='banno compartido')),
            ],
            options={
                'verbose_name_plural': 'Cuartos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Disponibilidad_de_cuarto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_final', models.DateField()),
                ('cuarto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inmobiliaria.Cuarto')),
            ],
            options={
                'verbose_name_plural': 'Disponibilidad de cuartos',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accion', models.CharField(choices=[('VE', 'Vender'), ('CM', 'Comprar'), ('SP', 'Solicitar Publicacion')], default='VE', max_length=2)),
                ('texto', models.TextField(default='')),
                ('tiempo', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, default='Hogar', max_length=30)),
                ('disponible', models.BooleanField(default=True)),
                ('calle_principal', models.CharField(default='calle principal', max_length=60, verbose_name='calle principal')),
                ('calle_secundaria', models.CharField(default='calle secundaria', max_length=60, verbose_name='calle secundaria')),
                ('calle_secundaria_opcional', models.CharField(blank=True, max_length=60, verbose_name='calle secundaria (opcional)')),
                ('ubicacion', models.CharField(choices=[('CI', 'Ciudad'), ('CP', 'Campo'), ('PL', 'Playa'), ('PE', 'Periferia')], max_length=2)),
                ('descripcion', models.TextField(blank=True)),
                ('lat', models.CharField(default='', max_length=25)),
                ('lng', models.CharField(default='', max_length=25)),
                ('foto1', models.ImageField(upload_to='imagen_casa')),
                ('foto2', models.ImageField(upload_to='imagen_casa')),
                ('foto3', models.ImageField(upload_to='imagen_casa')),
                ('cantidad_de_bannos', models.IntegerField(default=1, verbose_name='cantidad de bannos')),
                ('cantidad_de_cuartos', models.IntegerField(default=1, verbose_name='cantidad de cuartos')),
                ('cantidad_de_plantas', models.IntegerField(default=1, verbose_name='cantidad de plantas')),
                ('numero_de_vivienda', models.IntegerField(default=202, verbose_name='numero de vivienda')),
                ('precio_de_alquiler', models.IntegerField(default=100, verbose_name='precio de alquiler')),
                ('precio_de_venta', models.IntegerField(default=10000, verbose_name='precio de venta')),
                ('precio_de_subasta', models.IntegerField(default=10000, verbose_name='precio de subasta')),
                ('fecha_finalizacion', models.DateField()),
                ('evaluacion', models.IntegerField(default=1)),
                ('tiene_calle_secundaria_opcional', models.BooleanField(default=True, verbose_name='tiene calle secundaria opcional')),
                ('municipio', models.CharField(default='10 de Octubre', max_length=21)),
                ('provincia', models.CharField(choices=[('HA', 'La Habana'), ('MA', 'Matanzas'), ('PR', 'Pinar del Río'), ('VC', 'Villa Clara'), ('CI', 'Cienfuegos'), ('SE', 'Sancti Espíritus'), ('MY', 'Mayabeque'), ('AR', 'Artemisa'), ('TU', 'Las Tunas'), ('CA', 'Camaguey'), ('HO', 'Holguín'), ('GR', 'Granma'), ('SC', 'Santiago de Cuba'), ('GU', 'Guantánamo'), ('IJ', 'Isla de la Juventud')], default='LH', max_length=21)),
                ('venta_o_renta', models.CharField(choices=[('Venta', 'Venta'), ('Renta linear', 'Renta linear'), ('Renta de cuartos', 'Renta de cuartos')], default='Venta', max_length=20, verbose_name='venta o renta')),
                ('subastable', models.BooleanField(default=True)),
                ('chequeado', models.BooleanField(default=False)),
                ('ultimo_cambio', models.DateField(auto_now_add=True)),
                ('agente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lugar_asignado', to=settings.AUTH_USER_MODEL)),
                ('perito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lugar_insertado', to=settings.AUTH_USER_MODEL)),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tu_lugar', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Lugares',
                'permissions': (('view_profile', 'can see personal profile'), ('view_data', 'can see the data')),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Puja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tamanno_de_puja', models.IntegerField()),
                ('tiempo', models.DateTimeField(auto_now_add=True)),
                ('lugar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inmobiliaria.Lugar')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Pujas',
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_de_publicacion', models.CharField(blank=True, max_length=30, unique=True, verbose_name='nombre de publicación')),
                ('venta_o_renta', models.CharField(choices=[('Venta', 'Venta'), ('Renta linear', 'Renta linear'), ('Renta de cuartos', 'Renta de cuartos')], default='Venta', max_length=10, verbose_name='venta o renta')),
                ('calle_principal', models.CharField(default='calle principal', max_length=60, verbose_name='calle principal')),
                ('calle_secundaria', models.CharField(default='calle secundaria', max_length=60, verbose_name='calle secundaria')),
                ('calle_secundaria_opcional', models.CharField(blank=True, max_length=60, verbose_name='calle secundaria opcional')),
                ('tiene_calle_secundaria_opcional', models.BooleanField(default=True, verbose_name='tiene calle secundaria opcional')),
                ('numero_de_vivienda', models.IntegerField(default=202, verbose_name='numero de vivienda')),
                ('municipio', models.CharField(default='10 de Octubre', max_length=21)),
                ('provincia', models.CharField(choices=[('HA', 'La Habana'), ('MA', 'Matanzas'), ('PR', 'Pinar del Río'), ('VC', 'Villa Clara'), ('CI', 'Cienfuegos'), ('SE', 'Sancti Espíritus'), ('MY', 'Mayabeque'), ('AR', 'Artemisa'), ('TU', 'Las Tunas'), ('CA', 'Camaguey'), ('HO', 'Holguín'), ('GR', 'Granma'), ('SC', 'Santiago de Cuba'), ('GU', 'Guantánamo'), ('IJ', 'Isla de la Juventud')], default='LH', max_length=21)),
                ('chequeado', models.BooleanField(default=False)),
                ('tiempo', models.DateTimeField(auto_now_add=True)),
                ('lat', models.CharField(default='', max_length=25)),
                ('lng', models.CharField(default='', max_length=25)),
                ('perito', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitud_asignado', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Solicitudes de publicacion',
                'verbose_name': 'Solicitud de publicacion',
            },
        ),
        migrations.CreateModel(
            name='SolicitudDeNegociacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Compra', 'Compra'), ('Renta', 'Renta'), ('Renta de cuarto', 'Renta de cuarto')], default='Compra', max_length=4)),
                ('estado', models.CharField(default='Pendiente', max_length=1)),
                ('tiempo', models.DateTimeField(auto_now_add=True)),
                ('fecha', models.DateField(null=True)),
                ('cuarto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inmobiliaria.Cuarto')),
                ('lugar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inmobiliaria.Lugar')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Solicitudes de negociación',
                'verbose_name': 'Solicitud de negociación',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='algo', max_length=20)),
                ('tipo', models.CharField(choices=[('CU', 'Tag de Cuarto'), ('CA', 'Tag de Casa')], default='CA', max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'Tag',
            },
        ),
        migrations.AddField(
            model_name='lugar',
            name='tags',
            field=models.ManyToManyField(to='inmobiliaria.Tag'),
        ),
        migrations.AddField(
            model_name='log',
            name='nombre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inmobiliaria.Lugar'),
        ),
        migrations.AddField(
            model_name='log',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cuarto',
            name='casa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inmobiliaria.Lugar'),
        ),
        migrations.AddField(
            model_name='cuarto',
            name='tags',
            field=models.ManyToManyField(to='inmobiliaria.Tag'),
        ),
        migrations.AddField(
            model_name='alquiler',
            name='casa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inmobiliaria.Lugar'),
        ),
        migrations.AlterUniqueTogether(
            name='solicituddenegociacion',
            unique_together=set([('solicitante', 'tipo', 'lugar', 'tiempo')]),
        ),
        migrations.AlterUniqueTogether(
            name='puja',
            unique_together=set([('lugar', 'tamanno_de_puja', 'usuario', 'tiempo')]),
        ),
        migrations.AlterUniqueTogether(
            name='lugar',
            unique_together=set([('calle_principal', 'calle_secundaria', 'calle_secundaria_opcional', 'numero_de_vivienda')]),
        ),
        migrations.AlterUniqueTogether(
            name='disponibilidad_de_cuarto',
            unique_together=set([('cuarto', 'fecha_inicio', 'fecha_final')]),
        ),
        migrations.AlterUniqueTogether(
            name='alquiler',
            unique_together=set([('casa', 'fecha_inicio', 'fecha_final')]),
        ),
    ]