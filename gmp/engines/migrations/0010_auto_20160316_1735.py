# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-16 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engines', '0009_auto_20160316_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_stanina_L1_high',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - станина/L1 (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_stanina_L1_low',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - станина/L1 (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_stanina_L2_high',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - станина/L2 (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_stanina_L2_low',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - станина/L2 (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_stanina_S',
            field=models.FloatField(default=6.3, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - станина/S'),
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_stanina_W1_high',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - станина/W1 (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_stanina_W1_low',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - станина/W1 (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_stanina_b_high',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - станина/b (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_stanina_b_low',
            field=models.FloatField(default=0, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - станина/b (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_stanina_f',
            field=models.FloatField(default=1.5, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - станина/f'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_krishka_L1_high',
            field=models.FloatField(verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - крышка/L1 (верхний предел)'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_krishka_L1_low',
            field=models.FloatField(verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - крышка/L1 (нижний предел)'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_krishka_L2_high',
            field=models.FloatField(verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - крышка/L2 (верхний предел)'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_krishka_L2_low',
            field=models.FloatField(verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - крышка/L2 (нижний предел)'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_krishka_S',
            field=models.FloatField(default=6.3, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - крышка/S'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_krishka_W1_high',
            field=models.FloatField(verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - крышка/W1 (верхний предел)'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_krishka_W1_low',
            field=models.FloatField(verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - крышка/W1 (нижний предел)'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_krishka_b_high',
            field=models.FloatField(verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - крышка/b (верхний предел)'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_krishka_b_low',
            field=models.FloatField(verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - крышка/b (нижний предел)'),
        ),
        migrations.AlterField(
            model_name='engine',
            name='unmoveable_Ex_connections_out_krishka_f',
            field=models.FloatField(default=1.5, verbose_name='Неподвижное взрывонепроницаемое соединение/Выводное устройство - крышка/f'),
        ),
    ]
