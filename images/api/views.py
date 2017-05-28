from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ImageGroupSerializer, ImageSerializer
from images.models import Image, ImageGroup

class ImageGroupViewSet(ReadOnlyModelViewSet):
    queryset = ImageGroup.objects.filter(id__gte=0)
    serializer_class = ImageGroupSerializer

class ImageViewSet(ReadOnlyModelViewSet):
    queryset = Image.objects.filter(id__gte=0)
    serializer_class = ImageSerializer
