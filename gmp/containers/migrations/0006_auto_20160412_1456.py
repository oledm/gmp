# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-12 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('containers', '0005_auto_20160411_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='location',
            field=models.CharField(default='', max_length=200, verbose_name='Место установки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='carrier',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Тип носителя'),
        ),
        migrations.AlterField(
            model_name='container',
            name='desc',
            field=models.CharField(max_length=200, verbose_name='Описание оборудования'),
        ),
        migrations.AlterField(
            model_name='control',
            name='area',
            field=models.CharField(max_length=200, verbose_name='Объем контроля при изготовлении'),
        ),
        migrations.AlterField(
            model_name='control',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Метод контроля при изготовлении'),
        ),
        migrations.AlterField(
            model_name='factory',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Наименование завода'),
        ),
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Наименование материала'),
        ),
        migrations.AlterField(
            model_name='welding',
            name='material',
            field=models.CharField(max_length=200, verbose_name='Материал сварки'),
        ),
        migrations.AlterField(
            model_name='welding',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Вид сварки'),
        ),
    ]
