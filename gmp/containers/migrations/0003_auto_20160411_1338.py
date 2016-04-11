# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-11 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0002_auto_20160411_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='p_test',
            field=models.FloatField(verbose_name='Давление пробное, МПа'),
        ),
        migrations.AlterField(
            model_name='container',
            name='p_work',
            field=models.FloatField(verbose_name='Давление рабочее, МПа'),
        ),
        migrations.AlterField(
            model_name='container',
            name='volume',
            field=models.FloatField(verbose_name='Объем рабочий, м3'),
        ),
    ]
