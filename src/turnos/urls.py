from django.conf.urls import url

from turnos import views


urlpatterns = [
    url(r'^$', views.turno_list, name='turno_list'),
    url(r'^nuevo/$', views.turno_create, name='turno_create'),
    url(r'^reporte/$', views.turno_report, name='turno_report'),
    url(r'^editar/(?P<pk>\d+)/$', views.turno_update, name="turno_update"),
    url(r'^eliminar/(?P<pk>\d+)/$', views.turno_delete, name="turno_delete"),
]
