from django.contrib.auth.models import User, Group
from rest_framework import serializers

from turnos.models import Turno


class TurnoCalendarSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    start = serializers.DateTimeField(source='datetime_start')
    end = serializers.DateTimeField(source='datetime_end')
    no_asistio = serializers.BooleanField()

    class Meta:
        model = Turno
        fields = ('id', 'title', 'start', 'end', 'no_asistio')

    def create(self, validated_data):
        raise PermissionError("No es posible crear turnos en este endpoint")

    def update(self, instance, validated_data):
        start = validated_data.get('datetime_start')
        end = validated_data.get('datetime_end')
        instance.duracion = int((end - start).seconds/60)
        instance.dia = start.date()
        instance.hora = start.time()
        instance.save()
        return instance
