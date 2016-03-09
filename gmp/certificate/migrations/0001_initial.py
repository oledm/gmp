# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 12:10
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateField(default=datetime.date.today, verbose_name='Дата выдачи')),
                ('expired_at', models.DateField(verbose_name='Срок действия')),
                ('control', models.CharField(max_length=10, verbose_name='Вид контроля')),
                ('degree', models.PositiveSmallIntegerField(verbose_name='Уровень')),
                ('group', models.PositiveSmallIntegerField(choices=[(1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V')], verbose_name='Группа ЭБ')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
            ],
        ),
    ]
