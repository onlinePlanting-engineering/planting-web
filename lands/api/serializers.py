from rest_framework import serializers
from lands.models import Land, Meta
from accounts.api.serializers import UserSerializer
from images.models import ImageGroup
from images.api.serializers import ImageGroupUrlSerializer

from cameras.api.serializers import CameraSerializer

# class MetaImageSerializer(serializers.ModelSerializer):
#     meta = serializers.ReadOnlyField(source='meta.num')
#
#     class Meta:
#         model = MetaImage
#         fields = ('img', 'created_date', 'meta')

class MetaSerializer(serializers.ModelSerializer):
    # images = MetaImageSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    imgs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Meta
        fields = ('url', 'num', 'owner', 'land', 'size',
                  'price', 'is_rented', 'imgs')

    def get_imgs(self, obj):
        img_grp_qs = ImageGroup.objects.filter_by_instance(obj)
        return ImageGroupUrlSerializer(img_grp_qs, many=True).data


class LandSerializer(serializers.ModelSerializer):
    farm = serializers.ReadOnlyField(source='farm.name')
    # metas = serializers.HyperlinkedRelatedField(many=True, view_name='meta-detail', read_only=True)
    metas = MetaSerializer(many=True, read_only=True)
    cameras = CameraSerializer(many=True, read_only=True)

    class Meta:
        model = Land
        fields = ('id', 'url', 'farm', 'cat', 'is_trusteed', 'size', 'name', 'desc','is_active', 'cameras', 'metas')