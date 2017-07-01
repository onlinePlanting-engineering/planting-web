from django.db import models
from django.utils.translation import ugettext_lazy as _

from lands.models import Land
from images.models import upload_to

class CameraManager(models.Manager):
    pass

class Camera(models.Model):
    DEFINITION_CHOICES = (
        (1, '512/768kpbs'),
        (2, '128/256kpbs')
    )
    url = models.CharField(_('页面地址（URL）信息：'), max_length=1024)
    land = models.ForeignKey(Land, default=1, verbose_name='土地', related_name='cameras', help_text='摄像头所安置的土地名')
    title = models.CharField(_('标题'), max_length=64, null=True, blank=True)
    definition = models.PositiveSmallIntegerField(_('分辨率'), default=1, choices=DEFINITION_CHOICES, null=True, blank=True)
    abstract = models.TextField(_('简介'), max_length=1024, null=True, blank=True)
    cover_img = models.ImageField(_('封面图片'), upload_to=upload_to('upload/camera'), null=True, blank=True)
    password = models.CharField(_('播放密码'), max_length=6, null=True, blank=True, help_text="纯数字，最长 6 位数")
    duration = models.IntegerField(_('播放时长限制'), default=10)

    created_date = models.DateField(_('创建时间'), auto_now_add=True)
    updated_date = models.DateField(_('修改时间'), auto_now=True)
    is_active = models.BooleanField(_('是否被激活'), default=True)

    objects = CameraManager()

    def __str__(self):
        return '{id} - {land_name}'.format(id=self.pk, land_name=self.land.name)