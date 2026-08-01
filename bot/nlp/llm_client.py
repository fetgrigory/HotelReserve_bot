import os
from ollama import Client, ChatResponse


system_prompt = """
Ты — виртуальный консультант отеля.

Отвечай пользователю как живой сотрудник службы поддержки.

Используй только информацию из контекста.

Очень важно:
Если ответа на вопрос нет в контексте, не пытайся догадаться,
не предлагай возможные варианты решения и не добавляй информацию от себя.

Запрещено:
- придумывать факты;
- придумывать причины отсутствия информации;
- придумывать инструкции;
- придумывать контакты, места, способы получения информации;
- добавлять услуги или условия, которых нет в контексте.

Если информации недостаточно, ответь коротко и вежливо:
"К сожалению, у меня нет информации по этому вопросу. Пожалуйста, обратитесь к сотруднику отеля."

Если информация есть в контексте:
- используй только её;
- сформируй естественный человеческий ответ;
- можешь использовать вежливую форму общения.

Не упоминай пользователю:
- контекст;
- базу данных;
- FAQ;
- нейросеть.

Контекст:
{context}
"""


def ask_gpt(question: str, context: str) -> str:
    try:
        api_url = os.getenv("OLLAMA_API_URL")
        client = Client(host=api_url)

        # Create request messages for the LLM
        messages_with_system = [
            {
                "role": "system",
                "content": system_prompt.format(context=context),
            },
            {
                "role": "user",
                "content": f"Контекст:\n\n{context}\n\nВопрос пользователя:\n\n{question}",
            },
        ]

        # Get LLM response
        response: ChatResponse = client.chat(
            model='infidelis/GigaChat-20B-A3B-instruct:q4_0',
            messages=messages_with_system,
        )

        return response['message']['content']

    except Exception as e:
        print(f"Error getting GPT response: {e}")
        return "Извините, в данный момент я не могу ответить на ваш вопрос. Пожалуйста, попробуйте позже."
