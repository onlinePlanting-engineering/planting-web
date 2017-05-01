from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import re
from accounts.models import Profile

from rest_framework.serializers import (
ModelSerializer,
ValidationError,
CharField,
)

User = get_user_model()

class ProfileSerializer(ModelSerializer):
    class Meta:
        fields = [
            'nickname',
            'gender',
            'addr',
            'img_heading'
        ]
        model = Profile

class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]



class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'profile')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.save()

        profile.nickname = profile_data.get('nickname', profile.nickname)
        profile.addr = profile_data.get('addr', profile.addr)
        profile.gender = profile_data.get('gender', profile.gender)

        profile.img_heading = profile_data.get('img_heading', profile.img_heading)

        profile.save()

        return instance

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

    def validate(self, data):
        username = data.get('username')
        pattern = re.compile(r'^1[34578]\d{9}$')

        if not pattern.match(username):
            raise ValidationError('Please input a valid phone number.')
        return data

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
    token = CharField(allow_blank=True, read_only=True, validators=[])
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
