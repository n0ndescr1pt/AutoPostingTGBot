import asyncio

from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data.config import TOKEN
from handlers.admin_handlers import register_admin_handlers
from handlers.payment_handlers import register_payment_handlers
from handlers.user_handlers import register_user_handlers
from utils import apsched


def register_handler(dp: Dispatcher) -> None:
    register_user_handlers(dp)
    register_payment_handlers(dp)
    register_admin_handlers(dp)



async def main():

    token = TOKEN
    bot = Bot(token,parse_mode=ParseMode.MARKDOWN_V2)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(apsched.send_message_interval, trigger='interval', minutes=1, kwargs={'bot': bot})
    scheduler.start()

    register_handler(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    print(__name__)