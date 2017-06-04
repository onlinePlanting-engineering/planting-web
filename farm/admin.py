from django.contrib import admin
from .models import Farm, FarmImage

class FarmImageInline(admin.TabularInline):
    model = FarmImage
    extra = 3

class FarmAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'addr', 'phone', 'price')
    inlines = [FarmImageInline, ]

admin.site.register(Farm, FarmAdmin)