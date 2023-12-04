from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callbackFactory import IdsCallbackFactory


def get_admin_kb():
    adminKeyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Установить цену",
                    callback_data="setPrice"
                )
            ],
            [
    InlineKeyboardButton(
                    text="Рассылка",
                    callback_data="mailing"
                )
            ]
        ]
    )
    return adminKeyboard

def get_admin_choose_kb(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Принять", callback_data=IdsCallbackFactory(user_id=user_id)
    )
    builder.button(
        text="Отклонить", callback_data="no"
    )
    builder.adjust(1)
    return builder.as_markup()
    #kb2 = [
    #    [
    #        types.InlineKeyboardButton(text="Принять", callback_data="yes"),
    #        types.InlineKeyboardButton(text="Отклонить", callback_data="no")
    #    ]
    #]
    #chooseKeyboard = types.InlineKeyboardMarkup(inline_keyboard=kb2)
    #return chooseKeyboard


def get_backEnterPrice_kb():
    kb8 = [
        [InlineKeyboardButton(text="Назад", callback_data="back"), ]
    ]
    backBalanceKeyboard = InlineKeyboardMarkup(inline_keyboard=kb8)
    return backBalanceKeyboard