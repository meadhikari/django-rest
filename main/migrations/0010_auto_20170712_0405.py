# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-12 04:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20170710_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='limit',
            field=models.IntegerField(default=100, max_length=3),
        ),
        migrations.AlterField(
            model_name='binary',
            name='hash',
            field=models.CharField(blank=True, default=1499832347, max_length=50),
        ),
    ]
