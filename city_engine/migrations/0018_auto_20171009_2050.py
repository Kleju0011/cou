# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-09 20:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('city_engine', '0017_auto_20171008_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='cash',
            field=models.DecimalField(decimal_places=2, default=10000, max_digits=20),
        ),
    ]