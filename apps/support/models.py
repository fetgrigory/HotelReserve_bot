from django.db import models
from pgvector.django import VectorField
from sentence_transformers import SentenceTransformer

# Uploading a model for embeddings
embedding_model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


# Frequently asked questions table with vector embeddings
class FAQ(models.Model):
    question = models.TextField(verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    embedding = VectorField(dimensions=384, null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def save(self, *args, **kwargs):
        # Generate embedding before save
        text = self.question
        self.embedding = embedding_model.encode(text).tolist()
        super().save(*args, **kwargs)

    # String representation for admin panel
    def __str__(self):
        return str(self.question)[:80]

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
