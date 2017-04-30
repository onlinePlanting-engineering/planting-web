from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from rest_framework.serializers import (
ModelSerializer,
ValidationError,
CharField,
)

User = get_user_model()

class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
        ]

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

        extra_kwargs = {
            'password':
                {
                    'write_only': True
                }
        }

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user_obj = User(
            username = username,
        )
        user_obj.set_password(password)
        user_obj.save()

        return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=True, allow_blank=True)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
        ]
        extra_kwargs = {
            'password':
                {
                    'write_only': True
                }
        }

    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data['password']

        user = User.objects.filter(username = username)

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('This phone number has not be registered.')

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Invalid credentials, please try again.')

        data['username'] = user_obj.username
        data['token'] = Token.objects.get(user=user_obj)
        return data