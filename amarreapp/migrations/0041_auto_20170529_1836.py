# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-29 18:36
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amarreapp', '0040_auto_20170527_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='combustible',
            name='precio_litro',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]