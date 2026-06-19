from asgiref.sync import sync_to_async
from apps.reviews.models import Review
from bot.nlp.sentiment_analyzer import analyze_review


# Inserts review with sentiment analysis
@sync_to_async
def insert_review(user_id, room_id, review_text):
    analysis = analyze_review(review_text)

    review = Review.objects.create(
        user_id=user_id,
        room_id=room_id,
        review_text=review_text,
        sentiment_label=analysis["label"],
        sentiment_score=analysis["score"]
    )

    return review
