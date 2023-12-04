import sqlite3

from aiocryptopay import AioCryptoPay
from aiogram import types
from aiogram.fsm.context import FSMContext

from data.config import CRYPTO_PAY_TOKEN, NETWORK
from keyboards.user_kb import get_user_kb


async def infoUserYes(callback: types.CallbackQuery,bot):
    connection = sqlite3.connect('posts.db')
    cursor = connection.execute("SELECT user_id FROM uncheck WHERE message_id = ?", (callback.message.message_id,))

    for row in cursor:
        await bot.send_message(chat_id=row[0], text="Ваш пост прошел модерацию и будет опубликован в ближайшее время")


async def infoUserNo(callback: types.CallbackQuery,bot):
    connection = sqlite3.connect('posts.db')
    cursor = connection.execute("SELECT user_id FROM uncheck WHERE message_id = ?", (callback.message.message_id,))

    for row in cursor:
        await bot.send_message(chat_id=row[0], text="К сожалению ваш пост не прошел модерацию")


async def cancel(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer(text=f"Действие отменено", reply_markup=get_user_kb())


async def get_crypto_bot_sum(summa: float, currency: str, cryptopay: AioCryptoPay):
    courses = await cryptopay.get_exchange_rates()
    await cryptopay.close()
    for course in courses:
        if course.source == currency and course.target == 'USD':
            return summa / course.rate

async def check_crypto_bot_invoice(invoice_id: int):
    cryptopay = AioCryptoPay(CRYPTO_PAY_TOKEN,  network=NETWORK)
    invoice = await cryptopay.get_invoices(invoice_ids=invoice_id)
    await cryptopay.close()
    if invoice.status == 'paid':
        return True
    else:
        return False
