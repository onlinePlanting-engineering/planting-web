from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
import re
from accounts.models import Profile

from rest_framework import serializers

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    CharField,
    IntegerField,
    ChoiceField,
    Serializer,
    PrimaryKeyRelatedField
)
from django_filters.rest_framework import filters

User = get_user_model()

class UserFilteredPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(UserFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(owner=request.user)

def is_phone_number(value):
    pattern = re.compile(r'^1[34578]\d{9}$')

    if not pattern.match(value):
        raise ValidationError('Not a valid phone number.')

def is_phone_number_exists(value):
    qs = User.objects.filter(username=value)
    if qs.exists():
        raise ValidationError('The username has been registered')

class ProfileSerializer(ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        fields = [
            'id',
            # 'url',
            'owner',
            'nickname',
            'gender',
            'addr',
            'img_heading'
        ]
        model = Profile

    def update(self, instance, validated_data):
        nickname = validated_data.get('nickname', None)
        gender = validated_data.get('gender', None)
        addr = validated_data.get('addr', None)
        img_heading = validated_data.get('img_heading', None)

        if not nickname:
            nickname = instance.nickname
        if not gender:
            gender = instance.gender
        if not addr:
            addr = instance.addr
        if img_heading:
            instance.img_heading = img_heading

        instance.nickname = nickname
        instance.gender = gender
        instance.addr = addr
        instance.save()

        return  instance

class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()
    username = CharField(max_length=24, min_length=8, validators=[is_phone_number], allow_blank=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'profile')
        # fields = ('id', 'username')

        filter_backends = (filters.OrderingFilter)
        ordering_fields = ('id')
        ordering = ('-id')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        # if the updated username is not the same as the current username,
        # check if the updated username is '', if is '', do nothing
        # if the username set to some value and not equal to current value,
        # need to verify if the updated username is valid.
        # please use /api/users/change_username/ to update username
        # username = validated_data.get('username', None)
        # if username and username != instance.username:
        #     qs = User.objects.filter(username=username)
        #     if qs.exists():
        #         raise ValidationError('The username has been registered by others.')
        #     instance.username = username
        #     instance.save()

        nickname = profile_data.get('nickname')
        if not nickname:
            nickname = profile.nickname
        profile.nickname = nickname

        addr = profile_data.get('addr')
        if not addr:
            addr = profile.addr
        profile.addr = addr

        gender = profile_data.get('gender')
        if not gender:
            gender = profile.gender
        profile.gender = gender

        img = profile_data.get('img_heading', None)
        if img:
            profile.img_heading = profile_data.get('img_heading', profile.img_heading)

        profile.save()

        return instance

class UserCreateSerializer(ModelSerializer):
    username = CharField(max_length=24, min_length=8, validators=[is_phone_number, is_phone_number_exists])
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

class ChangeUsernameSerializer(Serializer):
    """
    Serializer for username change endpoint
    """
    username = CharField(max_length=24, min_length=8, validators=[is_phone_number])

class ResetPasswordSerializer(ModelSerializer):
    """
    Serializer for reset password for specific user
    """
    username = CharField(max_length=24, min_length=8, validators=[is_phone_number])
    password = CharField(min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance