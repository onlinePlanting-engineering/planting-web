from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework import serializers

from comments.models import Comment
from accounts.api.serializers import UserSerializer, ProfileSerializer

User = get_user_model()

def create_comment_serializer(model_type='farm', id=None, parent_id=None, user=None):
    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'grade',
                'timestamp'
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.id = id
            self.parent_obj = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    self.parent_obj = parent_qs.first()
                    
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def Validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count():
                raise serializers.ValidationError('This is not a valid content type')
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=self.id)
            if not obj_qs.exists or obj_qs.count() != 1:
                raise serializers.ValidationError('This is not a slug for this content type')
            return data

        def create(self, validated_data):
            d = {}
            d['content'] = validated_data.get('content')
            d['grade'] = validated_data.get('grade')
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            id = self.id
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                model_type, id, d, main_user, parent_obj=parent_obj
            )
            return comment

    return CommentCreateSerializer

class CommentListSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name='comments-api:thread')
    url = serializers.CharField(source='get_api_url', read_only=True)
    reply_count = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    type = serializers.CharField(source='get_content_type_name', read_only=True)
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'url',
            'user',
            'content',
            'grade',
            'timestamp',
            'parent',
            'type',
            'object_id',
            'reply_count',
            'replies',
        ]

    def get_replies(self, obj):
        return None


    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentChildSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
        ]

class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    reply_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    type = serializers.CharField(source='get_content_type_name', read_only=True)
    url = serializers.CharField(source='get_api_url', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'url',
            'user',
            'content',
            'grade',
            'timestamp',
            'parent',
            'type',
            'object_id',
            'reply_count',
            'replies',

        ]

        read_only_fields = [
            'reply_count',
            'replies',
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentDetailSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0


class CommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            # 'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
            'timestamp',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0