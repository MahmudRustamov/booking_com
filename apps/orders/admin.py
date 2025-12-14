from django.contrib import admin
from apps.orders.models import RoomOrder

@admin.register(RoomOrder)
class RoomOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'room', 'check_in', 'check_out',
        'total_guests', 'total_price', 'is_canceled', 'created_at'
    )
    list_filter = ('is_canceled', 'check_in', 'check_out', 'room__hotel')
    search_fields = ('user__email', 'room__name', 'room__hotel__name')
    readonly_fields = ('total_price', 'created_at')
    ordering = ('-created_at',)

    actions = ['cancel_orders']

    def cancel_orders(self, request, queryset):
        updated = queryset.update(is_canceled=True)
        self.message_user(request, f"{updated} order canceled successfully.")
    cancel_orders.short_description = "Cancel selected orders"

