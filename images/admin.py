from django.contrib import admin
from .models import ImageGroup, Image

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'is_cover', 'img')
    list_filter = ('group', 'is_cover')

class ImageInline(admin.TabularInline):
    model = Image
    extra = 3

class ImageGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content_type', 'object_id', 'desc')
    list_filter = ('content_type',)
    inlines = [ImageInline, ]

admin.site.register(ImageGroup, ImageGroupAdmin)
admin.site.register(Image, ImageAdmin)