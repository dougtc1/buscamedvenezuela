# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170628_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicina',
            name='nombre',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre de marca'),
        ),
    ]
