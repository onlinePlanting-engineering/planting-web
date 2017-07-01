from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import CameraSerializer
from cameras.models import Camera

class CameraViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CameraSerializer
    queryset = Camera.objects.filter(pk__gte=0)