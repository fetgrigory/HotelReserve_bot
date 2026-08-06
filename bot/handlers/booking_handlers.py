from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from apps.bookings.crud import is_room_available
from apps.users.crud import check_user_exists, insert_user_data
from bot.common import texts
from bot.common.callbacks import BookingCB
from bot.keyboards.user_keyboard import booking_keyboard
from bot.services.booking_service import calculate_rent_days, calculate_price, get_dates
from bot.states import BookingState

router = Router()


# Start booking process
@router.callback_query(F.data == BookingCB.ADD)
async def add_button(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    rooms = data.get('rooms')

    if rooms:
        room = rooms[0]
        await state.update_data(current_room=room)

        user_id = callback_query.from_user.id
        rent_days = data.get('rent_days', 1)
        start_date, end_date = get_dates(rent_days)

        if await is_room_available(room.id, start_date, end_date):
            if await check_user_exists(user_id):
                keyboard = booking_keyboard()
                await callback_query.message.edit_reply_markup(reply_markup=keyboard)
            else:
                # If the user is not registered, request data
                await state.set_state(BookingState.FIRST_NAME)

                await callback_query.message.answer(texts.REGISTRATION_INFO)
                await callback_query.message.answer(texts.STEP_1)
                await callback_query.message.answer(texts.BOOKING_FIRST_NAME)

        else:
            await callback_query.answer(texts.ERROR_ROOM_ALREADY_BOOKED)

    else:
        await callback_query.answer(texts.ERROR_ROOM_NOT_FOUND)


# Get username
@router.message(BookingState.FIRST_NAME)
async def process_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)

    await state.set_state(BookingState.LAST_NAME)
    await message.answer(texts.STEP_2)
    await message.answer(texts.BOOKING_LAST_NAME)


# Get user last name
@router.message(BookingState.LAST_NAME)
async def process_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)

    await state.set_state(BookingState.PHONE)
    await message.answer(texts.STEP_3)
    await message.answer(texts.BOOKING_PHONE)


# Get user phone number
@router.message(BookingState.PHONE)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)

    user_data = await state.get_data()
    user_id = message.from_user.id

    await insert_user_data(
        user_id,
        user_data['first_name'],
        user_data['last_name'],
        user_data['phone']
    )

    await state.clear()
    await message.answer(texts.REGISTRATION_DONE)

    room = user_data['current_room']
    rent_days = user_data.get('rent_days', 1)
    total_price = calculate_price(room.price, rent_days)

    text = texts.BOOKING_SUMMARY.format(days=rent_days, price=total_price)
    keyboard = booking_keyboard()

    await message.answer(text, reply_markup=keyboard)


# Increase the rental period and calculate the total price
@router.callback_query(F.data == BookingCB.ADD_DAYS)
async def add_days(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    room = data.get('current_room')

    if not room:
        await callback_query.answer(texts.ERROR_ROOM_NOT_FOUND)
        return

    rent_days = calculate_rent_days(data.get('rent_days', 1), 1)
    await state.update_data(rent_days=rent_days)

    new_price = calculate_price(room.price, rent_days)

    text = texts.BOOKING_SUMMARY.format(days=rent_days, price=new_price)
    keyboard = booking_keyboard()

    await callback_query.message.edit_text(text=text, reply_markup=keyboard)


# Decrease rental period
@router.callback_query(F.data == BookingCB.SUBTRACT_DAYS)
async def subtract_days(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    room = data.get('current_room')

    if not room:
        await callback_query.answer(texts.ERROR_ROOM_NOT_FOUND)
        return

    rent_days = calculate_rent_days(data.get('rent_days', 1), -1)
    await state.update_data(rent_days=rent_days)

    new_price = calculate_price(room.price, rent_days)

    text = texts.BOOKING_SUMMARY.format(days=rent_days, price=new_price)
    keyboard = booking_keyboard()

    await callback_query.message.edit_text(text=text, reply_markup=keyboard)