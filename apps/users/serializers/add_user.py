from rest_framework import serializers
from apps.hotels.models.hotels import HotelOwner


class HotelOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOwner
        fields = [
            'id',
            'user',        
            'company_name',
            'business_license',
            'tax_id',
            'bank_account',
        ]
        read_only_fields = ['id']
