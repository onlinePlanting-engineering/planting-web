from rest_framework import viewsets, status
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

    def list(self, request, *args, **kwargs):
        categories = Category.objects.all().order_by('-id')
        serializer = self.get_serializer(categories, many=True)
        return Response({
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class VegetableViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This API just provide list and retrieve specific vegetable information
    """
    queryset = Vegetable.objects.all()
    serializer_class = VegetableSerializer

    def list(self, request, *args, **kwargs):
        vegetables = Vegetable.objects.all().order_by('-id')
        serializer = self.get_serializer(vegetables, many=True)
        return Response({
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class VegMetaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This API just provide list and retrieve specific vegetable metas information
    """
    queryset = VegMeta.objects.all()
    serializer_class = VegMetaSerializer

    def list(self, request, *args, **kwargs):
        vegmetas = VegMeta.objects.all().order_by('-id')
        serializer = self.get_serializer(vegmetas, many=True)
        return Response({
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class VegMetaImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This API just provide list and retrieve specific vegetable information
    """
    queryset = VegMetaImage.objects.all()
    serializer_class = VegMetaImageSerializer

    def list(self, request, *args, **kwargs):
        vegmetaimages = VegMetaImage.objects.all().order_by('-id')
        serializer = self.get_serializer(vegmetaimages, many=True)
        return Response({
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)