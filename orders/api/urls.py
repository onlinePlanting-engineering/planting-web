from django.conf.urls import url

from .views import (
    OrderCreateAPIView,
    OrderListAPIView,
    OrderDetailAPIView
)

urlpatterns = [
    url(r'^$', OrderListAPIView.as_view(), name='list'),
    url(r'^create/$', OrderCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', OrderDetailAPIView.as_view(), name='thread'),
]
