from rest_framework import serializers
from apps.reviews.models.hotel_reviews import HotelReview



class HotelReviewListSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = HotelReview
        fields = ['id', 'user_email', 'rating', 'comment', 'created_at']

