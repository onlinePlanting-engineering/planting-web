from django.conf.urls import url
from rest_framework.authtoken import views as rest_framework_views

from .views import (
UserCreateAPIView,
UserLoginAPIView,
UserListAPIView,
UserLogoutAPIView,
)

urlpatterns = [
    url(r'^$', UserListAPIView.as_view(), name='list'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name='logout'),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
]
