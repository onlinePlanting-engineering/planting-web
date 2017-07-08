from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from uuid import uuid4
from tinymce_4.fields import TinyMCEModelField
import os
from functools import partial



User = get_user_model()

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    return '{user}/{filename}.{ext}'.format(
        user=instance.group.user.username,
        filename=uuid4().hex,
        ext=ext
    )

def _update_filename(instance, filename, path):
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(path, filename)

def upload_to(path):
    return partial(_update_filename, path=path)

class ImageGroupManager(models.Manager):
    def all(self):
        qs = super(ImageGroupManager, self).all()
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(ImageGroupManager, self).\
            filter(content_type=content_type, object_id=obj_id)
        return qs

    def create_by_model_type(self, model_type, id, data, user):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(pk=id)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.desc = data.get('desc', '')
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                instance.save()
                return instance
        return None

class ImageGroup(models.Model):
    user = models.ForeignKey(User, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # desc = models.CharField(max_length=1024, null=True, blank=True)
    desc = TinyMCEModelField(default="图片描述")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)


    objects = ImageGroupManager()

    class Meta:
        ordering = ['-timestamp']


    def __str__(self):
        return '{id} - {desc}'.format(id=self.id, desc=self.desc)

    def get_api_url(self):
        return reverse("imagegroup-detail", kwargs={'pk': self.id})

    def get_content_type_name(self):
        return self.content_type.name


class ImageManager(models.Manager):
    pass

class Image(models.Model):
    group = models.ForeignKey(ImageGroup, on_delete=models.CASCADE, related_name='imgs', default=1)
    img = models.ImageField(upload_to=upload_to('upload/imgs'))
    is_delete = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    is_cover = models.BooleanField(default=False)

    objects = ImageManager()

    def __str__(self):
        try:
            object_name = self.group.content_object.name
        except:
            object_name = None
        return '{img_id} - {content_type} - {object_name} - {img_group} - {is_cover}'.format(
            content_type = self.group.content_type.name,
            object_name = object_name,
            img_group = self.group.id,
            img_id = self.id,
            is_cover=self.is_cover
        )

class CommonImageManager(models.Manager):
    pass

class CommonImage(models.Model):
    """
    Common image model don't need to bind any group
    """
    img = models.ImageField(upload_to=upload_to('upload/common/imgs'))
    name = models.CharField(max_length=64, blank=True, null=True)
    desc = models.CharField(max_length=64, blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)

    objects = CommonImageManager()

    def __str__(self):
        return '{0} - {1}'.format(self.id, self.name)