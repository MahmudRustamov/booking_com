from rest_framework import serializers
from apps.rooms.models import Room
from apps.shared.mixins.translation_mixins import TranslatedFieldsReadMixin

class RoomTranslationMixin:
    translatable_fields = ['name', 'description']
    # media_fields = ['media_files']

class RoomDetailSerializer(RoomTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'id', 'hotel', 'room_type', 'name', 'description', 'max_guests', 'bed_type',
            'number_of_beds', 'price_per_night', 'currency', 'total_rooms', 'facilities',
            'is_available', 'images'
        ]

    def get_images(self, obj):
        return [media.file.url for media in obj.media_files.all()]
