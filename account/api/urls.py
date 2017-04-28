from django.conf.urls import url

from .views import (
UserCreateAPIView,
UserLoginAPIView,
UserListAPIView,
UserLogoutAPIView,
)

urlpatterns = [
    url(r'^$', UserListAPIView.as_view(), name='list'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name='logout'),
]