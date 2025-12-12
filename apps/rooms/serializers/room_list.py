from rest_framework import serializers
from apps.rooms.models import Room


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


