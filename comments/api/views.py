from django.db.models import Q
from rest_framework import (
    filters, status,
    generics, mixins,
    permissions
)
from comments.models import Comment
from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    CommentChildSerializer,
    create_comment_serializer
)
from accounts.permissions import IsOwnerOrReadOnly

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        id = self.request.GET.get('id')
        parent_id = self.request.GET.get('parent_id', None)
        return create_comment_serializer(
            model_type = model_type,
            id=id,
            parent_id = parent_id,
            user = self.request.user
        )

class CommentDetailAPIView(mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                           generics.RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_class = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [permissions.AllowAny, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'user__name']
    # pagination_class =
    queryset = Comment.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.filter(id__gte=0)
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains = query)|
                Q(user__name__icontains=query)
            ).distinct()
        return queryset_list