from farm.models import Farm, FarmImage
from rest_framework import serializers
from comments.models import Comment
from comments.api.serializers import CommentSerializer
from lands.models import Land

class FarmImageSerializer(serializers.ModelSerializer):
    # Create a custom method field, that list farms belong to current user
    # farm = UserFilteredPrimaryKeyRelatedField(queryset=Farm.objects, source='farm.name')

    class Meta:
        model = FarmImage
        fields = ('url', 'img', 'flags', 'is_delete', 'updated_date')

class FarmCommnetSerializer(serializers.ModelSerializer):

    url = serializers.CharField(source='get_api_url', read_only=True)

    class Meta:
        model = Comment
        fields = ('url',)

class FarmLandSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_api_url', read_only=True)
    class Meta:
        model = Land
        fields = ['url', ]

class FarmSerializer(serializers.ModelSerializer):
    # images = serializers.HyperlinkedRelatedField(many=True, view_name='farmimage-detail', read_only=True)
    images = FarmImageSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')
    notice = serializers.HyperlinkedIdentityField(view_name='farm-notice', format='html')
    content = serializers.HyperlinkedIdentityField(view_name='farm-content', format='html')
    comments = serializers.SerializerMethodField()
    lands = serializers.SerializerMethodField()

    class Meta:
        fields = ('url', 'id', 'name', 'owner', 'price', 'subject', 'addr', 'phone',
                  'is_delete', 'notice', 'content', 'images', 'comments', 'lands')

        model = Farm

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = FarmCommnetSerializer(c_qs, many=True).data
        return comments

    def get_lands(self, obj):
        lands_qs = Land.objects.filter(pk=obj.id)
        lands = FarmLandSerializer(lands_qs, many=True).data
        return lands