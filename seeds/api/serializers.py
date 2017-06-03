from rest_framework import serializers
from seeds.models import Category, Vegetable, VegMeta, VegMetaImage
from images.models import ImageGroup
from images.api.serializers import ImageGroupUrlSerializer

class VegMetaImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = VegMetaImage
        fields = ('img', 'updated_date')

class VegMetaSerializer(serializers.ModelSerializer):
    # images = VegMetaImageSerializer(many=True, read_only=True)
    imgs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VegMeta
        fields = ('url', 'name', 'first_letter', 'stime', 'etime', 'cycle', 'region', 'output',
                  'seed_price', 'mature_price', 'desc', 'content', 'is_active', 'imgs')

    def get_imgs(self, obj):
        img_grp_qs = ImageGroup.objects.filter_by_instance(obj)
        return ImageGroupUrlSerializer(img_grp_qs, many=True).data

class VegetableSerializer(serializers.ModelSerializer):
    vegmetas = VegMetaSerializer(many=True, read_only=True)

    class Meta:
        model = Vegetable
        fields = ('url', 'name', 'vegmetas')

class CategorySerializer(serializers.ModelSerializer):
    vegetables = VegetableSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('url', 'name', 'vegetables')