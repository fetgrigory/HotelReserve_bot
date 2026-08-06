import os

from aiogram import Bot, types
from aiogram.types import LabeledPrice

from apps.bookings.crud import get_user_reservation_draft
from bot.services.booking_service import calculate_booking_total


async def send_invoice(bot: Bot, callback_query: types.CallbackQuery):
    chat_id = callback_query.from_user.id
    # Set the title and description for the invoice
    provider_token = os.getenv('PAYMENTS_TOKEN')

    # Get reservation draft data from database
    draft = await get_user_reservation_draft(chat_id)

    if not draft or not draft.room:
        await callback_query.answer("Ошибка: данные бронирования не найдены")
        return

    room = draft.room

    rent_days, total_price = calculate_booking_total(
        price_per_day=room.price,
        start_date=draft.start_date,
        end_date=draft.end_date
    )

    title = f"Бронь: {room.name if hasattr(room, 'name') else 'Номер в отеле'}"
    description = (
        f"Аренда на {rent_days} дн. "
        f"({draft.start_date.strftime('%d.%m')} - "
        f"{draft.end_date.strftime('%d.%m')})"
    )

    invoice_payload = f"draft_payment_{draft.id}"
    currency = "RUB"

    prices = [
        LabeledPrice(
            label=f"Проживание ({rent_days} дн.)",
            amount=int(total_price * 100)
        )
    ]

    await bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=invoice_payload,
        provider_token=provider_token,
        currency=currency,
        prices=prices
    )


async def handler_successful_payment(bot: Bot, message: types.Message):
    payment_info = message.successful_payment
    # Displaying the payment details in the console
    for k, v in payment_info.__dict__.items():
        print(f"{k} = {v}")
    # Send a confirmation message to the user
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"Платеж на сумму {payment_info.total_amount // 100} {payment_info.currency} прошел успешно!"
    )
