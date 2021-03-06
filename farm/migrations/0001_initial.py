# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 14:36
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=24, unique=True)),
                ('addr', models.CharField(blank=True, max_length=64)),
                ('phone', models.CharField(blank=True, max_length=16)),
                ('subject', models.CharField(blank=True, max_length=128)),
                ('price', models.PositiveIntegerField(default=0)),
                ('desc', models.TextField(blank=True, null=True)),
                ('notice', models.TextField(blank=True, max_length=1024, null=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FarmImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=accounts.models.user_directory_path)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('flags', models.IntegerField(db_index=True, default=0)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='farm.Farm')),
            ],
        ),
    ]
