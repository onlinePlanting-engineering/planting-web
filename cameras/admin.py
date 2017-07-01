from django.contrib import admin
from .models import Camera

class CameraAdmin(admin.ModelAdmin):
    fields = ('url', 'land', 'title', 'definition', 'password', 'duration', 'is_active', 'abstract', 'cover_img')
    list_display = ('id', 'land', 'title', 'definition', 'duration', 'is_active', 'url', 'cover_img')
    save_on_top = True

admin.site.register(Camera, CameraAdmin)
