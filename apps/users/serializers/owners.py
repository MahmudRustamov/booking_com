from rest_framework import serializers

from apps.shared.mixins.translation_mixins import TranslatedFieldsWriteMixin
from apps.users.models.owners import Owners
from apps.users.models.user import User


class OwnersTranslationMixin:
    """Shared configuration for OnBoarding serializers"""
    translatable_fields = ['bio']
    media_fields = ['image']


class OwnersCreateSerializer(TranslatedFieldsWriteMixin, serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Owners
        fields = [
            'user',
            'first_name',
            'last_name',
            'company_name',
            'business_license',
            'bank_account',
            'email',
            'bio',
            'is_active',
        ]


class OwnersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owners
        fields = [
            'id',
            'first_name',
            'last_name',
            'company_name',
            'business_license',
            'bank_account',
            'email',
            'bio',
            'is_active',
        ]