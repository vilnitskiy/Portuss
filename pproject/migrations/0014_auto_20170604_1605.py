# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pproject', '0013_commentcar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentcar',
            name='comment_body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='commentcar',
            name='unauthed_user_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
