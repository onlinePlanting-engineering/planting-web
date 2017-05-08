from rest_framework import viewsets
from rest_framework.response import Response

from seeds.models import Category, Vegetable, VegMeta, VegMetaImage

from .serializers import (
    CategorySerializer,
    VegetableSerializer,
    VegMetaSerializer,
    VegMetaImageSerializer
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This API view provide list and get specific seed category information
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class VegetableViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This API just provide list and retrieve specific vegetable information
    """
    queryset = Vegetable.objects.all()
    serializer_class = VegetableSerializer

class VegMetaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This API just provide list and retrieve specific vegetable metas information
    """
    queryset = VegMeta.objects.all()
    serializer_class = VegMetaSerializer

class VegMetaImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This API just provide list and retrieve specific vegetable information
    """
    queryset = VegMetaImage.objects.all()
    serializer_class = VegMetaImageSerializer