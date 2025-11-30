from rest_framework import serializers

from apps.hotels.models.hotels import HotelsModel
from apps.shared.mixins.translation_mixins import TranslatedFieldsWriteMixin, TranslatedFieldsReadMixin


class HotelTranslationMixin:
    translatable_fields = ['name', 'description']
    media_fields = ['images']



class HotelCreateSerializer(TranslatedFieldsWriteMixin, serializers.ModelSerializer):
    class Meta:
        model = HotelsModel
        fields = [
            'id', 'name', 'description', 'hotel_type', 'address', 'city','country','postal_code',
            'phone', 'email','website','star_rating','check_in_time','check_out_time',
            'cancellation_policy','is_active',
        ]


class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelsModel
        fields = [
            'id', 'name', 'description', 'hotel_type', 'address', 'city', 'country', 'postal_code',
            'phone', 'email', 'website', 'star_rating', 'check_in_time', 'check_out_time',
            'cancellation_policy', 'is_active',
        ]

