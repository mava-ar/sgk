from django.conf.urls import url, include

from frontend import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sobre/$', views.about, name='about'),
    url(r'^personas/$', views.persona_list, name='persona_list'),
    url(r'^personas/nueva$', views.persona_create, name='persona_create'),
    url(r'^turnos/$', views.turno_list, name='turno_list'),
    url(r'^turnos/nuevo$', views.turno_create, name='turno_create'),
    url(r'^turnos/editar/(?P<pk>\d+)/$', views.turno_update, name="turno_update"),
    url(r'^pacientes/$', views.paciente_list, name='paciente_list'),
    url(r'^pacientes/nuevo$', views.paciente_create, name='paciente_create'),
    url(r'^pacientes/editar/(?P<pk>\d+)/$', views.paciente_update, name="paciente_update"),
    url(r'^fichakinesica/(?P<pk>\d+)/$', views.ficha_kinesica, name="ficha_kinesica"),
    url(r'^fichakinesica/(?P<pk>\d+)/antecedentes/$', views.ficha_kinesica_update, name="ficha_kinesica_update"),
    url(r'^fichakinesica/(?P<pk>\d+)/motivos/$', views.motivo_consulta, name="motivo_consulta"),
    url(r'^fichakinesica/(?P<pk>\d+)/motivos/nuevo/$', views.motivo_consulta_create, name="motivo_consulta_create"),
]
