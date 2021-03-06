from django.conf.urls import url, include

from frontend import views
from pacientes.views import historia_clinica_report_pdf


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^personas/$', views.persona_list, name='persona_list'),
    url(r'^personas/nueva/$', views.persona_create, name='persona_create'),
    url(r'^personas/editar/(?P<pk>\d+)/$', views.persona_update, name="persona_update"),
    url(r'^turnos/', include('turnos.urls')),

    url(r'^pacientes/$', views.paciente_list, name='paciente_list'),
    url(r'^pacientes/nuevo/$', views.paciente_create, name='paciente_create'),
    url(r'^pacientes/editar/(?P<pk>\d+)/$', views.paciente_update, name="paciente_update"),
    url(r'^coberturas/', include('coberturas_medicas.urls')),
    # plan nivel 2
    url(r'^pacientes/(?P<pk>\d+)/$', views.ficha_kinesica, name="ficha_kinesica"),
    url(r'^pacientes/(?P<pk>\d+)/historia-clinica/$', views.historia_clinica_list, name="historia_clinica_list"),
    url(r'^pacientes/(?P<pk>\d+)/historia-clinica/report-pdf/$', historia_clinica_report_pdf, name="historia_clinica_report_pdf"),
    url(r'^pacientes/(?P<pk>\d+)/antecedentes/$', views.ficha_kinesica_update, name="ficha_kinesica_update"),
    url(r'^pacientes/(?P<pk>\d+)/hc_comentario/$', views.comentario_hc_create, name="comentario_hc_create"),
    url(r'^pacientes/(?P<pk>\d+)/hc_comentario/(?P<pk_comentario>\d+)/$', views.comentario_hc_update, name="comentario_hc_update"),
    url(r'^pacientes/(?P<pk>\d+)/hc_imagen/$', views.imagen_hc_create, name="imagen_hc_create"),
    url(r'^pacientes/(?P<pk>\d+)/hc_imagen/(?P<pk_imagen>\d+)/$', views.imagen_hc_update, name="imagen_hc_update"),
    url(r'^fichakinesica/', include('tratamientos.urls')),
]
