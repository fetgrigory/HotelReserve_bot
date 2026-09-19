from datetime import datetime, timedelta

from aiogram import types
from aiogram.fsm.context import FSMContext

from apps.bookings.crud import add_room_to_draft, is_room_available
from bot.common.texts import ERROR_ROOM_ALREADY_BOOKED, ERROR_ROOM_NOT_FOUND, ROOM_ADDED_TO_BOOKING


# Add room to draft
async def process_add_room_to_draft(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    room = data.get('current_room')
    rent_days = data.get('rent_days', 1)

    if not room:
        return await callback.answer(ERROR_ROOM_NOT_FOUND, show_alert=True)
    start_date = datetime.now()
    end_date = start_date + timedelta(days=rent_days)

    # Check if the room is available for the selected dates
    if not await is_room_available(
        room.id,
        start_date,
        end_date
    ):
        return await callback.answer(ERROR_ROOM_ALREADY_BOOKED, show_alert=True)

    await add_room_to_draft(
        user_telegram_id=callback.from_user.id,
        room_id=room.id,
        start_date=start_date,
        end_date=end_date
    )

    await callback.answer(
        ROOM_ADDED_TO_BOOKING.format(
            start_date=start_date.strftime('%d.%m.%Y'),
            end_date=end_date.strftime('%d.%m.%Y'),
            days=rent_days
        ),
        show_alert=False
    )
