# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelapp', '0009_auto_20161128_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=420),
        ),
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.CharField(max_length=420),
        ),
    ]
