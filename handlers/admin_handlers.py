from aiogram import Dispatcher, F, types, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from data.config import Admin
from keyboards.admin_kb import get_backEnterPrice_kb, get_admin_kb
from states.state import ConfigState
from utils.callbackFactory import IdsCallbackFactory
from utils.database import delData, addToReady, giveAllUsers, setPricePerPost, getCountMessage
from utils.someMethods import infoUserNo, infoUserYes, cancel


# get response from admins

async def deletePost(callback: types.CallbackQuery):
    await infoUserNo(callback, callback.bot)

    await delData(callback.message.message_id)

    await callback.answer(text="Удалено из очереди")

    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)


# get response from admins

async def addPost(callback: types.CallbackQuery,callback_data: IdsCallbackFactory):
    await infoUserYes(callback, callback.bot)
    count = await getCountMessage(callback.message.message_id)
    print(callback_data.user_id)
    await addToReady(callback.message.message_id,count,int(callback_data.user_id))

    await callback.answer(text=f"Успешно добавленно в очередь")

    await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)




async def mailing(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите сообщение", reply_markup=get_backEnterPrice_kb())
    await state.set_state(ConfigState.mailing)


async def addMessage(message: types.Message, state: FSMContext):
    users = await giveAllUsers()
    succes = 0
    unluck = 0
    print(users)
    for user in users:
        if (user[0] != Admin):
            try:
                print(user[0])
                await message.bot.send_message(chat_id=user[0], text=message.text)
                succes = succes + 1
            except Exception as e:
                print(f"пользователь {user[0]} удалил бота")
                print(e)
                unluck = unluck + 1
    await message.answer(text=f"Рассылка отправлена успешно дошло {succes}, не дошло {unluck}",
                         reply_markup=get_admin_kb())
    await state.clear()

async def setPrice(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите цену за пост", reply_markup=get_backEnterPrice_kb())
    await state.set_state(ConfigState.setPrice)


async def enterPrice(message: types.Message, state: FSMContext):
    try:
        await setPricePerPost(float(message.text))
        await message.answer(f"Успешно изменена на {message.text} $",reply_markup=get_admin_kb(), parse_mode=ParseMode.HTML)
        await state.clear()

    except ValueError:
        await message.answer(
            '<b>❗️Цена должна быть в числовом формате!</b>', parse_mode=ParseMode.HTML
        )


async def backCancle(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text=f"Действие отменено", reply_markup=get_admin_kb())


def register_admin_handlers(dp: Dispatcher):
    dp.callback_query.register(deletePost, F.data == "no")
    dp.callback_query.register(addPost, IdsCallbackFactory.filter())
    dp.callback_query.register(mailing, F.data == "mailing")
    dp.message.register(addMessage, ConfigState.mailing)
    dp.callback_query.register(setPrice, F.data == "setPrice")
    dp.callback_query.register(backCancle, F.data == "back")
    dp.message.register(enterPrice, ConfigState.setPrice)
