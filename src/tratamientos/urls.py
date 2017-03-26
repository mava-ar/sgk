from django.conf.urls import url, include

from tratamientos import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/tratamientos/$', views.tratamiento_list, name="tratamiento_list"),
    url(r'^(?P<pk>\d+)/tratamientos/nuevo/$', views.tratamiento_create, name="tratamiento_create"),
    url(r'^(?P<pk>\d+)/tratamientos/(?P<pk_motivo>\d+)/$', views.tratamiento_update,
        name="tratamiento_update"),
    url(r'^(?P<pk>\d+)/tratamientos/(?P<pk_motivo>\d+)/finalizar/$', views.tratamiento_finish,
        name="tratamiento_finish"),
    url(r'^(?P<pk>\d+)/tratamientos/(?P<pk_motivo>\d+)/planificar_sesiones/$', views.planificacion_add,
        name="planificacion_add"),
    url(r'^(?P<pk>\d+)/tratamientos/(?P<pk_motivo>\d+)/nueva_sesion/$', views.sesion_create,
        name="sesion_create"),
    url(r'^(?P<pk>\d+)/tratamientos/(?P<pk_turno>\d+)/sesion_perdida/$', views.sesion_perdida_create,
        name="sesion_perdida_create"),
    url(r'^(?P<pk>\d+)/tratamientos/(?P<pk_motivo>\d+)/terminar_sesion/$', views.sesion_save_close,
        name="sesion_save_close"),
    # sesiones
    url(r'^(?P<pk>\d+)/sesiones/(?P<pk_sesion>\d+)/eliminar/$', views.sesion_delete,
        name="sesion_delete"),
    url(r'^(?P<pk>\d+)/sesiones/(?P<pk_sesion>\d+)/editar/$', views.sesion_update,
        name="sesion_update"),
    # url(r'^fichakinesica/(?P<pk>\d+)/tratamientos/(?P<pk_motivo>\d+)/planificacion/$', views.planificacion_create,
    #     name="planificacion_create"),
    url(r'^(?P<pk>\d+)/objetivos/(?P<pk_objetivo>\d+)/$', views.objetivo_update,
        name="objetivo_update"),
    url(r'^(?P<pk>\d+)/objetivos/(?P<pk_objetivo>\d+)/cumplido$', views.objetivo_cumplido_toggle,
        name="objetivo_cumplido_toggle")
]
