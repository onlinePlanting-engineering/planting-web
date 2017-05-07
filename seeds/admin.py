from django.contrib import admin
from .models import Category, Vegetable, VegMeta, VegMetaImage

class VegMetaImageInline(admin.TabularInline):
    model = VegMetaImage
    extra = 1

class VegMetaInline(admin.TabularInline):
    model = VegMeta
    extra = 1

class VegtableAdmin(admin.ModelAdmin):
    inlines = [VegMetaInline, ]

class VegMetaAdmin(admin.ModelAdmin):
    inlines = [VegMetaImageInline,]

admin.site.register(Vegetable, VegtableAdmin)
admin.site.register(VegMeta, VegMetaAdmin)
admin.site.register(Category)