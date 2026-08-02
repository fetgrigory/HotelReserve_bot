from asgiref.sync import sync_to_async
from apps.reviews.models import Review
from apps.users.models import User
from bot.nlp.sentiment_analyzer import analyze_review


# Inserts review with sentiment analysis
@sync_to_async
def insert_review(telegram_id, room_id, review_text):
    analysis = analyze_review(review_text)

    # Find existing user by Telegram ID
    user = User.objects.filter(
        telegram_id=telegram_id,
    ).first()

    if not user:
        return None

    # Create review with sentiment analysis results
    review = Review.objects.create(
        user=user,
        room_id=room_id,
        review_text=review_text,
        sentiment_label=analysis["label"],
        sentiment_score=analysis["score"],
    )

    return review
