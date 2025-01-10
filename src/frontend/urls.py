from django.conf.urls import include
from django.urls import path

from frontend import views
from pacientes.views import historia_clinica_report_pdf


urlpatterns = [
    path('', views.index, name='index'),
    path('personas/', views.persona_list, name='persona_list'),
    path('personas/nueva/', views.persona_create, name='persona_create'),
    path('personas/editar/<int:pk>/', views.persona_update, name="persona_update"),
    path('turnos/', include('turnos.urls')),

    path('pacientes/', views.paciente_list, name='paciente_list'),
    path('pacientes/nuevo/', views.paciente_create, name='paciente_create'),
    path('pacientes/editar/<int:pk>/', views.paciente_update, name="paciente_update"),
    path('coberturas/', include('coberturas_medicas.urls')),
    # plan nivel 2
    path('pacientes/<int:pk>/', views.ficha_kinesica, name="ficha_kinesica"),
    path('pacientes/<int:pk>/historia-clinica/', views.historia_clinica_list, name="historia_clinica_list"),
    path('pacientes/<int:pk>/historia-clinica/report-pdf/', historia_clinica_report_pdf, name="historia_clinica_report_pdf"),
    path('pacientes/<int:pk>/antecedentes/', views.ficha_kinesica_update, name="ficha_kinesica_update"),
    path('pacientes/<int:pk>/hc_comentario/', views.comentario_hc_create, name="comentario_hc_create"),
    path('pacientes/<int:pk>/hc_comentario/<int:pk_comentario>/', views.comentario_hc_update, name="comentario_hc_update"),
    path('pacientes/<int:pk>/hc_imagen/', views.imagen_hc_create, name="imagen_hc_create"),
    path('pacientes/<int:pk>/hc_imagen/<int:pk_imagen>/', views.imagen_hc_update, name="imagen_hc_update"),
    path('fichakinesica/', include('tratamientos.urls')),
]
