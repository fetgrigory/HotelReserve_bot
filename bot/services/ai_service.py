from typing import List, Dict
from asgiref.sync import sync_to_async
from bot.nlp.rag.vector_search import search_faq, get_faq_answer


async def process_question(message_text: str,
                           messages: List[Dict]) -> tuple[str, List[Dict]]:
    new_messages = messages.copy()
    new_messages.append({"role": "user", "content": message_text})
    # Search FAQ and respond with the most relevant answer
    results = await sync_to_async(search_faq)(message_text, limit=1)
    if results:
        response = await sync_to_async(get_faq_answer)(results)
    else:
        response = "Информация по данному вопросу не найдена."

    new_messages.append({"role": "assistant", "content": response})
    return response, new_messages
