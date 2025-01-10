from django.urls import path

from coberturas_medicas import views

urlpatterns = [
    path('', views.cobertura_list, name='cobertura_list'),
    path('nueva/', views.cobertura_create, name='cobertura_create'),
    path(r'editar/<int:pk>/', views.cobertura_update, name="cobertura_update"),
]
