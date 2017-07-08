"""planting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
admin.autodiscover()
from django.conf import settings
from django.conf.urls.static import static, serve
from rest_framework.routers import DefaultRouter
from filebrowser.sites import site as fb_site
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Planting Web API')

from rest_framework_jwt.views import obtain_jwt_token

from farm.api.views import FarmViewSet, FarmImageViewSet
from accounts.api.views import ProfileViewSet
from lands.api.views import LandViewSet, MetaViewSet
from seeds.api.views import CategoryViewSet, VegetableViewSet, VegMetaViewSet, VegMetaImageViewSet
from images.api.views import ImageGroupViewSet, ImageViewSet, CommonImageViewSet
from orders.api.views import OrderItemViewSet

from cameras.api.views import CameraViewSet

router = DefaultRouter()
router.register(r'farms', FarmViewSet)
# router.register(r'farmimages', FarmImageViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'land/lands', LandViewSet)
router.register(r'land/metas', MetaViewSet)
# router.register(r'metaimages', MetaImageViewSet)

router.register(r'seed/categories', CategoryViewSet)
router.register(r'seed/vegetables', VegetableViewSet)
router.register(r'seed/vegmetas', VegMetaViewSet)
# router.register(r'vegmetaimages', VegMetaImageViewSet)

router.register(r'image_groups', ImageGroupViewSet)
router.register(r'images', ImageViewSet)
router.register(r'common/images', CommonImageViewSet)

router.register(r'order_items', OrderItemViewSet)

router.register(r'cameras', CameraViewSet)

urlpatterns = [
    url(r'^docs/', schema_view),
    url(r'^api/', include(router.urls)),
    url(r'^api/comments/', include("comments.api.urls", namespace='comments-api')),
    url(r'^api/orders/', include("orders.api.urls", namespace='orders-api')),
    url(r'^admin/', include([
        url(r'^', include(admin.site.urls)),
        url(r'^filebrowser/', include(fb_site.urls))
    ])),
    url(r'^api/users/', include('accounts.api.urls', namespace='accounts-api')),
    url(r'^api/auth/token/', obtain_jwt_token),
    # url(r'^docs/', include('rest_framework_docs.urls')),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.extend([
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
    ])
