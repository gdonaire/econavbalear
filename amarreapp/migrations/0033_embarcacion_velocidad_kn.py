# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-16 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amarreapp', '0032_auto_20170516_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='embarcacion',
            name='velocidad_kn',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
