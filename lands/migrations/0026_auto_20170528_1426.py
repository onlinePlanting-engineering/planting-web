# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-28 14:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lands', '0025_auto_20170528_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metaimage',
            name='meta',
        ),
        migrations.DeleteModel(
            name='MetaImage',
        ),
    ]
