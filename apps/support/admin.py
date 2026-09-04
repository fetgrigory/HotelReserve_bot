from django.contrib import admin

from bot.nlp.rag.document_parser import DocumentProcessor
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

    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)
            return

        uploaded_file = form.cleaned_data["file"]

        # Save file to storage without creating DocumentChunk yet
        obj.file.save(
            uploaded_file.name,
            uploaded_file,
            save=False,
        )

        # Process PDF and create chunks in DB
        DocumentProcessor.process(
            file_path=obj.file.path,
            document_title=obj.document_title,
            file_name=obj.file.name,
        )
