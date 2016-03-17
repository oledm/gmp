# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-17 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engines', '0018_auto_20160317_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engine',
            name='elements_condition_width_norm_cap',
        ),
        migrations.RemoveField(
            model_name='engine',
            name='elements_condition_width_norm_external',
        ),
        migrations.RemoveField(
            model_name='engine',
            name='elements_condition_width_norm_shield',
        ),
        migrations.RemoveField(
            model_name='engine',
            name='elements_condition_width_norm_shield_reverse',
        ),
        migrations.RemoveField(
            model_name='engine',
            name='elements_condition_width_real_cap',
        ),
        migrations.RemoveField(
            model_name='engine',
            name='elements_condition_width_real_external',
        ),
        migrations.RemoveField(
            model_name='engine',
            name='elements_condition_width_real_shield',
        ),
        migrations.RemoveField(
            model_name='engine',
            name='elements_condition_width_real_shield_reverse',
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_norm_cap_high',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Допустимые толщины норма (не менее) / Крышка коробки выводов (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_norm_cap_low',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Допустимые толщины норма (не менее) / Крышка коробки выводов (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_norm_external_high',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Допустимые толщины норма (не менее) / Наружная оболочка корпуса статора (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_norm_external_low',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Допустимые толщины норма (не менее) / Наружная оболочка корпуса статора (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_norm_shield_high',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Допустимые толщины норма (не менее) / Подшипниковый щит со стороны привода (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_norm_shield_low',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Допустимые толщины норма (не менее) / Подшипниковый щит со стороны привода (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_norm_shield_reverse_high',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Допустимые толщины норма (не менее) / Подшипниковый щит с противоположной приводу стороны (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_norm_shield_reverse_low',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Допустимые толщины норма (не менее) / Подшипниковый щит с противоположной приводу стороны (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_real_cap_high',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Толщина основного металла, мм (фактическая) / Крышка коробки выводов (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_real_cap_low',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Толщина основного металла, мм (фактическая) / Крышка коробки выводов (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_real_external_high',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Толщина основного металла, мм (фактическая) / Наружная оболочка корпуса статора (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_real_external_low',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Толщина основного металла, мм (фактическая) / Наружная оболочка корпуса статора (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_real_shield_high',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Толщина основного металла, мм (фактическая) / Подшипниковый щит со стороны привода (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_real_shield_low',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Толщина основного металла, мм (фактическая) / Подшипниковый щит со стороны привода (нижний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_real_shield_reverse_high',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Толщина основного металла, мм (фактическая) / Подшипниковый щит с противоположной приводу стороны (верхний предел)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='engine',
            name='elements_condition_width_real_shield_reverse_low',
            field=models.FloatField(default=0, verbose_name='Техническое состояние элементов / Толщина основного металла, мм (фактическая) / Подшипниковый щит с противоположной приводу стороны (нижний предел)'),
            preserve_default=False,
        ),
    ]
