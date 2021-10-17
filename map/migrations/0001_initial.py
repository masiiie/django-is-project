# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-03 03:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='marker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('icon', models.CharField(max_length=50)),
                ('lat', models.FloatField(default=0)),
                ('lng', models.FloatField(default=0)),
            ],
        ),
    ]