from django.db import models

from apps.shared.models import BaseModel
from apps.users.models.user import User


class Owners(BaseModel):
    ROLE_CHOICES = [
        ('hotel', 'Hotel Owner'),
        ('car', 'Car Owner'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='owners',
        null=True,
        blank=True
    )

    company_name = models.CharField(max_length=200)
    business_license = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=100)
    email = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'owner'
        verbose_name_plural = 'owners'

