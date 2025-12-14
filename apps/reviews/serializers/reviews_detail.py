from rest_framework import serializers
from apps.reviews.models.hotel_reviews import HotelReview
from apps.reviews.models.room_reviews import RoomReview


class HotelReviewDetailSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = HotelReview
        fields = ['id', 'hotel', 'user', 'user_email', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']


class RoomReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomReview
        fields = ['rating', 'comment']


class RoomReviewDetailSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    hotel_name = serializers.CharField(source='room.hotel.name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)

    class Meta:
        model = RoomReview
        fields = ['id', 'room', 'user', 'user_email', 'hotel_name', 'room_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']



