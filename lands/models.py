# _*_ coding: utf-8 _*_

from django.db import models
from farm.models import Farm
from django.contrib.auth import get_user_model
from farm.models import farm_image_storage_directory
from tinymce_4.fields import TinyMCEModelField
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from tinymce_4.fields import TinyMCEModelField

User = get_user_model()

class LandManager(models.Manager):
    pass

class Land(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='lands')
    cat = models.BooleanField(default=False)            # 是否有棚
    is_trusteed = models.BooleanField(default=True)     # 是否托管，True-托管，False-不托管
    name = models.CharField(max_length=16, null=True, blank=True)
    # desc = models.TextField(default='', null=True, blank=True)
    desc = TinyMCEModelField(default="土地描述")
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

    objects = LandManager()

    def __str__(self):
        return '{farm_name} - {name}'.\
            format(farm_name=self.farm.name, name=self.name)

    def get_api_url(self):
        return reverse("land-detail", kwargs={'pk': self.id})

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
        return '{farm_name} - {cat} - {num}'. \
            format(farm_name=self.land.farm.name,
                   cat=self.land.cat, num=self.num)

# class MetaImage(models.Model):
#     meta = models.ForeignKey(Meta, related_name='images')
#     img = models.ImageField(upload_to=farm_image_storage_directory)     # 每周上传给用户看到图片
#     is_delete = models.BooleanField(default=False)
#     created_date = models.DateField(auto_now_add=True)
#     updated_date = models.DateField(auto_now=True)
#     flags = models.PositiveSmallIntegerField(default=0)

    # def __str__(self):
    #     return '{meta} - {image}'.format(meta=self.meta.num, image=self.img.url)

def create_land_metas(sender, instance, created, **kwargs):
    if created:
        item_size = instance.item_size
        item_price = instance.item_price
        owner = instance.farm.owner
        name = instance.name

        count = instance.count
        if count == 0:
            count = int(instance.size / item_size)

        for i in range(count):
            num = '{:04d}'.format(i+1)
            num = '{land_name}-{num}'.format(land_name=name, num=num)
            Meta.objects.create(
                land = instance,
                owner = owner,
                num = num,
                size = item_size,
                price = item_price
            )

post_save.connect(create_land_metas, sender=Land)