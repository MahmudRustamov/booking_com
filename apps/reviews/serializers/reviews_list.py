from rest_framework import serializers
from apps.reviews.models.hotel_reviews import HotelReview
from apps.reviews.models.room_reviews import RoomReview


class HotelReviewListSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = HotelReview
        fields = ['id', 'user_email', 'rating', 'comment', 'created_at']


class RoomReviewListSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = RoomReview
        fields = [
            'id',
            'user_email',
            'rating',
            'comment',
            'created_at'
        ]



