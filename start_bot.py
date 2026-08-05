import os
import asyncio
import logging

import django
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from aiogram import Bot, Router, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from bot.common.texts import WELCOME
from bot.keyboards.user_keyboard import start_keyboard

from bot.handlers.catalog_handlers import router as catalog_router
from bot.handlers.booking_handlers import router as booking_router
from bot.handlers.reservation_handlers import router as reservation_router
from bot.handlers.payment_handlers import router as payment_router
from bot.handlers.review_handlers import router as review_router
from bot.handlers.ai_handlers import router as ai_router

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger(__name__)


# Load environment variables
load_dotenv()

router = Router()


TOKEN = os.getenv("TOKEN")

if not TOKEN:
    logger.critical("TOKEN не задан в переменных окружения!")
    raise RuntimeError("TOKEN не задан!")


# Initialize bot and dispatcher
storage = MemoryStorage()

bot = Bot(token=TOKEN)

dp = Dispatcher(storage=storage)


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    logger.info("User pressed /start")

    await state.clear()

    keyboard = start_keyboard()

    me = await message.bot.get_me()

    await message.answer(
        WELCOME.format(
            user_name=message.from_user.first_name,
            bot_name=me.first_name
        ),
        parse_mode="html",
        reply_markup=keyboard
    )
# Connect routers
dp.include_routers(
    router,
    catalog_router,
    booking_router,
    reservation_router,
    payment_router,
    review_router,
    ai_router,
)


async def main():
    logger.info("Start polling")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
