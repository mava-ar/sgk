from django.conf.urls import include
from django.urls import path
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'turnos-cal', views.TurnoCalendarSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
