# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-01 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Наименование ТГ'),
        ),
    ]
