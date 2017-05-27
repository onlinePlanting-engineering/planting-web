# _*_ coding: utf-8 _*_

from django.db import models
from farm.models import Farm
from django.contrib.auth import get_user_model
from farm.models import farm_image_storage_directory
from tinymce_4.fields import TinyMCEModelField

User = get_user_model()

class Land(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='lands')
    cat = models.BooleanField(default=False)            # 是否有棚
    is_trusteed = models.BooleanField(default=True)     # 是否托管，True-托管，False-不托管
    num = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=16, null=True, blank=True)
    size = models.PositiveIntegerField(default=666)     # 每块土地大小
    is_active = models.BooleanField(default=False)      # 是否可用
    count = models.PositiveIntegerField(default=0)      # 切分数量
    item_size = models.PositiveIntegerField(default=33) # 每块大小
    item_price = models.DecimalField(default=2999, max_digits=10, decimal_places=2)        # 每块租金
    unit_price = models.DecimalField(default=90.87, max_digits=10, decimal_places=2)       # 每平米租金
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    flags = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '{farm_name} - {cat} - {num}'.\
            format(farm_name=self.farm.name, cat=self.cat, num=self.num)

class Meta(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='metas')
    owner = models.ForeignKey(User)
    num = models.CharField(max_length=12, unique=True)
    is_rented = models.BooleanField(default=False)
    size = models.PositiveIntegerField(default=33)
    price = models.DecimalField(default=2999.99, max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    flags = models.PositiveSmallIntegerField(default=0)
    notice = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return '{farm_name} - {cat} - {land_num} - {num}'. \
            format(farm_name=self.land.farm.name,
                   cat=self.land.cat, land_num=self.land.num, num=self.num)

class MetaImage(models.Model):
    meta = models.ForeignKey(Meta, related_name='images')
    img = models.ImageField(upload_to=farm_image_storage_directory)     # 每周上传给用户看到图片
    is_delete = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    flags = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '{meta} - {image}'.format(meta=self.meta.num, image=self.img.url)
