from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

class CommentLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class CommentPageNumberPagination(PageNumberPagination):
    page_size = 20