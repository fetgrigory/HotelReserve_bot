from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance
from apps.support.models import FAQ


FAQ_SIMILARITY_THRESHOLD = 0.45


# Uploading a model for embeddings
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def search_faq(query_text: str, limit: int = 1) -> list:
    # Generate query embedding
    query_embedding = model.encode(query_text.lower()).tolist()

    # Vector search with cosine distance
    return list(
        FAQ.objects.filter(
            is_active=True,
            embedding__isnull=False
        ).annotate(
            distance=CosineDistance("embedding", query_embedding)
        ).order_by("distance")[:limit]
    )


def calculate_similarity(distance: float) -> float:
    # Convert distance to similarity
    return 1 - distance


def is_relevant_faq(distance: float) -> bool:
    similarity = calculate_similarity(distance)

    # Checking match quality
    return similarity > FAQ_SIMILARITY_THRESHOLD


def get_faq_answer(results) -> str:
    for item in results:
        if is_relevant_faq(item.distance):
            return item.answer

    return "Информация по данному вопросу не найдена."
