from django.db import models
from pgvector.django import VectorField


# Frequently asked questions table with vector embeddings
class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    embedding = VectorField(dimensions=384, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation for admin panel
    def __str__(self):
        return str(self.question)[:80]

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
