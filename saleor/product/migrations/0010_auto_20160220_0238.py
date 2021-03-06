# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-20 08:38
from __future__ import unicode_literals

from django.db import migrations, models
import saleor.product.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20160220_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='available_on',
            field=models.DateField(blank=True, null=True, verbose_name='available on'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=saleor.product.models.fields.WeightField(decimal_places=2, default=1, max_digits=6, unit='lb', verbose_name='weight'),
            preserve_default=False,
        ),
    ]
