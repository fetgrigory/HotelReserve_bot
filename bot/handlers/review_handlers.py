from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from apps.reviews.crud import insert_review
from apps.reviews.schemas import ReviewCreate
from bot.common import texts
from bot.states import ReviewState

router = Router()


# User review input
@router.callback_query(F.data.startswith("add_review"))
async def request_review(callback_query: types.CallbackQuery, state: FSMContext):
    room_id = int(callback_query.data.split(":")[1])

    await state.update_data(review_room_id=room_id)
    await state.set_state(ReviewState.TEXT)

    await callback_query.message.answer(texts.REVIEW_INPUT_MESSAGE)
    await callback_query.answer()


@router.message(ReviewState.TEXT)
async def save_review(message: types.Message, state: FSMContext):
    data = await state.get_data()
    room = data['review_room_id']

    user_id = message.from_user.id

    try:
        review_data = ReviewCreate(text=message.text)
    except ValidationError:
        await message.answer(texts.REVIEW_LENGTH_ERROR)
        return

    review = await insert_review(
        user_id,
        room,
        review_data.text,
    )

    if review is None:
        await message.answer(texts.REVIEW_REGISTRATION_REQUIRED)
        return

    await message.answer(texts.REVIEW_SUBMITTED)
    await state.clear()
