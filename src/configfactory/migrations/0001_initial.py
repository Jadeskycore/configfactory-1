# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-17 06:43
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('alias', autoslug.fields.AutoSlugField(editable=False, populate_from='name')),
                ('settings', jsonfield.fields.JSONField(default={})),
                ('settings_development', jsonfield.fields.JSONField(default={})),
                ('settings_staging', jsonfield.fields.JSONField(default={})),
                ('settings_production', jsonfield.fields.JSONField(default={})),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]