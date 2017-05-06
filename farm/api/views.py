from rest_framework import status
from rest_framework.response import Response
from rest_framework import (
    viewsets, permissions,
    decorators, renderers,
)
from accounts.permissions import IsOwnerOrReadOnly
from farm.models import Farm, FarmImage
from .serializers import FarmSerializer, FarmImageSerializer


class FarmViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically profides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @decorators.detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def notice(self, request, *args, **kwargs):
        farm = self.get_object()
        return Response(farm.notice)

    @decorators.detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def content(self, request, *args, **kwargs):
        farm = self.get_object()
        return Response(farm.content)

class FarmImageViewSet(viewsets.ModelViewSet):
    queryset = FarmImage.objects.all()
    serializer_class = FarmImageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

