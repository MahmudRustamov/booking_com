from rest_framework import serializers
from apps.orders.models import RoomOrder


class RoomOrderSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name', read_only=True)
    hotel_name = serializers.CharField(source='room.hotel.name', read_only=True)

    class Meta:
        model = RoomOrder
        fields = [
            'id', 'room', 'room_name', 'hotel_name',
            'check_in', 'check_out', 'total_guests',
            'total_price', 'is_canceled', 'created_at'
        ]
        read_only_fields = ['total_price', 'created_at']

    def validate(self, data):
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        room = data.get('room')

        if check_in and check_out:
            if check_in >= check_out:
                raise serializers.ValidationError("Check-out must be after check-in.")

            overlapping = RoomOrder.objects.filter(
                room=room, is_canceled=False,
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            if overlapping.exists():
                raise serializers.ValidationError("Room is already booked for these dates.")

            days = (check_out - check_in).days
            data['total_price'] = room.price_per_night * days

        return data