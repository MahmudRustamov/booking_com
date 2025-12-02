from rest_framework import serializers

from apps.users.models.owners import Owners


class OwnerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owners
        fields = [
            "company_name",
            "business_license",
            "tax_id",
            "bank_account",
            "email",
            "role",
        ]


class OwnerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owners
        fields = [
            "id",
            "company_name",
            "email",
            "role",
            "created_at",
        ]


class OwnerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owners
        fields = "__all__"
