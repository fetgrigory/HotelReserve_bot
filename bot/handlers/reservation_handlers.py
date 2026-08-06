from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from apps.bookings.crud import delete_reservation_draft, get_user_reservation_draft
from bot.common import texts
from bot.common.callbacks import BookingCB
from bot.keyboards.user_keyboard import (
    draft_keyboard,
    catalog_categories_keyboard,
    start_keyboard
)
from bot.services.booking_service import calculate_price
from bot.services.reservation_draft import process_add_room_to_draft

router = Router()


# Add to draft action
@router.callback_query(F.data == BookingCB.ADD_TO_DRAFT)
async def add_to_draft_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await process_add_room_to_draft(callback_query, state)


# Reservation draft
@router.message(F.text == "🛒 Моя корзина")
async def show_booking_draft(message: types.Message):
    draft = await get_user_reservation_draft(message.from_user.id)

    if not draft or not draft.room:
        await message.answer(
            texts.BOOKING_EMPTY,
            reply_markup=start_keyboard()
        )
        return

    days = (draft.end_date - draft.start_date).days
    total_price = calculate_price(draft.room.price, days)

    text = texts.BOOKING_DRAFT_INFO.format(
        room=draft.room.room_number,
        start_date=draft.start_date.strftime("%d.%m.%Y"),
        end_date=draft.end_date.strftime("%d.%m.%Y"),
        days=days,
        price=total_price
    )

    keyboard = draft_keyboard()

    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == BookingCB.CLEAR_DRAFT)
async def clear_draft(callback: types.CallbackQuery):
    await delete_reservation_draft(callback.from_user.id)

    await callback.message.edit_text(texts.BOOKING_CLEARED)
    await callback.answer()


@router.callback_query(F.data == BookingCB.BACK_TO_CATALOG)
async def back_to_catalog(callback: types.CallbackQuery):
    await callback.message.edit_text(
        texts.BACK_TO_CATALOG,
        reply_markup=catalog_categories_keyboard()
    )
    await callback.answer()
