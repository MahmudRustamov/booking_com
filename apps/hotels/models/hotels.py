from django.contrib.contenttypes.fields import GenericRelation

from apps.shared.models import BaseModel, Media
from django.db import models
from apps.users.models.user import User


class HotelOwner(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    business_license = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name


    class Meta:
        verbose_name = 'hotel owner'
        verbose_name_plural = 'hotel owners'




class HotelsModel(BaseModel):
    HOTEL_TYPES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('hostel', 'Hostel'),
        ('guesthouse', 'Guest House'),
    )

    STAR_RATINGS = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=200)
    hotel_type = models.CharField(max_length=20, choices=HOTEL_TYPES, default='hotel')
    description = models.TextField()

    media_files = GenericRelation(
        'shared.Media',related_query_name='hotels'
    )

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)

    star_rating = models.IntegerField(choices=STAR_RATINGS, null=True, blank=True)
    total_reviews = models.IntegerField(default=0)

    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='12:00')
    cancellation_policy = models.TextField(default='Free cancellation up to 24 hours before check-in')

    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'hotel'
        verbose_name_plural = 'hotels'

    def __str__(self):
        return self.name



