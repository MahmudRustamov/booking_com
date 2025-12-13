from django.db import models
from apps.hotels.models.hotels import HotelsModel
from core import settings


class HotelReview(models.Model):
    hotel = models.ForeignKey(
        HotelsModel, on_delete=models.CASCADE, related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hotel_reviews'
    )
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.hotel.name} ({self.rating})"


