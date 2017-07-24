# _*_ coding: utf-8 _*_

from django.db import models
from farm.models import Farm
from django.contrib.auth import get_user_model
from farm.models import farm_image_storage_directory
from tinymce_4.fields import TinyMCEModelField
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from tinymce_4.fields import TinyMCEModelField
from django.utils.translation import ugettext_lazy as _

User = get_user_model()

class LandManager(models.Manager):
    pass

class Land(models.Model):
    CATEGORIES = (
        (True, _("大鹏种植")),
        (False, _("露天种植")),
    )
    TRUSTEDS = (
        (True, _("托管")),
        (False, _("非托管")),
    )
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='lands', verbose_name=_("农场"))
    cat = models.BooleanField(default=False, verbose_name=_("大棚或露天种植"), choices=CATEGORIES)
    is_trusteed = models.BooleanField(default=True, verbose_name=_("是否托管"))
    name = models.CharField(max_length=16, null=True, blank=True, verbose_name=_("土地名称"))
    # desc = models.TextField(default='', null=True, blank=True)
    desc = TinyMCEModelField(default="土地描述", verbose_name=_("土地描述"))
    size = models.PositiveIntegerField(default=666, verbose_name=_("土地面积"), help_text=_("单位为平方米"))
    is_active = models.BooleanField(default=False, verbose_name=_("该块土地是否可租"))
    count = models.PositiveIntegerField(default=0, verbose_name=_("该块土地可切多少小块"))
    item_size = models.PositiveIntegerField(default=33, verbose_name=_("每小块土地面积"))
    item_price = models.DecimalField(default=2999, max_digits=10, decimal_places=2, verbose_name=_("每小块土地一年的租金"))
    unit_price = models.DecimalField(default=90.87, max_digits=10, decimal_places=2, verbose_name=_("每平方米的租金"))
    created_date = models.DateField(auto_now_add=True, verbose_name=_("创建时间"))
    updated_date = models.DateField(auto_now=True, verbose_name=_("更新时间"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("是否删除"))
    flags = models.PositiveSmallIntegerField(default=0, verbose_name=_("标志位"))

    objects = LandManager()

    def __str__(self):
        return '{farm_name} - {name}'.\
            format(farm_name=self.farm.name, name=self.name)

    def get_api_url(self):
        return reverse("land-detail", kwargs={'pk': self.id})

class MetaManager(models.Manager):
    pass

class Meta(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='metas', verbose_name=_("所属土地"))
    owner = models.ForeignKey(User, verbose_name=_("所属用户"))
    num = models.CharField(max_length=12, unique=True, verbose_name=_("编号"))
    is_rented = models.BooleanField(default=False, verbose_name=_("是否被租"))
    size = models.PositiveIntegerField(default=33, verbose_name=_("面积"))
    price = models.DecimalField(default=2999.99, max_digits=10, decimal_places=2, verbose_name=_("每年租金"))
    is_active = models.BooleanField(default=False, verbose_name=_("是否激活"))
    created_date = models.DateField(auto_now_add=True, verbose_name=_("创建时间"))
    updated_date = models.DateField(auto_now=True, verbose_name=_("更新时间"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("是否删除"))
    flags = models.PositiveSmallIntegerField(default=0, verbose_name=_("标志位"))
    notice = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("通知"))

    objects = MetaManager()

    def __str__(self):
        return '{farm_name} - {cat} - {num}'. \
            format(farm_name=self.land.farm.name,
                   cat=self.land.cat, num=self.num)



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