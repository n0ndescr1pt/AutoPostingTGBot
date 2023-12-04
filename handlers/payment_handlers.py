from aiocryptopay import AioCryptoPay
from aiogram import Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.utils.markdown import hlink

from data.config import CRYPTO_PAY_TOKEN, Admin, NETWORK
from keyboards.user_kb import get_addBalance_kb, get_backBalance_kb, crypto_bot_currencies_kb, check_crypto_bot_kb
from states.state import CryproBot
from utils.callbackFactory import NumbersCallbackFactory
from utils.database import getBalance, add_new_payment, select_payment, delete_payment, update_balance
from utils.someMethods import get_crypto_bot_sum, check_crypto_bot_invoice


async def balance(callback: types.CallbackQuery):
    await callback.message.delete()
    records = await getBalance(callback.from_user.id)
    photo = FSInputFile("assets/pay.png")
    await callback.message.answer_photo(caption=f"Баланс {records} $" ,photo=photo,reply_markup=get_addBalance_kb(),parse_mode=ParseMode.HTML)



async def addBalance(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text=f"Введите сумму пополнения в долларах",reply_markup=get_backBalance_kb())

    await state.set_state(CryproBot.sum)



async def enterCur(message: types.Message,state: FSMContext):
    try:
        if float(message.text) >= 0.1:
            await message.answer(
                f'<b>{hlink("⚜️ CryptoBot", "https://t.me/CryptoBot")}</b>\n\n'
                f'— Сумма: <b>{message.text} $</b>\n\n'
                '<b>💸 Выберите валюту, которой хотите оплатить счёт</b>',
                disable_web_page_preview=True,
                reply_markup=crypto_bot_currencies_kb(),
                parse_mode=ParseMode.HTML
            )

            await state.update_data(sum=float(message.text))
            await state.set_state(CryproBot.currency)
        else:
            await message.answer(
                text='⚠️ Минимум: 0.1 $!',parse_mode=ParseMode.HTML
            )
    except ValueError:
        await message.answer(
            '<b>❗️Сумма для пополнения должна быть в числовом формате!</b>',parse_mode=ParseMode.HTML
        )


async def crypto_bot_currency(call: types.CallbackQuery, state: FSMContext):

    try:
        await call.message.delete()
        data = await state.get_data()
        cryptopay = AioCryptoPay(CRYPTO_PAY_TOKEN, network=NETWORK)
        invoice = await cryptopay.create_invoice(
            asset=call.data.split('|')[1],
            amount=await get_crypto_bot_sum(
                data['sum'],
                call.data.split('|')[1],
                cryptopay
            )
        )
        await cryptopay.close()

        await state.update_data(currency=call.data.split('|')[1])

        await add_new_payment(invoice.invoice_id, data['sum'])

        await call.message.answer(
            f"<b>💸 Отправьте {data['sum']} $ {hlink('по ссылке', invoice.bot_invoice_url)}</b>",
            reply_markup=check_crypto_bot_kb(invoice.bot_invoice_url, invoice.invoice_id), parse_mode=ParseMode.HTML
        )
        await state.clear()

    except Exception:

        await call.message.answer(
            '<b>⚠️ Произошла ошибка!</b>',reply_markup=get_addBalance_kb(), parse_mode=ParseMode.HTML
        )

async def check_crypto_bot(call: types.CallbackQuery,callback_data: NumbersCallbackFactory):
    info = await select_payment(callback_data.id)
    if info is not None:
        if await check_crypto_bot_invoice(callback_data.id):
            cryptopay = AioCryptoPay(CRYPTO_PAY_TOKEN, network=NETWORK)
            invoice = await cryptopay.get_invoices(invoice_ids=callback_data.id)

            await cryptopay.close()
            print(invoice)
            print(invoice.amount)

            print(int(info[1]))
            print(int(info[0]))
            print(callback_data)
            print(call.from_user.id)

            await update_balance(call.from_user.id, info[1])
            await delete_payment(invoice.invoice_id)
            print(1)
            await call.answer(
                '✅ Оплата прошла успешно!',
                show_alert=True
            )
            await call.message.delete()
            await call.message.answer(
                f'<b>💸 Ваш баланс пополнен на сумму {info[1]} $!</b>',parse_mode=ParseMode.HTML
            )


            await call.bot.send_message(
                Admin,
                f'<b>{hlink("⚜️ CryptoBot", "https://t.me/CryptoBot")}</b>\n'
                f'<b>💸 Обнаружено пополнение от @{call.from_user.username} [<code>{call.from_user.id}</code>] '
                f'на сумму {info[1]} $!</b>', parse_mode=ParseMode.HTML
            )

        else:
            await call.answer(
                '❗️ Вы не оплатили счёт!',
                show_alert=True
            )

async def backBalance(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=f"Ваш профиль",reply_markup=get_addBalance_kb())

def register_payment_handlers(dp: Dispatcher):
    dp.callback_query.register(balance, F.data == "balance")
    dp.callback_query.register(addBalance, F.data == "addBalance")
    dp.message.register(enterCur,CryproBot.sum)
    dp.callback_query.register(crypto_bot_currency, CryproBot.currency)
    dp.callback_query.register(check_crypto_bot, NumbersCallbackFactory.filter())
    dp.callback_query.register(backBalance, F.data == "backAddBalance")