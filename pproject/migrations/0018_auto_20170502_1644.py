# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-02 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pproject', '0017_auto_20170502_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='rental_perion_begin',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='car',
            name='rental_perion_end',
            field=models.DateField(),
        ),
    ]
