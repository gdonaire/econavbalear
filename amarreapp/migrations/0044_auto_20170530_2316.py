# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-30 23:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amarreapp', '0043_auto_20170530_2306'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='distancia',
            unique_together=set([('origen', 'destino')]),
        ),
    ]