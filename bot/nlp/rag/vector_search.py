from sentence_transformers import SentenceTransformer
from django.db import connection


# Uploading a model for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


# Search for similar objects using a text query
def search_contract(query_text: str, limit: int = 3) -> list:

    return []


# Formats the search results into a string for display to the user
def format_contract_results(results: list) -> str:
    if not results:
        return "Информация по договору не найдена."

    lines = []

    for idx, (text_chunk, similarity) in enumerate(results, 1):

        if similarity > 0.75:
            indicator = "🟢"
        elif similarity > 0.60:
            indicator = "🟡"
        else:
            indicator = "🟠"

        lines.append(
            f"{indicator} {idx}. {text_chunk[:200]}...\n"
            f"Релевантность: {similarity:.1%}"
        )

    return "\n\n".join(lines)