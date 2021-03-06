# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-16 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engines', '0010_auto_20160316_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_cap_shield_L1_high',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Крышка узла взрывозащиты - подшипниковый щит со стороны привода/L1 (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_cap_shield_L1_low',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Крышка узла взрывозащиты - подшипниковый щит со стороны привода/L1 (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_cap_shield_L2_high',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Крышка узла взрывозащиты - подшипниковый щит со стороны привода/L2 (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_cap_shield_L2_low',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Крышка узла взрывозащиты - подшипниковый щит со стороны привода/L2 (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_cap_shield_S',
            field=models.FloatField(default=6.3, verbose_name='Неподвижное взрывонепроницаемое соединение/Крышка узла взрывозащиты - подшипниковый щит со стороны привода/S'),
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_cap_shield_W1_high',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Крышка узла взрывозащиты - подшипниковый щит со стороны привода/W1 (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_cap_shield_W1_low',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Крышка узла взрывозащиты - подшипниковый щит со стороны привода/W1 (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_cap_shield_b_high',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Крышка узла взрывозащиты - подшипниковый щит со стороны привода/b (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_cap_shield_b_low',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Крышка узла взрывозащиты - подшипниковый щит со стороны привода/b (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_cap_shield_f',
            field=models.FloatField(default=1.5, verbose_name='Неподвижное взрывонепроницаемое соединение/Крышка узла взрывозащиты - подшипниковый щит со стороны привода/f'),
        ),
    ]
