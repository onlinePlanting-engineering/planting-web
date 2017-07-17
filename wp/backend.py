from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, get_hasher
from wp.models import WpUser

UserModel = get_user_model()
# UserModel = WpUser

class WPBackend(object):
    """
    Authentication against user_login and a hash of the password, For example:
    user_login = "planting"
    user_pass = "$P$B8Wa4IPrveTlsVAIPhT5WIot8qfc67/"

    Before check_password, need to convert hashed password to "phpass$$P$B8Wa4IPrveTlsVAIPhT5WIot8qfc67/"
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(user_login=username)
        except:
            return None
        else:
            hasher = get_hasher('phpass')
            encoded_password = hasher.from_orig(user.user_pass)

            if check_password(password, encoded_password) and self.user_can_authenticate(user):
                return user
            return None

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(id=user_id)
        except:
            return None
        return user if self.user_can_authenticate(user) else None
