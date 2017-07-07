from rest_framework import status
from rest_framework.response import Response
from rest_framework import (
    viewsets, permissions,
    decorators, renderers, generics
)
from accounts.permissions import IsOwnerOrReadOnly
from farm.models import Farm, FarmImage
from .serializers import FarmSerializer, FarmImageSerializer


class FarmViewSet(viewsets.ModelViewSet):
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        data = request.data

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        self.perform_unserialized_fields(instance, data)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_unserialized_fields(self, instance, data):
        # Update farm notice and content field
        notice = data.get('notice', None)
        content = data.get('content', None)

        if notice:
            instance.notice = notice
        if content:
            instance.content = content
        if notice or content:
            instance.save()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = Farm.objects.get(pk=serializer.data.id)
        self.perform_unserialized_fields(instance, data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class FarmImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FarmImage.objects.all()
    serializer_class = FarmImageSerializer
