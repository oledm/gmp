# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-14 12:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engines', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThermClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SmallIntegerField(choices=[(0, 'T1'), (1, 'T2'), (2, 'T3'), (3, 'T4'), (4, 'T5'), (5, 'T6')], unique=True, verbose_name='Обозначение температурного класса')),
            ],
            options={
                'verbose_name_plural': 'Thermo classes',
            },
        ),
    ]
