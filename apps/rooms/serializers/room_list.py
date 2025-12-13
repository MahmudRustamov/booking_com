from rest_framework import serializers
from apps.shared.models import Media
from apps.rooms.models import Room


class RoomCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Room
        fields = [
            'id', 'hotel', 'room_type', 'name', 'description', 'max_guests',
            'bed_type', 'number_of_beds', 'price_per_night', 'currency',
            'total_rooms', 'facilities', 'is_available', 'images'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        room = super().create(validated_data)

        for image in images_data:
            room.media_files.create(file=image)
        return room


class RoomListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id', 'hotel', 'room_type', 'name', 'description', 'max_guests',
            'bed_type', 'number_of_beds', 'price_per_night', 'currency',
            'total_rooms', 'facilities', 'is_available', 'images'
        ]

    def get_images(self, obj):
        return [media.file.url for media in obj.media_files.all()]
