from django.urls import path, re_path

from turnos import views

urlpatterns = [
    path('', views.turno_list, name='turno_list'),
    path('nuevo/', views.turno_create, name='turno_create'),
    path('reporte/', views.turno_report, name='turno_report'),
    path('editar/<int:pk>/', views.turno_update, name="turno_update"),
    path('eliminar/<int:pk>/', views.turno_delete, name="turno_delete"),
]
