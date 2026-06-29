from django.contrib import admin
from .models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active", "created_at")
    search_fields = ("question", "answer")
    list_filter = ("is_active",)
    fields = ("question", "answer", "is_active")
