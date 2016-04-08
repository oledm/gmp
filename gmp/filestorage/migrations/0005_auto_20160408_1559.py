# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-08 15:59
from __future__ import unicode_literals

from django.db import migrations, models
import gmp.filestorage.models


class Migration(migrations.Migration):

    dependencies = [
        ('filestorage', '0004_auto_20160408_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storage',
            name='fileupload',
            field=models.FileField(default='', upload_to=gmp.filestorage.models.get_hash_path),
            preserve_default=False,
        ),
    ]
