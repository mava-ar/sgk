from django.urls import path

from tratamientos import views

urlpatterns = [
    path('<int:pk>/tratamientos/', views.tratamiento_list, name="tratamiento_list"),
    path('<int:pk>/tratamientos/nuevo/', views.tratamiento_create, name="tratamiento_create"),
    path('<int:pk>/tratamientos/<int:pk_motivo>/', views.tratamiento_update,
        name="tratamiento_update"),
    path('<int:pk>/tratamientos/<int:pk_motivo>/finalizar/', views.tratamiento_finish,
        name="tratamiento_finish"),
    path('<int:pk>/tratamientos/<int:pk_motivo>/planificar_sesiones/', views.planificacion_add,
        name="planificacion_add"),
    path('<int:pk>/tratamientos/<int:pk_motivo>/nueva_sesion/', views.sesion_create,
        name="sesion_create"),
    path('<int:pk>/tratamientos/<int:pk_turno>/sesion_perdida/', views.sesion_perdida_create,
        name="sesion_perdida_create"),
    path('<int:pk>/tratamientos/<int:pk_motivo>/terminar_sesion/', views.sesion_save_close,
        name="sesion_save_close"),
    # sesiones
    path('<int:pk>/sesiones/<int:pk_sesion>/eliminar/', views.sesion_delete,
        name="sesion_delete"),
    path('<int:pk>/sesiones/<int:pk_sesion>/editar/', views.sesion_update,
        name="sesion_update"),
    # path('fichakinesica/<int:pk>/tratamientos/<int:pk_motivo>/planificacion/', views.planificacion_create,
    #     name="planificacion_create"),
    path('<int:pk>/objetivos/<int:pk_objetivo>/', views.objetivo_update,
        name="objetivo_update"),
    path('<int:pk>/objetivos/<int:pk_objetivo>/cumplido', views.objetivo_cumplido_toggle,
        name="objetivo_cumplido_toggle")
]
