from rest_framework import status
from rest_framework.response import Response
from rest_framework import (
    viewsets, permissions,
    decorators, renderers,
)
from accounts.permissions import IsOwnerOrReadOnly
from farm.models import Farm, FarmImage
from .serializers import FarmSerializer, FarmImageSerializer


class FarmViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This API just provide list and get specific farm information
    """
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

    @decorators.detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def notice(self, request, *args, **kwargs):
        farm = self.get_object()
        return Response(farm.notice)

    @decorators.detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def content(self, request, *args, **kwargs):
        farm = self.get_object()
        return Response(farm.content)

    def list(self, request, *args, **kwargs):
        query_set = Farm.objects.all().order_by('-id')

        # Filter by username
        username = request.query_params.get('username', None)
        if username is not None:
            query_set = query_set.filter(owner__username=username)

        serializer = self.get_serializer(query_set, many=True)

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

class FarmImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FarmImage.objects.all()
    serializer_class = FarmImageSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly)
