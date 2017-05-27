# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-16 00:09
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amarreapp', '0027_distancia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distancia',
            name='distancia',
        ),
        migrations.AddField(
            model_name='distancia',
            name='distancia_km',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5, verbose_name='distance_km'),
        ),
    ]
