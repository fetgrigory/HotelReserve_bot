from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    # Columns displayed in the booking list view
    list_display = (
        "id",
        "guest_display",
        "phone_display",
        "room_display",
        "start_date",
        "end_date",
        "rent_days",
        "total_price",
    )

    # Fields available for search
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__phone",
        "room__room_number",
    )

    # Filters available in the admin sidebar
    list_filter = (
        "start_date",
        "end_date",
        "room__category",
    )

    # Fields displayed in read-only mode
    readonly_fields = (
        "id",
        "user",
        "room",
        "start_date",
        "end_date",
        "rent_days",
        "total_price",
    )

    # Organize booking details into logical sections
    fieldsets = (
        (
            "Информация о госте",
            {
                "fields": (
                    "user",
                )
            },
        ),
        (
            "Информация о номере",
            {
                "fields": (
                    "room",
                )
            },
        ),
        (
            "Период проживания",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "rent_days",
                )
            },
        ),
        (
            "Стоимость",
            {
                "fields": (
                    "total_price",
                )
            },
        ),
    )

    # Display the guest's full name
    @admin.display(description="Гость")
    def guest_display(self, obj):
        return (
            f"{obj.user.first_name} "
            f"{obj.user.last_name}"
        )

    # Display the guest's phone number
    @admin.display(description="Телефон")
    def phone_display(self, obj):
        return obj.user.phone

    # Display the room category and number
    @admin.display(description="Номер")
    def room_display(self, obj):
        return (
            f"{obj.room.get_category_display()} "
            f"№{obj.room.room_number}"
        )

    # Disable creation of new bookings via the admin panel
    def has_add_permission(self, request):
        return False

    # Disable editing of existing bookings
    def has_change_permission(self, request, obj=None):
        return False

    # Disable deletion of bookings
    def has_delete_permission(self, request, obj=None):
        return False
