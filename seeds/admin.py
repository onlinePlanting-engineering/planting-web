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
    list_display = ('id', 'cat', 'name', 'desc', 'keywords')
    list_filter = ('cat', )

class VegMetaAdmin(admin.ModelAdmin):
    inlines = [VegMetaImageInline,]
    list_display = ('id', 'get_vgcat', 'name', 'stime', 'etime', 'get_cycle', 'region', 'get_output')
    list_filter = ('vgcat', )

    def get_vgcat(self, obj):
        return obj.vgcat.name
    get_vgcat.admin_order_field = 'vgcat'
    get_vgcat.short_description = '品种'

    def get_cycle(self, obj):
        return obj.cycle
    get_cycle.short_description = '生长周期 (天)'

    def get_output(self, obj):
        return obj.output
    get_output.short_description = '产量 (公斤/亩)'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc')

admin.site.register(Vegetable, VegtableAdmin)
admin.site.register(VegMeta, VegMetaAdmin)
admin.site.register(Category, CategoryAdmin)