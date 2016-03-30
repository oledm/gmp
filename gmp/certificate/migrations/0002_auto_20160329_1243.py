# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-29 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ControlTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Вид контроля')),
                ('full_name', models.CharField(max_length=50, verbose_name='Полное наименование вида контроля')),
            ],
        ),
        migrations.AlterField(
            model_name='certificate',
            name='control',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='certificate.ControlTypes', verbose_name='Вид контроля'),
        ),
    ]