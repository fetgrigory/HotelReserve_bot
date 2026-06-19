from django.db import models
from django.utils import timezone
from apps.users.models import User
from apps.rooms.models import Room


# Reviews table
class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    # Review details and sentiment analysis results
    review_text = models.TextField()
    sentiment_label = models.CharField(max_length=255)
    sentiment_score = models.FloatField()
    date = models.DateField(default=timezone.localdate)

    # String representation for admin panel
    def __str__(self):
        return f"Отзыв от пользователя {self.user} для номера {self.room}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
