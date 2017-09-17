from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from apps.home.views import index as index_view
from apps.clients import views as client_views


router = routers.DefaultRouter()
router.register(r'clients', client_views.ClientViewSet, base_name='clients')


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.home.urls')),
]
