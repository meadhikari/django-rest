# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-06 09:56
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20170527_0501'),
    ]

    operations = [
        migrations.AddField(
            model_name='binary',
            name='hash',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='binary',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/ubuntu/'), upload_to=b''),
        ),
    ]
