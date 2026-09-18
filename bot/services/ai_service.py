import logging
from typing import Dict, List

from asgiref.sync import sync_to_async

from bot.nlp.llm_client import LLMClient
from bot.nlp.rag.vector_search import (get_document_chunks_context,
                                       get_faq_answer, is_relevant_faq,
                                       search_document_chunks, search_faq)

logger = logging.getLogger(__name__)

llm_client = LLMClient()


async def process_question(
    message_text: str,
    messages: List[Dict],
) -> tuple[str, List[Dict]]:

    new_messages = messages.copy()
    new_messages.append({"role": "user", "content": message_text})

    # Find matching FAQ
    faq_results = await sync_to_async(search_faq)(message_text, limit=1)

    logger.info(
        "FAQ search: query=%r, results=%d",
        message_text,
        len(faq_results),
    )

    faq_context = ""

    if faq_results:
        faq_similarity = 1 - faq_results[0].distance

        logger.info(
            "FAQ result: distance=%.4f, similarity=%.4f, relevant=%s",
            faq_results[0].distance,
            faq_similarity,
            is_relevant_faq(faq_results[0].distance),
        )

    if faq_results and is_relevant_faq(faq_results[0].distance):
        # Extract information from FAQ
        faq_context = await sync_to_async(get_faq_answer)(faq_results)

        logger.info(
            "Using FAQ context: length=%d",
            len(faq_context),
        )

    if faq_context:
        # Send question and context to the LLM
        response = await llm_client.get_response(
            question=message_text,
            context=faq_context,
        )

        logger.info("Response generated using FAQ")

    else:
        # Semantic search by documents
        document_results = await sync_to_async(search_document_chunks)(
            message_text,
            limit=5,
        )

        logger.info(
            "Document search: query=%r, results=%d",
            message_text,
            len(document_results),
        )

        if document_results:
            logger.info(
                "Document results: %s",
                [
                    {
                        "similarity": round(1 - result.distance, 4),
                        "chunk_index": result.chunk_index,
                        "content": result.content,
                    }
                    for result in document_results
                ],
            )

        document_context = await sync_to_async(get_document_chunks_context)(
            document_results,
        )

        logger.info(
            "Document context: exists=%s, length=%d",
            bool(document_context),
            len(document_context),
        )

        if document_context:
            logger.info(
                "LLM context for query %r:\n%s",
                message_text,
                document_context,
            )

            response = await llm_client.get_response(
                question=message_text,
                context=document_context,
            )

            logger.info(
                "LLM response for query %r: %r",
                message_text,
                response,
            )

            logger.info("Response generated using document context")

        else:
            logger.info(
                "No relevant document context found. Using fallback."
            )

            response = (
                "К сожалению, у меня нет информации по этому вопросу. "
                "Пожалуйста, обратитесь к сотруднику отеля."
            )

    new_messages.append({"role": "assistant", "content": response})
    return response, new_messages
