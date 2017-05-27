# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-24 12:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amarreapp', '0002_combustible'),
    ]

    operations = [
        migrations.CreateModel(
            name='Embarcacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eslora', models.DecimalField(decimal_places=2, max_digits=4)),
                ('manga', models.DecimalField(decimal_places=2, max_digits=4)),
                ('calado', models.DecimalField(decimal_places=2, max_digits=4)),
                ('motor_num', models.PositiveIntegerField()),
                ('motor_potencia', models.PositiveIntegerField()),
                ('motor_tipo', models.CharField(choices=[('I', 'Intraborda'), ('F', 'Foraborda')], default='F', max_length=1)),
                ('motor_consumo', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('motor_combustible', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='amarreapp.Combustible')),
            ],
        ),
    ]