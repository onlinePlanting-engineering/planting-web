from django.contrib import admin
from .models import BaseOrder, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, ]
    list_display = ('id', 'number', 'customer', 'status', 'total', 'created_at', 'updated_at')
    fields = ('number', 'customer', 'status', 'total', 'created_at', 'updated_at')
    readonly_fields = ('number', 'created_at', 'updated_at')

admin.site.register(BaseOrder, OrderAdmin)