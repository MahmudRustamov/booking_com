from django.contrib import admin

from apps.reviews.models.hotel_reviews import HotelReview
from apps.reviews.models.room_reviews import RoomReview


@admin.register(HotelReview)
class HotelReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'user', 'rating', 'comment', 'created_at')
    list_filter = ('rating', 'created_at', 'hotel')
    search_fields = ('user__email', 'hotel__name', 'comment')
    readonly_fields = ('created_at', 'user')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(RoomReview)
class RoomReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'get_hotel', 'user', 'rating', 'comment', 'created_at')
    list_filter = ('rating', 'created_at', 'room')
    search_fields = ('user__email', 'room__name', 'comment')
    readonly_fields = ('created_at', 'user')
    ordering = ('-created_at',)

    def get_hotel(self, obj):
        return obj.room.hotel.name

    get_hotel.short_description = 'Hotel'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


