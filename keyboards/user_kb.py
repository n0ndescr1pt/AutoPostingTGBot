from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callbackFactory import NumbersCallbackFactory


def get_user_kb():
    kb = [
        [
            types.KeyboardButton(text="Профиль"),
            types.KeyboardButton(text="Автопостинг"),
            types.KeyboardButton(text="Правила")
        ],
    ]
    startKeyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    return startKeyboard


def get_addBalance_kb():
    addBalanceKeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Пополнить баланс",
                    callback_data="addBalance"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="backProfile"
                )
            ]
        ]
    )
    return addBalanceKeyboard


def get_back_kb():
    kb3 = [
        [
            types.KeyboardButton(text="Отмена"),
        ],
    ]
    backKeyboard = types.ReplyKeyboardMarkup(
        keyboard=kb3,
        resize_keyboard=True,
    )
    return backKeyboard


def get_photo_kb():
    kb3 = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет"),
            types.KeyboardButton(text="Отмена"),
        ],
    ]
    backKeyboardPhoto = types.ReplyKeyboardMarkup(
        keyboard=kb3,
        resize_keyboard=True,
    )
    return backKeyboardPhoto



def get_userChoose_kb():
    kb4 = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Отмена"),
        ],
    ]
    userKeyboardChoose = types.ReplyKeyboardMarkup(
        keyboard=kb4,
        resize_keyboard=True,
    )
    return userKeyboardChoose


def get_profile_kb():
    profileKeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Баланс',
                    callback_data="balance"
                )
            ],
            [
                InlineKeyboardButton(
                    text='Мои сообщения',
                    callback_data="myMessage"
                )
            ]
        ]
    )
    return profileKeyboard


def get_addBalance_kb():
    addBalanceKeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Пополнить баланс",
                    callback_data="addBalance"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="backProfile"
                )
            ]
        ]
    )
    return addBalanceKeyboard

def get_backBalance_kb():
    kb8 = [
        [InlineKeyboardButton(text="Назад", callback_data="backAddBalance"), ]
    ]
    backBalanceKeyboard = InlineKeyboardMarkup(inline_keyboard=kb8)
    return backBalanceKeyboard


def crypto_bot_currencies_kb():
    currencies = ['USDT', 'USDC', 'BTC', 'ETH', 'TON', 'BNB']
    markup = InlineKeyboardBuilder()
    for currency in currencies:
        markup.button(text=currency,callback_data= f"crypto_bot_currency|{currency}")
        markup.adjust(3)

    markup.row(
        types.InlineKeyboardButton( text="❌ Отменить действие", callback_data="cancel")
    )
    return markup.as_markup()


def check_crypto_bot_kb(url: str, invoice_hash: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Оплатить", url=url
    )
    builder.button(
        text="Проверить оплату", callback_data=NumbersCallbackFactory(id=invoice_hash)
    )

    builder.adjust(1)
    return builder.as_markup()