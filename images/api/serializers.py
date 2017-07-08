from images.models import Image, ImageGroup, CommonImage
from rest_framework import serializers

class ImageGroupUrlSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_api_url', read_only=True)
    class Meta:
        model = ImageGroup
        fields = ['url',]

class ImageGroupSerializer(serializers.ModelSerializer):
    imgs = serializers.SerializerMethodField()

    class Meta:
        model = ImageGroup
        fields = ['id', 'desc', 'timestamp','imgs']

    def get_imgs(self, obj):
        return ImageSerializer(obj.imgs ,many=True).data

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class CommonImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonImage
        fields = '__all__'