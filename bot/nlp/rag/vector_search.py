from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance
from apps.support.models import FAQ

# Uploading a model for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


def search_faq(query_text: str, limit: int = 1) -> list:
    # Generate query embedding
    query_embedding = model.encode(query_text).tolist()

    # Vector search with cosine distance
    results = FAQ.objects.filter(
        is_active=True,
        embedding__isnull=False
    ).annotate(
        distance=CosineDistance("embedding", query_embedding)
    ).order_by("distance")[:limit]

    search_results = []

    for item in results:
        # Convert distance to similarity
        similarity = 1 - item.distance
        search_results.append((item.answer, similarity))

    return search_results


def format_faq_results(results: list) -> str:
    # Checking match quality
    if results[0][1] < 0.7:
        return "Информация не найдена."

    return results[0][0]
