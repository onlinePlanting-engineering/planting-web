from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .serializers import ImageGroupSerializer, ImageSerializer, CommonImageSerializer
from images.models import Image, ImageGroup, CommonImage

class ImageGroupViewSet(ReadOnlyModelViewSet):
    queryset = ImageGroup.objects.filter(id__gte=0)
    serializer_class = ImageGroupSerializer

class ImageViewSet(ReadOnlyModelViewSet):
    queryset = Image.objects.filter(id__gte=0)
    serializer_class = ImageSerializer

class CommonImageViewSet(ModelViewSet):
    queryset = CommonImage.objects.filter(id__gte=0)
    serializer_class = CommonImageSerializer