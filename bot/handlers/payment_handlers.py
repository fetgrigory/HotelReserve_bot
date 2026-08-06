from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType

from apps.bookings.crud import process_draft_payment_success
from bot.common import texts
from bot.common.callbacks import BookingCB
from bot.payment import send_invoice


router = Router()


# Payment processing
@router.callback_query(F.data == BookingCB.PAY)
async def pay_for_apartment(callback_query: types.CallbackQuery):
    await send_invoice(callback_query.bot, callback_query)
    await callback_query.answer()


@router.pre_checkout_query()
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await pre_checkout_q.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, state: FSMContext):
    await handler_successful_payment(message.bot, message, state)


async def handler_successful_payment(bot, message, state):
    user_id = message.from_user.id

    booking = await process_draft_payment_success(user_id)

    if booking:
        await state.clear()
        await bot.send_message(user_id, texts.PAYMENT_SUCCESS)
    else:
        await bot.send_message(
            user_id,
            "✅ Оплата прошла успешно, но возникла ошибка при переносе записи из корзины.\n"
            "Пожалуйста, свяжитесь со службой поддержки."
        )