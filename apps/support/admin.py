from django.contrib import admin
from .models import FAQ, DocumentChunk


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active", "created_at")
    search_fields = ("question", "answer")
    list_filter = ("is_active",)
    fields = ("question", "answer", "is_active")


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ("document_title", "chunk_index", "created_at")
    search_fields = ("document_title", "content")
    list_filter = ("document_title",)
    fields = ("document_title", "file")
