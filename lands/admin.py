from django.contrib import admin
from .models import Land, Meta, MetaImage

class MetaInline(admin.TabularInline):
    model = Meta
    extra = 1

class MetaImageInline(admin.TabularInline):
    model = MetaImage
    extra = 3

class LandAdmin(admin.ModelAdmin):
    inlines = [MetaInline, ]

class MetaAdmin(admin.ModelAdmin):
    inlines = [MetaImageInline, ]

admin.site.register(Land, LandAdmin)
admin.site.register(Meta, MetaAdmin)
