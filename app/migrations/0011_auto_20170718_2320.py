# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 23:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20170718_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activo',
            name='componente',
            field=models.TextField(unique=True, verbose_name='Componente activo'),
        ),
        migrations.AlterField(
            model_name='medicina',
            name='nombre',
            field=models.TextField(verbose_name='Nombre de marca'),
        ),
        migrations.AlterField(
            model_name='presentacion',
            name='presentacion',
            field=models.TextField(verbose_name='Presentacion'),
        ),
        migrations.AlterField(
            model_name='presentacion',
            name='registro',
            field=models.TextField(verbose_name='Registro sanitario'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='clasificacion',
            field=models.TextField(verbose_name='Clasificacion'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='link',
            field=models.TextField(unique=True, verbose_name='Link'),
        ),
    ]
