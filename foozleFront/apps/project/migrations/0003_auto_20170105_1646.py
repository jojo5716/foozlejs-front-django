# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-05 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_project_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error',
            name='resolved_time',
            field=models.DateTimeField(null=True),
        ),
    ]
