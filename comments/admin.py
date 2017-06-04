from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('user', 'content_type', 'object_id')
    list_display = ('user', 'content_type', 'object_id', 'parent', 'content')

admin.site.register(Comment, CommentAdmin)