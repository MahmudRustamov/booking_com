from apps.hotels.models.hotels import HotelsModel
from apps.hotels.serializers.create_hotel import HotelTranslationMixin
from apps.shared.mixins.translation_mixins import TranslatedFieldsReadMixin
from rest_framework import serializers


class HotelDetailSerializer(HotelTranslationMixin, TranslatedFieldsReadMixin, serializers.ModelSerializer):
    class Meta:
        model = HotelsModel
        fields = [
            'id', 'name', 'description', 'hotel_type', 'address', 'city', 'country', 'postal_code',
            'phone', 'email', 'website', 'star_rating', 'check_in_time', 'check_out_time',
            'cancellation_policy', 'is_active',
        ]