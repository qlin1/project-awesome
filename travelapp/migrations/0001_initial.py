# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-07 02:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(blank=True, default='', max_length=200)),
                ('activity', models.CharField(blank=True, default='', max_length=200)),
                ('destination', models.CharField(blank=True, default='', max_length=200)),
                ('url', models.CharField(blank=True, default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_date', models.CharField(blank=True, default='', max_length=20)),
                ('create_date', models.DateField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travelapp.Plan'),
        ),
    ]
