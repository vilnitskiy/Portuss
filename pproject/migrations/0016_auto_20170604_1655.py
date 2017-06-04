# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 16:55
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pproject', '0015_auto_20170604_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='car_rating',
            field=models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='commonuser',
            name='user_rating',
            field=models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
