from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import re
from accounts.models import Profile

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CharField,
    IntegerField,
    ChoiceField
)
from django_filters.rest_framework import filters

User = get_user_model()

def phone_number(value):
    pattern = re.compile(r'^1[34578]\d{9}$')

    if not pattern.match(value):
        raise ValidationError('Not a valid phone number.')

class ProfileSerializer(ModelSerializer):
    gender = ChoiceField(
        choices=[0,1,2,3],
        style={'base_template': 'radio.html'}
    )
    class Meta:
        fields = [
            'nickname',
            'gender',
            'addr',
            'img_heading'
        ]
        model = Profile


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()
    username = CharField(max_length=24, min_length=8, validators=[phone_number])
    class Meta:
        model = User
        fields = ('id', 'username', 'profile')

        filter_backends = (filters.OrderingFilter)
        ordering_fields = ('id')
        ordering = ('-id')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.save()

        profile.nickname = profile_data.get('nickname', profile.nickname)
        profile.addr = profile_data.get('addr', profile.addr)
        profile.gender = profile_data.get('gender', profile.gender)

        img = profile_data.get('img_heading', None)
        if img:
            profile.img_heading = profile_data.get('img_heading', profile.img_heading)

        profile.save()

        return instance


class UserCreateSerializer(ModelSerializer):
    username = CharField(max_length=24, min_length=8, validators=[phone_number])
    password = CharField(min_length=6)
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
