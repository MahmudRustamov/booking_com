from django.db import models
from django.conf import settings
from apps.rooms.models import Room

class RoomOrder(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='room_orders')
    check_in = models.DateField()
    check_out = models.DateField()
    total_guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.room.name} ({self.check_in} to {self.check_out})"
