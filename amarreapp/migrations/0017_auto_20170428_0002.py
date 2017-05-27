# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 00:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amarreapp', '0016_auto_20170427_2312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Precio_mes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enero', models.DecimalField(decimal_places=2, max_digits=4)),
                ('febrero', models.DecimalField(decimal_places=2, max_digits=4)),
                ('marzo', models.DecimalField(decimal_places=2, max_digits=4)),
                ('abril', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.AddField(
            model_name='amarre',
            name='precio_dia',
            field=models.ForeignKey(default=1.0, on_delete=django.db.models.deletion.CASCADE, to='amarreapp.Precio_mes'),
            preserve_default=False,
        ),
    ]
