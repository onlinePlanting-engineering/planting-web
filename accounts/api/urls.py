from django.conf.urls import url
from rest_framework_expiring_authtoken import views

from .views import (
    UserCreateAPIView,
    UserLogoutAPIView,
    UserViewSet,
    get_current_user_info,
    ChangeUsernameView,
    ResetPasswordView
)

user_list = UserViewSet.as_view({
    'get': 'list_users',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update'
})

urlpatterns = [
    url(r'^$', user_list, name='list'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', views.obtain_expiring_auth_token, name='login'),
    url(r'^logout/$', UserLogoutAPIView.as_view(), name='logout'),
    url(r'^get_auth_token/$', views.obtain_expiring_auth_token, name='get_auth_token'),
    url(r'^reset_password', ResetPasswordView.as_view(), name='reset_password'),
    url(r'^change_username', ChangeUsernameView.as_view(), name='change_username'),
    url(r'^(?P<pk>[0-9]+)/$', user_detail, name='detail'),
    url(r'^user_info/$', get_current_user_info, name='user_info'),
]
