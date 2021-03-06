# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-02 07:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lands', '0026_auto_20170528_1426'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='new', max_length=24, verbose_name='Status')),
                ('currency', models.CharField(editable=False, help_text='Currency in which this order was concluded', max_length=7)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Subtotal')),
                ('total', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Tocal')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated_at')),
                ('is_valid', models.BooleanField(default=True, help_text='will be set to be false automatically if not paid within 45 minutes')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, help_text='Product name at the moment of purchase.', max_length=255, null=True, verbose_name='Product name')),
                ('product_code', models.CharField(blank=True, help_text='Product code at the moment of purchase.', max_length=255, null=True, verbose_name='Product code')),
                ('unit_price', models.DecimalField(decimal_places=2, help_text='Products unit price at the moment of purchase.', max_digits=30, null=True, verbose_name='Unit price')),
                ('quantity', models.SmallIntegerField(default=1, help_text='The quantity of the same product purchased', verbose_name='Quantity')),
                ('line_total', models.DecimalField(decimal_places=2, help_text='Line total on the invoice at the moment of purchase.', max_digits=30, null=True, verbose_name='Line Total')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.BaseOrder', verbose_name='Order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lands.Meta', verbose_name='Product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(help_text='How much was paid with this particaular transfer.', max_length=7, verbose_name='Amount paid')),
                ('transaction_id', models.CharField(help_text="The transaction processor's reference", max_length=255, verbose_name='Transaction ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Received at')),
                ('payment_method', models.CharField(help_text='The payment backend used to process the purchase', max_length=50, verbose_name='Payment method')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.BaseOrder', verbose_name='Order')),
            ],
        ),
    ]
