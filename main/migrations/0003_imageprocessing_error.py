# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-11 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20170222_0736'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageprocessing',
            name='error',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]