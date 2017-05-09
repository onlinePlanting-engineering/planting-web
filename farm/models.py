# _*_ coding: utf-8 -*-

from django.db import models
from uuid import uuid4
from tinymce_4.fields import TinyMCEModelField
from django.contrib.auth import get_user_model
from comments.models import Comment

User = get_user_model()

def farm_image_storage_directory(instance, filename):
    ext = filename.split('.')[-1]
    return 'farm/{0}.{1}'.format(uuid4().hex, ext)

class Farm(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=24, unique=True)
    addr = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=16, blank=True)
    subject = models.CharField(max_length=128, blank=True)
    price = models.PositiveIntegerField(default=0)
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    notice = TinyMCEModelField(default="农场须知")   # 农场须知
    content = TinyMCEModelField(default='农场介绍')

    def __str__(self):
        return '{id} - {name}'.format(id = self.id, name = self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.owner is None:
            self.owner = User.objects.get(id=1)
        super(Farm, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

class FarmImage(models.Model):
    FLAG_CHOICES = (
        ('I', '农场内部图'),
        ('O', '农场外部图'),
        ('X', '未知未知'),
    )
    farm = models.ForeignKey(Farm, related_name='images')
    image = models.ImageField(upload_to=farm_image_storage_directory)     # 农场图片
    is_delete = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    flags = models.CharField(max_length=1, default='X', db_index=True, choices=FLAG_CHOICES)   #  O-农场外图， I-农场内图， X-其他

    def __str__(self):
        return '{farm} - {image}'.format(farm=self.farm.name, image=self.image.url)

