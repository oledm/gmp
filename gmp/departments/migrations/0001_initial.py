# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-09 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Measurer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование прибора')),
                ('model', models.CharField(max_length=50, verbose_name='Тип (марка)')),
                ('serial_number', models.CharField(max_length=30, verbose_name='Заводской номер')),
                ('verification', models.CharField(max_length=50, verbose_name='Свидетельство о поверке')),
                ('expired_at', models.DateField(max_length=50, verbose_name='Дата следующей поверки')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='departments.Department', verbose_name='Отдел')),
            ],
        ),
    ]
