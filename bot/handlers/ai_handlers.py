from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.common import texts
from bot.services.ai_service import process_question
from bot.states import QuestionState

router = Router()


# AI support chat
@router.message(F.text == "🎧 Задать вопрос")
async def ask_question_handler(message: types.Message, state: FSMContext):
    await state.set_state(QuestionState.WAITING_QUESTION)
    await state.update_data(messages=[])

    await message.answer(texts.AI_QUESTION_MESSAGE)


@router.message(QuestionState.WAITING_QUESTION)
async def handler_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    messages = data.get('messages', [])

    user_id = message.from_user.id
    thinking_msg = await message.answer(texts.AI_THINKING)

    try:
        response, updated_messages = await process_question(message.text, messages)

        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=thinking_msg.message_id
        )

        await state.update_data(messages=updated_messages)
        await message.answer(response)

    except Exception as e:
        print(f"Error (User {user_id}): {e}")
        await message.answer(texts.AI_ERROR)
