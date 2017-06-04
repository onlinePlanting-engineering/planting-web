from django.contrib import admin
from .models import Land, Meta

class MetaInline(admin.TabularInline):
    model = Meta
    extra = 1
#
# class MetaImageInline(admin.TabularInline):
#     model = MetaImage
#     extra = 3

class LandAdmin(admin.ModelAdmin):
    inlines = [MetaInline, ]
    list_display = ('name', 'size', 'item_size', 'item_price', 'cat', 'is_trusteed', 'is_active')
    list_filter = ('cat', 'is_trusteed', 'is_active')

class MetaAdmin(admin.ModelAdmin):
    list_display = ('land', 'num', 'owner', 'size', 'price', 'is_rented', 'is_active')
    list_filter = ('is_rented', 'is_active')

admin.site.register(Land, LandAdmin)
admin.site.register(Meta, MetaAdmin)
