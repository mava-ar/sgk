from django.conf.urls import url

from coberturas_medicas import views

urlpatterns = [
    url(r'^$', views.cobertura_list, name='cobertura_list'),
    url(r'^nueva$', views.cobertura_create, name='cobertura_create'),
    url(r'^editar/(?P<pk>\d+)/$', views.cobertura_update, name="cobertura_update"),
]
