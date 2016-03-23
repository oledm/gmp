# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-17 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engines', '0020_auto_20160317_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='engine',
            name='control_zone_1',
            field=models.SmallIntegerField(choices=[(0, 'Подшипниковый щит со стороны привода'), (1, 'Крышка коробки выводов'), (2, 'Наружная оболочка корпуса статора'), (3, 'Подшипниковый щит с противоположной стороны привода')], default=0, verbose_name='Зона контроля 1'),
        ),
        migrations.AddField(
            model_name='engine',
            name='control_zone_2',
            field=models.SmallIntegerField(choices=[(0, 'Подшипниковый щит со стороны привода'), (1, 'Крышка коробки выводов'), (2, 'Наружная оболочка корпуса статора'), (3, 'Подшипниковый щит с противоположной стороны привода')], default=1, verbose_name='Зона контроля 2'),
        ),
        migrations.AddField(
            model_name='engine',
            name='control_zone_3',
            field=models.SmallIntegerField(choices=[(0, 'Подшипниковый щит со стороны привода'), (1, 'Крышка коробки выводов'), (2, 'Наружная оболочка корпуса статора'), (3, 'Подшипниковый щит с противоположной стороны привода')], default=2, verbose_name='Зона контроля 3'),
        ),
        migrations.AddField(
            model_name='engine',
            name='control_zone_4',
            field=models.SmallIntegerField(choices=[(0, 'Подшипниковый щит со стороны привода'), (1, 'Крышка коробки выводов'), (2, 'Наружная оболочка корпуса статора'), (3, 'Подшипниковый щит с противоположной стороны привода')], default=3, verbose_name='Зона контроля 4'),
        ),
    ]