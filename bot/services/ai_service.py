from typing import List, Dict
from asgiref.sync import sync_to_async
from bot.nlp.rag.vector_search import search_faq, get_faq_answer
from bot.nlp.llm_client import ask_gpt


async def process_question(message_text: str,
                           messages: List[Dict]) -> tuple[str, List[Dict]]:
    new_messages = messages.copy()
    new_messages.append({"role": "user", "content": message_text})

    # Find matching FAQ
    results = await sync_to_async(search_faq)(message_text, limit=1)

    if results:
        # Extract information from FAQ
        context = await sync_to_async(get_faq_answer)(results)

        # Send question and context to the LLM
        response = await sync_to_async(ask_gpt)(
            message_text,
            context
        )

    else:
        response = "Информация по данному вопросу не найдена."

    new_messages.append({"role": "assistant", "content": response})
    return response, new_messages
