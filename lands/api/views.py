from rest_framework import status
from rest_framework.response import Response
from rest_framework import (
    viewsets, permissions
)
from lands.models import Land, Meta, MetaImage
from .serializers import (
    LandSerializer,
    MetaSerializer,
    MetaImageSerializer
)

class LandViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This API view provide list and get specific land information
    """
    queryset = Land.objects.all()
    serializer_class = LandSerializer

class MetaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Meta.objects.all()
    serializer_class = MetaSerializer

class MetaImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MetaImage.objects.all()
    serializer_class = MetaImageSerializer