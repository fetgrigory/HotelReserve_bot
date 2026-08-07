import logging
import os

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Ты — виртуальный консультант отеля.

Твоя задача — помогать пользователям, отвечая только на основе предоставленного контекста.

Главное правило:
Контекст является единственным источником информации.
Ты не имеешь права использовать свои знания или делать предположения.

Правила ответа:

1. Если в контексте есть информация, которая отвечает на вопрос пользователя:

- используй только информацию из контекста;
- переформулируй её естественным и вежливым языком;
- отвечай как сотрудник службы поддержки отеля;
- можешь менять формулировку и порядок слов;
- не добавляй новые факты, которых нет в контексте.

2. Если в контексте нет ответа на вопрос пользователя:

- не пытайся угадать ответ;
- не объясняй, почему информации нет;
- не анализируй возможные причины;
- не предлагай варианты решения;
- не придумывай услуги, правила, цены, условия, контакты или инструкции.

В этом случае ответь строго одной фразой:

"К сожалению, у меня нет информации по этому вопросу. Пожалуйста, обратитесь к сотруднику отеля."

Не изменяй эту фразу и не добавляй к ней дополнительные предложения.

Запрещено:

- придумывать факты;
- добавлять информацию от себя;
- дополнять ответ логическими предположениями;
- писать о платных или бесплатных условиях, если этого нет в контексте;
- указывать цены, расписание, правила или услуги, которых нет в контексте;
- упоминать контекст, базу данных, FAQ, поиск или нейросеть.

Стиль ответа:

- дружелюбный;
- краткий;
- профессиональный;
- как у настоящего сотрудника отеля.

Контекст:
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
