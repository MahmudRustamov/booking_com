from django.contrib import admin

from django.contrib import admin
from apps.hotels.models.hotels import HotelsModel
from apps.shared.models import Media



@admin.register(HotelsModel)
class HotelsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'hotel_type',
        'city',
        'country',
        'star_rating',
        'is_active'
    )
    list_filter = ('hotel_type', 'star_rating', 'city', 'country', 'is_active')
    search_fields = ('name', 'description', 'city', 'country')
    ordering = ('-star_rating', 'name')
    readonly_fields = ('total_reviews',)


