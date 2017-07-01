from django.db.models import Q
from rest_framework import (
    filters, status,
    generics, mixins,
    permissions
)
from rest_framework.response import Response
from comments.models import Comment
from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentChildSerializer,
    create_comment_serializer
)
from .pagination import CommentLimitOffsetPagination, CommentPageNumberPagination
from accounts.permissions import IsOwnerOrReadOnly

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        id = self.request.GET.get('id')
        parent_id = self.request.GET.get('parent_id', None)

        create_serializer = create_comment_serializer(
            model_type=model_type,
            id=id,
            parent_id=parent_id,
            user=self.request.user
        )

        return create_serializer

class CommentDetailAPIView(mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                           generics.RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_class = [IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(data={
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={
            'data': 'Deleted',
            'status_code': status.HTTP_204_NO_CONTENT
        }, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data={
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)

class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [permissions.AllowAny, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'user__name']
    # pagination_class = CommentPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get('q')

        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains = query)|
                Q(user__username__icontains=query)
            ).distinct()
        return queryset_list

    def list(self, request, *args, **kwargs):
        content_type = self.request.GET.get('type', None)
        object_id = self.request.GET.get('id', None)

        if not id or not content_type:
            return Response(data={
                'detail':'please specify content_type and content_id parameters. ex. ?type=farm&id=1',
                'status_code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter( Q(content_type__model__exact=content_type) & Q(object_id__exact=object_id) )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(data={
            'data': serializer.data,
            'status_code': status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
