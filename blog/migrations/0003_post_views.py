# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-28 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20171227_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='浏览量'),
        ),
    ]
