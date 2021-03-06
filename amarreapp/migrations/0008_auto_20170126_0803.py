# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 08:03
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amarreapp', '0007_auto_20170125_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='fax',
            field=models.CharField(blank=True, max_length=15, verbose_name='fax'),
        ),
        migrations.AddField(
            model_name='contacto',
            name='telefono',
            field=models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='correo_electronico',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='pagina_web',
            field=models.URLField(blank=True),
        ),
    ]
