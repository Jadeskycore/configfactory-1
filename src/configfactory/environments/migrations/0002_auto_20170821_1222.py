# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('environments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='environment',
            options={'ordering': ('order', 'name'), 'verbose_name': 'environment', 'verbose_name_plural': 'environments'},
        ),
        migrations.AddField(
            model_name='environment',
            name='order',
            field=models.SmallIntegerField(default=0, verbose_name='order'),
        ),
    ]
