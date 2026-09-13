from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance
from apps.support.models import FAQ, DocumentChunk


FAQ_SIMILARITY_THRESHOLD = 0.45
DOCUMENT_CHUNK_SIMILARITY_THRESHOLD = 0.45


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


def is_relevant_document_chunk(distance: float) -> bool:
    similarity = calculate_similarity(distance)

    return similarity > DOCUMENT_CHUNK_SIMILARITY_THRESHOLD


def get_faq_answer(results) -> str:
    for item in results:
        if is_relevant_faq(item.distance):
            return item.answer

    return "Информация по данному вопросу не найдена."


def get_query_embedding(query_text: str) -> list[float]:
    return model.encode(
        query_text.strip()
    ).tolist()


def search_document_chunks(query_text: str, limit: int = 1) -> list[DocumentChunk]:

    query_embedding = get_query_embedding(query_text)

    return list(
        DocumentChunk.objects
        .filter(
            embedding__isnull=False,
        )
        .annotate(
            distance=CosineDistance(
                "embedding",
                query_embedding,
            )
        )
        .order_by("distance")[:limit]
    )


def get_document_chunks_context(results: list[DocumentChunk]) -> str:
    relevant_chunks = [
        chunk.content
        for chunk in results
        if is_relevant_document_chunk(chunk.distance)
    ]

    return "\n\n".join(relevant_chunks)