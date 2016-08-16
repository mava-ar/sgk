from django.conf.urls import url, include
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'turnos', views.TurnoViewSet)
router.register(r'turnos-cal', views.TurnoCalendarSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
]
