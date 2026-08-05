from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType

from apps.bookings.crud import insert_booking_data
from bot.common import texts
from bot.common.callbacks import BookingCB
from bot.payment import send_invoice
from bot.services.booking_service import calculate_price, get_dates

router = Router()


# Payment processing
@router.callback_query(F.data == BookingCB.PAY)
async def pay_for_apartment(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await send_invoice(callback_query.bot, callback_query, data)


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await pre_checkout_q.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, state: FSMContext):
    await handler_successful_payment(message.bot, message, state)


async def handler_successful_payment(bot, message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    room = data['current_room']
    rent_days = data.get('rent_days', 1)
    start_date, _ = get_dates(rent_days)
    total_price = calculate_price(room.price, rent_days)

    await insert_booking_data(
        user_id,
        room.id,
        start_date,
        rent_days,
        total_price
    )

    await bot.send_message(user_id, texts.PAYMENT_SUCCESS)
