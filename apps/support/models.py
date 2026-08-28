import logging
from django.db import models
from pgvector.django import VectorField
from sentence_transformers import SentenceTransformer

log = logging.getLogger(__name__)

# Uploading a model for embeddings
embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


# Frequently asked questions
class FAQ(models.Model):
    question = models.TextField(verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    embedding = VectorField(dimensions=384, null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def save(self, *args, **kwargs):
        # Generate embedding if created or updated
        text = self.question
        try:
            self.embedding = embedding_model.encode(text).tolist()
        except Exception as e:
            logging.error("Error generating embedding: %s", e)
            # Save even if embedding failed
        super().save(*args, **kwargs)

    # String representation for admin panel
    def __str__(self):
        return str(self.question)[:80]

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"


# Internal regulation document chunks
class DocumentChunk(models.Model):
    document_title = models.CharField(max_length=255, verbose_name="Название документа")
    file = models.FileField(upload_to="regulations/")
    content = models.TextField()
    chunk_index = models.IntegerField()
    embedding = VectorField(dimensions=384, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Пункт регламента"
        verbose_name_plural = "Внутренние регламенты"
        unique_together = ('document_title', 'chunk_index')

    def __str__(self):
        return f"{self.document_title} - Chunk {self.chunk_index}"
