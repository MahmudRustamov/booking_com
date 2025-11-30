from apps.shared.models import BaseModel
from django.db import models

from apps.users.models.user import User


class Car(BaseModel):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    year = models.IntegerField()
    seats = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    availability = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')


    def __str__(self):
        return f"{self.brand} {self.name}"


    class Meta:
        verbose_name = 'car'
        verbose_name_plural = 'cars'
