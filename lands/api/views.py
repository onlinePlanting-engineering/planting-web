from rest_framework import status
from rest_framework.response import Response
from rest_framework import (
    viewsets, permissions
)
from lands.models import Land, Meta
from .serializers import (
    LandSerializer,
    MetaSerializer
)

class LandViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This API view provide list and get specific land information
    """
    queryset = Land.objects.all()
    serializer_class = LandSerializer

    def list(self, request, *args, **kwargs):
        lands = Land.objects.all().order_by('-id')
        serializer = self.get_serializer(lands, many=True)
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

class MetaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Meta.objects.all()
    serializer_class = MetaSerializer

    def list(self, request, *args, **kwargs):
        metas = Meta.objects.all().order_by('-id')
        serializer = self.get_serializer(metas, many=True)
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

# class MetaImageViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = MetaImage.objects.all()
#     serializer_class = MetaImageSerializer
#
#     def list(self, request, *args, **kwargs):
#         metaimages = MetaImage.objects.all().order_by('-id')
#         serializer = self.get_serializer(metaimages, many=True)
#         return Response({
#             'data': serializer.data,
#             'status_code': status.HTTP_200_OK
#         }, status=status.HTTP_200_OK)
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response({
#             'data': serializer.data,
#             'status_code': status.HTTP_200_OK
#         }, status=status.HTTP_200_OK)