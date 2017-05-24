from farm.models import Farm, FarmImage
from rest_framework import serializers
from accounts.api.serializers import (
    UserSerializer,
    UserFilteredPrimaryKeyRelatedField
)
from comments.models import Comment
from comments.api.serializers import CommentSerializer

class FarmImageSerializer(serializers.ModelSerializer):
    # Create a custom method field, that list farms belong to current user
    # farm = UserFilteredPrimaryKeyRelatedField(queryset=Farm.objects, source='farm.name')

    class Meta:
        model = FarmImage
        fields = ('url', 'img', 'flags', 'is_delete', 'updated_date')

class FarmSerializer(serializers.ModelSerializer):
    # images = serializers.HyperlinkedRelatedField(many=True, view_name='farmimage-detail', read_only=True)
    images = FarmImageSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    notice = serializers.HyperlinkedIdentityField(view_name='farm-notice', format='html')
    content = serializers.HyperlinkedIdentityField(view_name='farm-content', format='html')
    # comments = serializers.HyperlinkedIdentityField(view_name='comment-list', format='html')
    # comments = serializers.SerializerMethodField()

    class Meta:
        fields = ('url', 'id', 'name', 'owner', 'price', 'subject',
                  'is_delete', 'notice', 'content', 'images')

        model = Farm

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments