from django.conf.urls import url, include
from django.conf import settings

from frontend import views_public


urlpatterns = [
    url(r'^$', views_public.index, name='index'),
]
