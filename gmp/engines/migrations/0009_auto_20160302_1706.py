# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-02 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engines', '0008_auto_20160302_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engine',
            name='freq',
            field=models.SmallIntegerField(verbose_name='Номинальная частота вращения, об/мин'),
        ),
    ]
