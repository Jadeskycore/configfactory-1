# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('environments', '0002_auto_20170821_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
        ),
    ]
