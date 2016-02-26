# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-26 16:42
from __future__ import unicode_literals

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20160225_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(default='SE', max_length=2, verbose_name='country'),
        ),
    ]
