# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-29 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pproject', '0012_auto_20170429_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='building',
            field=models.PositiveIntegerField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='street',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
