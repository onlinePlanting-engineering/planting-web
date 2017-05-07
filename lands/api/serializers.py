from rest_framework import serializers
from lands.models import Land, Meta, MetaImage

class MetaImageSerializer(serializers.ModelSerializer):
    meta = serializers.ReadOnlyField(source='meta.num')

    class Meta:
        model = MetaImage
        fields = ('image', 'created_date', 'meta')

class MetaSerializer(serializers.ModelSerializer):
    # images = serializers.HyperlinkedRelatedField(many=True, view_name='metaimage-detail', read_only=True)
    images = MetaImageSerializer(many=True, read_only=True)

    class Meta:
        model = Meta
        fields = ('url', 'num', 'owner', 'land', 'size',
                  'price', 'is_rented', 'images')

class LandSerializer(serializers.ModelSerializer):
    farm = serializers.ReadOnlyField(source='farm.name')
    # metas = serializers.HyperlinkedRelatedField(many=True, view_name='meta-detail', read_only=True)
    metas = MetaSerializer(many=True, read_only=True)

    class Meta:
        model = Land
        fields = ('id', 'url', 'farm', 'cat', 'size', 'is_active', 'metas')