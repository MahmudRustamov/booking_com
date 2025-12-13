from django.contrib.auth import authenticate
from rest_framework import serializers, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from apps.users.models.user import User, VerificationCode
from apps.users.utils.code_generators import (
    generate_unique_username,
    generate_verification_code,
    send_email
)


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("This email already registered")

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=generate_unique_username(),
            password=password,
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            is_active=False
        )

        code = generate_verification_code()
        VerificationCode.objects.create(user=user, code=code)

        send_email(receiver_email=user.email, body=f"Your code: {code}")

        return user


class VerifyCodeSerializer(serializers.Serializer):
    """Check verification code and activate user"""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        try:
            verification = VerificationCode.objects.filter(user=user, code=code, used=False).latest("created_at")
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired code")

        if not verification.is_valid():
            raise serializers.ValidationError("Verification code is expired")

        verification.used = True
        verification.save()
        user.is_active = True
        user.is_email_verified = True
        user.save()

        attrs["user"] = user
        return attrs



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Email or password is incorrect.")

        if not user.is_active:
            raise serializers.ValidationError("Email not verified.")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone_number",
            "first_name",
            "last_name",
            "middle_name",
            "date_of_birth",
            "role",
            "is_active",
            "is_email_verified",
            "is_phone_verified",
            "is_deleted",
            "is_staff",
            "is_superuser",
            "full_name",
        ]
        read_only_fields = ["id", "full_name", "is_staff", "is_superuser"]

