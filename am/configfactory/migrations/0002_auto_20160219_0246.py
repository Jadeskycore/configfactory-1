# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 02:46
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('configfactory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='require_schema',
            field=models.BooleanField(default=False, help_text='Use json schema validation'),
        ),
        migrations.AddField(
            model_name='component',
            name='schema',
            field=jsonfield.fields.JSONField(default={}),
        ),
    ]