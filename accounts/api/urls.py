from django.conf.urls import url
from rest_framework_expiring_authtoken import views

from .views import (
UserCreateAPIView,
UserListAPIView,
UserLogoutAPIView,
reset_password
)

urlpatterns = [
    url(r'^$', UserListAPIView.as_view(), name='list'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', views.obtain_expiring_auth_token, name='login'),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name='logout'),
    url(r'^get_auth_token/$', views.obtain_expiring_auth_token, name='get_auth_token'),
    url(r'^reset_password', reset_password, name='reset_password')
]
