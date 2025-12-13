# serializers.py
from rest_framework import serializers
from apps.shared.models import Media
from apps.hotels.models.hotels import HotelsModel
from apps.shared.mixins.translation_mixins import TranslatedFieldsWriteMixin, TranslatedFieldsReadMixin


class HotelTranslationMixin:
    translatable_fields = ['name', 'description']
    # media_fields = ['media_fields']


class HotelCreateSerializer(TranslatedFieldsWriteMixin, serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = HotelsModel
        fields = [
            'id', 'owner', 'name', 'description', 'hotel_type', 'address', 'city',
            'country','postal_code', 'phone', 'email', 'website', 'star_rating',
            'check_in_time','check_out_time', 'cancellation_policy','is_active','images'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        hotel = super().create(validated_data)

        for image in images_data:
            hotel.media_files.create(file=image)
        return hotel


class HotelListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = HotelsModel
        fields = [
            'id', 'name', 'description', 'hotel_type', 'address', 'city', 'country', 'postal_code',
            'phone', 'email', 'website', 'star_rating', 'check_in_time', 'check_out_time',
            'cancellation_policy', 'is_active', 'images'
        ]

    def get_images(self, obj):
        return [media.file.url for media in obj.media_files.all()]



