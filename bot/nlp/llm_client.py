import logging
import os

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Ты — виртуальный консультант отеля.

Отвечай только на основании фрагментов документов ниже.
Не используй свои знания и ничего не придумывай.

Внимательно проверь все фрагменты перед ответом.
Если в документе есть условие, ограничение или исключение, обязательно учитывай его.

Если в документах есть ответ на вопрос — дай его, сохраняя смысл и важные условия.
Если ответа нет — ответь:
"К сожалению, у меня нет информации по этому вопросу. Пожалуйста, обратитесь к сотруднику отеля."

Отвечай кратко, одним-двумя предложениями.

Фрагменты документов:
{context}
"""


class LLMClient:
    def __init__(self) -> None:
        api_url = os.getenv("OLLAMA_API_URL")

        if not api_url:
            raise ValueError("OLLAMA_API_URL is not configured")

        self.client = AsyncOpenAI(
            base_url=f"{api_url}/v1",
            api_key="ollama",
        )
        self.model = "qwen2.5:3b"

    async def get_response(
        self,
        question: str,
        context: str,
    ) -> str:
        try:
            # Create request messages for the LLM
            messages: list[ChatCompletionMessageParam] = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT.format(context=context),
                },
                {
                    "role": "user",
                    "content": f"Вопрос пользователя:\n\n{question}",
                },
            ]

            # Get LLM response
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )

            return response.choices[0].message.content or ""

        except Exception:
            logger.exception("Error getting GPT response")

            return (
                "Извините, в данный момент я не могу ответить на ваш вопрос. "
                "Пожалуйста, попробуйте позже."
            )
