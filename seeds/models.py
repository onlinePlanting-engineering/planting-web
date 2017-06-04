from django.db import models
from farm.models import farm_image_storage_directory
import pypinyin
from tinymce_4.fields import TinyMCEModelField

class Category(models.Model):
    name = models.CharField(max_length=12)
    desc = models.CharField(max_length=128, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    flags = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return '{name}'.format(name = self.name)

class Vegetable(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='vegetables')
    name = models.CharField(max_length=12)
    # desc = models.CharField(max_length=128, blank=True, null=True)
    desc = TinyMCEModelField(default="蔬菜种类描述")
    keywords = models.CharField(max_length=64, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    flags = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return '{name}'.format(name = self.name)

class VegMeta(models.Model):
    vgcat = models.ForeignKey(Vegetable, on_delete=models.CASCADE, related_name='vegmetas')
    name = models.CharField(max_length=12)
    stime = models.DateField(blank=True, null=True)
    etime = models.DateField(blank=True, null=True)
    cycle = models.PositiveSmallIntegerField(default=30)
    region = models.CharField(max_length=24, blank=True, null=True)
    output = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    seed_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    mature_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    # desc = models.TextField(blank=True, null=True)
    # content = models.TextField(blank=True, null=True)
    desc = TinyMCEModelField(default="蔬菜品种描述")
    content = TinyMCEModelField(default="内容")
    flags = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return '{name}'.format(
            name = self.name
        )

    @property
    def first_letter(self):
        first_letters = pypinyin.pinyin(self.name, pypinyin.FIRST_LETTER)
        return first_letters[0][0].upper()

class VegMetaImage(models.Model):
    vegmeta = models.ForeignKey(VegMeta, related_name='images')
    img = models.ImageField(upload_to=farm_image_storage_directory)     # 每周上传给用户看到图片
    is_delete = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    flags = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '{meta} - {image}'.format(meta=self.vegmeta.name, image=self.img.url)