from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class WpUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users must have an user_login name')

        user = self.model(
            user_login = username,
            email = email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            password=password,
            email=email
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class WpUser(AbstractBaseUser):
    """This has been given a wp prefix, as contrib.user is so commonly
    imported name, and we do not want to namespace this everywhere."""

    id = models.AutoField(primary_key=True, db_column='ID' )  # Field name made lowercase.
    user_login = models.CharField(max_length=180, unique=True)
    user_pass = models.CharField(max_length=192)
    user_nicename = models.CharField(max_length=150,null=True, blank=True)
    email = models.CharField(max_length=300, db_column='user_email', default='')
    user_url = models.CharField(max_length=300, null=True, blank=True)
    user_registered = models.DateTimeField(auto_now_add=True)
    user_activation_key = models.CharField(max_length=180, null=True, blank=True)
    user_status = models.IntegerField(default=1)
    display_name = models.CharField(max_length=750, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = u'wp_users'

    objects = WpUserManager()

    USERNAME_FIELD = 'user_login'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.user_login

    def get_full_name(self):
        return self.user_login

    def get_short_name(self):
        return self.user_login

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission"
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin