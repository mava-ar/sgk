from django.urls import path

from frontend import views_public


urlpatterns = [
    path('', views_public.index, name='index'),
]
