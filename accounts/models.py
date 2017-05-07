from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    return 'user_{0}/{1}.{2}'.format(instance.owner.id, uuid4().hex, ext)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    '''Customized account integrated with system users'''
    nickname = models.CharField(max_length=12, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')        # M-male, F-female, O-others
    addr = models.CharField(max_length=128, blank=True)
    mobile = models.CharField(max_length=24, db_index=True, blank=True)
    qq = models.CharField(max_length=16, blank=True)
    weixin = models.CharField(max_length=16, blank=True)
    is_deleted = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_third_party = models.BooleanField(default=False)
    img_heading = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    flags = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return '{id} - {name}'.format(id=self.owner.id, name=self.owner.username)

    # reserved char fileds
    rfc0 = models.CharField(max_length=32, null=True, blank=True)
    rfc1 = models.CharField(max_length=32, null=True, blank=True)
    rfc2 = models.CharField(max_length=32, null=True, blank=True)
    rfc3 = models.CharField(max_length=32, null=True, blank=True)
    rfc4 = models.CharField(max_length=32, null=True, blank=True)
    rfc5 = models.CharField(max_length=64, null=True, blank=True)
    rfc6 = models.CharField(max_length=64, null=True, blank=True)
    rfc7 = models.CharField(max_length=64, null=True, blank=True)
    rfc8 = models.CharField(max_length=64, null=True, blank=True)
    rfc9 = models.CharField(max_length=64, null=True, blank=True)
    rfc10 = models.CharField(max_length=128, blank=True, null=True)
    rfc11 = models.CharField(max_length=128, blank=True, null=True)
    rfc12 = models.CharField(max_length=128, blank=True, null=True)
    rfc13 = models.CharField(max_length=128, blank=True, null=True)
    rfc14 = models.CharField(max_length=128, blank=True, null=True)

    # reserved integer fileds
    rfi0 = models.IntegerField(null=True, blank=True)
    rfi1 = models.IntegerField(null=True, blank=True)
    rfi2 = models.IntegerField(null=True, blank=True)
    rfi3 = models.IntegerField(null=True, blank=True)
    rfi4 = models.IntegerField(null=True, blank=True)
    rfi5 = models.IntegerField(null=True, blank=True)
    rfi6 = models.IntegerField(null=True, blank=True)
    rfi7 = models.IntegerField(null=True, blank=True)
    rfi8 = models.IntegerField(null=True, blank=True)
    rfi9 = models.IntegerField(null=True, blank=True)
    rfi10 = models.IntegerField(null=True, blank=True)
    rfi11 = models.IntegerField(null=True, blank=True)
    rfi12 = models.IntegerField(null=True, blank=True)
    rfi13 = models.IntegerField(null=True, blank=True)
    rfi14 = models.IntegerField(null=True, blank=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)
post_save.connect(create_user_profile, sender=User)