from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.hotels.models.hotels import HotelsModel


class Room(models.Model):
    ROOM_TYPES = (
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('twin', 'Twin Room'),
        ('deluxe', 'Deluxe Room'),
        ('family', 'Family Room'),
    )

    BED_TYPES = (
        ('single', 'Single Bed'),
        ('double', 'Double Bed'),
        ('king', 'King Bed'),
        ('twin', 'Twin Beds'),
    )

    hotel = models.ForeignKey(HotelsModel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    name = models.CharField(max_length=100, help_text='e.g., Deluxe Ocean View')
    description = models.TextField()

    media_files = GenericRelation(
        'shared.Media', related_query_name='rooms'
    )

    max_guests = models.IntegerField()
    bed_type = models.CharField(max_length=20, choices=BED_TYPES)
    number_of_beds = models.IntegerField(default=1)

    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    total_rooms = models.IntegerField(default=1)

    facilities = models.TextField(blank=True, help_text='Comma-separated (AC, TV, Balcony, etc.)')

    is_available = models.BooleanField(default=True)


    class Meta:
        ordering = ['price_per_night']

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"
