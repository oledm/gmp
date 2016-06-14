# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-14 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0013_auto_20160607_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='dimensions_side_bottom',
            field=models.FloatField(verbose_name='Толщина стенок днища (проектная), мм'),
        ),
        migrations.AlterField(
            model_name='container',
            name='dimensions_side_ring',
            field=models.FloatField(verbose_name='Толщина стенок обечайки (проектная), мм'),
        ),
    ]
