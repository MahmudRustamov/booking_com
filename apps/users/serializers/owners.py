from rest_framework import serializers
from apps.users.models.owners import Owners
from apps.users.models.user import User


class OwnerCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Owners
        fields = [
            "user",
            "first_name",
            "last_name",
            "company_name",
            "business_license",
            "bank_account",
            "email",
            "bio",
            "is_active",
        ]


class OwnerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owners
        fields = [
            "id",
            "company_name",
            "email",
            "created_at",
        ]


class OwnerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owners
        fields = "__all__"
