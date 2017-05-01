from django.conf.urls import url
from rest_framework_expiring_authtoken import views

from .views import (
    UserCreateAPIView,
    UserLogoutAPIView,
    UserViewSet,
    reset_password,
    get_current_user_info
)

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    url(r'^$', user_list, name='list'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', views.obtain_expiring_auth_token, name='login'),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name='logout'),
    url(r'^get_auth_token/$', views.obtain_expiring_auth_token, name='get_auth_token'),
    url(r'^reset_password', reset_password, name='reset_password'),
    url(r'^(?P<pk>[0-9]+)/$', user_detail, name='detail'),
    url(r'^user_info/$', get_current_user_info, name='user_info'),
]
