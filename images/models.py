from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from uuid import uuid4

User = get_user_model()

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    return '{user}/{filename}.{ext}'.format(
        user=instance.group.user.username,
        filename=uuid4().hex,
        ext=ext
    )

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
    desc = models.CharField(max_length=1024, null=True, blank=True)
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

class Image(models.Model):
    group = models.ForeignKey(ImageGroup, on_delete=models.CASCADE, related_name='imgs')
    img = models.ImageField(upload_to=content_file_name)
    is_delete = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return '{image}'.format(image=self.img.url)