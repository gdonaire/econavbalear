# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-08 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amarreapp', '0050_auto_20170604_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='precio',
            name='diciembre',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=5, verbose_name='Diciembre'),
        ),
    ]
