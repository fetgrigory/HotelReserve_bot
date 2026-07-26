from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # List display
    list_display = (
        "id",
        "user_id_display",
        "room_id_display",
        "sentiment_display",
        "date",
    )

    # Search fields
    search_fields = (
        "review_text",
        "user__first_name",
        "user__last_name",
        "user__phone",
    )

    # List filters
    list_filter = (
        "sentiment_label",
        "date",
    )

    # Read-only fields
    readonly_fields = (
        "id",
        "user",
        "room",
        "review_text",
        "sentiment_label",
        "sentiment_score",
        "date",
    )

    # Fieldsets
    fieldsets = (
        (
            "Информация об отзыве",
            {
                "fields": (
                    "id",
                    "user",
                    "room",
                    "review_text",
                )
            },
        ),
        (
            "Анализ тональности",
            {
                "fields": (
                    "sentiment_label",
                    "sentiment_score",
                )
            },
        ),
        (
            "Дата",
            {
                "fields": (
                    "date",
                )
            },
        ),
    )

    # User ID
    @admin.display(description="ID пользователя")
    def user_id_display(self, obj):
        return obj.user.id

    # Room ID
    @admin.display(description="ID номера")
    def room_id_display(self, obj):
        return obj.room.id

    # Sentiment score
    @admin.display(description="Оценка")
    def sentiment_display(self, obj):
        return f"{obj.sentiment_label} ({obj.sentiment_score})"

    # Disable adding
    def has_add_permission(self, request):
        return False

    # Disable editing
    def has_change_permission(self, request, obj=None):
        return False

    # Disable deleting
    def has_delete_permission(self, request, obj=None):
        return False
