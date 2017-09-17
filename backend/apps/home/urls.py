from django.conf.urls import url, include
from apps.home.views import index as index_view


urlpatterns = [
    url(r'^.*?', index_view, name='index'),
]
