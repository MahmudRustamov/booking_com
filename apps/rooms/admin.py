from django.contrib import admin

from apps.rooms.models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'name', 'room_type', 'price_per_night', 'is_available')
    list_filter = ('room_type', 'is_available', 'hotel')
    search_fields = ('name', 'description')
    ordering = ('price_per_night',)
