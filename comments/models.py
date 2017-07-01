from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from tinymce_4.fields import TinyMCEModelField

User = get_user_model()

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).\
            filter(content_type=content_type, object_id=obj_id).\
            filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, id, data, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(pk=id)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = data.get('content', '')
                instance.grade = data.get('grade', 5)
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None

class Comment(models.Model):
    GRADE_CHOICES = (
        (1, '*'),
        (2, '**'),
        (3, '***'),
        (4, '****'),
        (5, '*****'),
    )

    user = models.ForeignKey(User, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey('self', null=True, blank=True)
    # content = models.TextField()
    content = TinyMCEModelField(default='评论内容')
    grade = models.PositiveSmallIntegerField(default=5, choices=GRADE_CHOICES, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']


    def __str__(self):
        return self.user.username

    def get_api_url(self):
        return reverse("comments-api:thread", kwargs={'pk': self.id})

    def get_content_type_name(self):
        return self.content_type.name

    def children(self): # replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.children().count() == 0:
            return False
        return True
        # if self.parent is not None:
        #     return False
        # return True