from django.contrib import admin
from django.db.models import Count

from bot.nlp.rag.document_parser import parse_document

from .models import FAQ, Document, DocumentChunk


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active", "created_at")
    search_fields = ("question", "answer")
    list_filter = ("is_active",)
    fields = ("question", "answer", "is_active")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "chunk_count", "created_at")
    search_fields = ("title", )
    fields = ("title", "file")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            chunks_total=Count("chunks"))

    @admin.display(
        description="Количество чанков",
        ordering="chunks_total",
    )
    def chunk_count(self, obj):
        return obj.chunks_total

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            chunks = parse_document(obj.file.path)

            DocumentChunk.objects.bulk_create(
                [
                    DocumentChunk(
                        document=obj,
                        content=chunk.page_content,
                        chunk_index=index,
                    )
                    for index, chunk in enumerate(chunks)
                ]
            )
