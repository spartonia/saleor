# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-20 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_remove_product_weight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price_recurring',
        ),
    ]
