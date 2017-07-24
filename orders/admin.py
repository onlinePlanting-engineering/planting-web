from django.contrib import admin
from .models import BaseOrder, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, ]
    list_display = ('id', 'number', 'customer', 'status', 'total')
    readonly_fields = ('number', )

admin.site.register(BaseOrder, OrderAdmin)