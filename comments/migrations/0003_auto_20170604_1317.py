# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-04 13:17
from __future__ import unicode_literals

from django.db import migrations
import tinymce_4.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comment_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=tinymce_4.fields.TinyMCEModelField(default='评论内容'),
        ),
    ]