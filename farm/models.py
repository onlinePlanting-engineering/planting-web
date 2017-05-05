# _*_ coding: utf-8 -*-

from django.db import models
from uuid import uuid4
from tinymce_4.fields import TinyMCEModelField
from django.contrib.auth import get_user_model

User = get_user_model()

def farm_image_storage_directory(instance, filename):
    ext = filename.split('.')[-1]
    return 'farm/{0}.{1}'.format(uuid4().hex, ext)

class Farm(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=24, unique=True)
    addr = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=16, blank=True)
    subject = models.CharField(max_length=128, blank=True)
    price = models.PositiveIntegerField(default=0)
    is_delete = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    notice = TinyMCEModelField(default="农场须知")   # 农场须知
    content = TinyMCEModelField(default='农场介绍')

    def __str__(self):
        return '{id} - {name}'.format(id = self.id, name = self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.user is None:
            self.user = User.objects.get(id=1)
        super(Farm, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)

class FarmImage(models.Model):
    farm = models.ForeignKey(Farm, related_name='images')
    image = models.ImageField(upload_to=farm_image_storage_directory, null=True, blank=True)     # 农场图片
    is_delete = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    flags = models.IntegerField(default=0, db_index=True)   # 0。 农场外图， 1. 农场内图， 2. 其他

    def __str__(self):
        return '{farm} - {image}'.format(farm=self.farm.name, image=self.image.url)

