# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 11:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amarreapp', '0006_contacto_puerto'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gestor_combustible',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='gestor_predicciones',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='gestor_puertos',
            field=models.BooleanField(default=False),
        ),
    ]