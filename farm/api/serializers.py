from farm.models import Farm, FarmImage
from rest_framework import serializers
from comments.models import Comment
from comments.api.serializers import CommentSerializer
from lands.models import Land
from images.models import ImageGroup, Image
from images.api.serializers import ImageGroupUrlSerializer

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
    owner = serializers.ReadOnlyField(source='owner.username')
    notice = serializers.HyperlinkedIdentityField(view_name='farm-notice', format='html')
    content = serializers.HyperlinkedIdentityField(view_name='farm-content', format='html')
    comments = serializers.SerializerMethodField()
    lands = serializers.SerializerMethodField()
    imgs = serializers.SerializerMethodField()

    class Meta:
        fields = ('url', 'id', 'name', 'owner', 'price', 'subject', 'addr', 'phone',
                  'is_delete', 'notice', 'content', 'comments', 'lands', 'imgs', 'home_img_url')

        model = Farm

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = FarmCommnetSerializer(c_qs, many=True).data
        return comments

    def get_lands(self, obj):
        lands_qs = Land.objects.filter(farm=obj.id)
        lands = FarmLandSerializer(lands_qs, many=True).data
        return lands

    def get_imgs(self, obj):
        img_grp_qs = ImageGroup.objects.filter_by_instance(obj)
        img_grps = ImageGroupUrlSerializer(img_grp_qs, many=True).data
        return img_grps
