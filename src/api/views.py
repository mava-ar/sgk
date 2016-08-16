from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics

from turnos.models import Turno
from .serializers import UserSerializer, GroupSerializer, TurnoSerializer, TurnoCalendarSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer


# class TurnoCalendarList(generics.ListCreateAPIView):
#     queryset = Turno.objects.all()
#     serializer_class = TurnoCalendarSerializer
#
#
# class TurnoCalendarDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Turno.objects.all()
#     serializer_class = TurnoCalendarSerializer


class TurnoCalendarSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Turno.objects.all()
    serializer_class = TurnoCalendarSerializer
    http_method_names = ['get', 'put', ]
