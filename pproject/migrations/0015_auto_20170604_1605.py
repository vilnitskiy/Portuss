# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pproject', '0014_auto_20170604_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentcar',
            name='comment_body',
            field=models.TextField(default=b'comment'),
        ),
    ]