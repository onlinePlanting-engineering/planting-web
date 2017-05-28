from django.contrib import admin
from .models import ImageGroup, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3

class ImageGroupAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]

admin.site.register(ImageGroup, ImageGroupAdmin)