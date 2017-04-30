# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-23 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pproject', '0008_commonuser_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonuser',
            name='docs_are_checked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commonuser',
            name='soc_networks_are_checked',
            field=models.BooleanField(default=False),
        ),
    ]
