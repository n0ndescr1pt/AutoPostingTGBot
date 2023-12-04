from aiocryptopay import AioCryptoPay
from aiogram import types, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from data.config import Admin, CRYPTO_PAY_TOKEN, NETWORK
from keyboards.admin_kb import get_admin_kb, get_admin_choose_kb
from keyboards.user_kb import get_addBalance_kb, get_back_kb, get_user_kb, get_photo_kb, get_userChoose_kb, \
    get_profile_kb
from states.state import PostState
from utils.database import addNewUser, getBalance, getPrice, payForPost, orderPosts, addData, checkMyPost, \
    select_payment, update_balance, delete_payment
from utils.someMethods import cancel


#start command
async def start(message: types.Message):
    await addNewUser(message.from_user.id)
   # try:
    if(message.from_user.id == Admin):
        photo = FSInputFile("assets/moderation.png")
        await message.reply_photo(photo=photo,caption=f"Приветствую", reply_markup=get_admin_kb(),parse_mode=ParseMode.HTML)


    else:
        await message.reply(f"Приветствую", reply_markup=get_user_kb())
    #except Exception:
    #    print("Что то сломалось либо пользователь заблокировал бота")


#handle create post
async def setContent(message: types.Message, state:FSMContext):
        photo = FSInputFile("assets/autoposting.png")
        await message.answer_photo(photo=photo,caption=f"Отправьте текст поста",reply_markup=get_back_kb())
        await state.set_state(PostState.text)


#add text to post
async def setText(message: types.Message, state:FSMContext):
    if(message.text == "Отмена"):
        await cancel(message, state)

    else:
        await state.update_data(text=message.md_text)
        await message.answer(text=f"Добавить картинку?",reply_markup=get_photo_kb())
        await state.set_state(PostState.addImg)

#add img to post?
async def addImg(message: types.Message, state:FSMContext):
    if (message.text == "Отмена"):
        await cancel(message, state)

    elif (message.text == "Да"):
        await message.answer(text=f"Отправьте картинку")
        await state.set_state(PostState.image)
    else:
        await state.update_data(photo="")

        #user_data = await state.get_data()
        #postText = user_data['text']

        await message.answer(text="Введите количество публикаций поста",reply_markup=get_back_kb())
        #await message.answer(text=postText, reply_markup=get_back_kb())
        await state.set_state(PostState.setCount)


#add img to post

async def setImg(message: types.Message, state:FSMContext):
    if (message.text == "Отмена"):
        await cancel(message, state)

    else:
        await state.update_data(photo=message.photo[-1].file_id)

        #user_data = await state.get_data()
        #postText = user_data['text']
        #postImg = user_data['photo']

        await message.answer(text="Введите количество публикаций поста",reply_markup=get_back_kb())
        #await message.answer_photo(photo=postImg, caption=postText,reply_markup=get_back_kb())

        await state.set_state(PostState.setCount)


async def setCounts(message: types.Message, state:FSMContext):
    if (message.text == "Отмена"):
        await cancel(message, state)

    else:
        try:
            float(message.text)
            await state.update_data(count=message.text)

            user_data = await state.get_data()
            postText = user_data['text']
            postImg = user_data['photo']
            count = user_data['count']
            if(int(count)>=2 and int(count)<=4):
                await message.answer(text=f"Ваш пост выглядит так и будет опубликован {message.text} раза, продолжить?")
            else:
                await message.answer(text=f"Ваш пост выглядит так и будет опубликован {message.text} раз, продолжить?")
            if (postImg == ""):
                await message.answer(text=postText, disable_web_page_preview=True, reply_markup=get_userChoose_kb())
            else:
                await message.answer_photo(photo=postImg, caption=postText,reply_markup=get_userChoose_kb())
            price = await getPrice()
            await message.answer(text=f"С вашего баланса будет списано {price * float(count)} $", disable_web_page_preview=True, parse_mode=ParseMode.HTML)
            await state.set_state(PostState.refactor)
        except ValueError:
            await message.answer(
                '<b>Введите число</b>', parse_mode=ParseMode.HTML
            )


#send post to admins

async def refactoring(message: types.Message, state:FSMContext):
    user_data = await state.get_data()
    postText = user_data['text']
    postImg = user_data['photo']
    count = user_data['count']

    balance = await getBalance(message.from_user.id)
    price = await getPrice()
    if (message.text == "Отмена"):
        await cancel(message, state)
    elif(balance < price * float(count)):
        await message.answer(
            text=f"На балансе недостаточно средств, пополните баланс.\nЦена за один пост = {price} $\nваш баланс = {balance} $",
            reply_markup=get_addBalance_kb(), parse_mode=ParseMode.HTML)
        await cancel(message, state)
    else:
        await payForPost(message.from_user.id)
        order = await orderPosts()

        await message.answer(text=f"Постов в очереди {order}, на балансе осталось {balance} $",parse_mode=ParseMode.HTML)

        if (postImg == ""):
            msg = await message.bot.send_message(chat_id=Admin, text=postText, reply_markup=get_admin_choose_kb(message.from_user.id), disable_web_page_preview=True)
        else:
            msg = await message.bot.send_photo(chat_id=Admin, photo=postImg, caption=postText, reply_markup=get_admin_choose_kb(message.from_user.id))
        addData(msg.message_id,postText,postImg,message.from_user.id,count)

        await message.answer(text=f"Успешно отправлено на модерацию", reply_markup=get_user_kb())

        await state.clear()

async def profile(message: types.Message):
    photo = FSInputFile("assets/profile.png")
    await message.answer_photo(photo=photo,reply_markup=get_profile_kb())


async def myMessage(callback: types.CallbackQuery):
    posts = await checkMyPost(callback.from_user.id)
    await callback.message.answer("Ваши посты в очереди на проверку")
    for row in posts:
        if (row[1] == ""):
                await callback.message.answer(text=row[0], disable_web_page_preview=True)
        else:
                await callback.message.answer_photo(photo=row[1], caption=row[0],)



async def backProfile(callback: types.CallbackQuery):
    await callback.message.delete()
    photo = FSInputFile("assets/profile.png")
    await callback.message.answer_photo(photo=photo ,reply_markup=get_profile_kb())



async def rules(message: types.Message):
    photo = FSInputFile("assets/rules.jpg")

    await message.answer_photo(photo=photo, caption=f"🚫 Political discussions\n"
                                                    f"🚫 Unauthorized advertising\n"
                                                    f"🚫 Scamming a chat member - BAN\n"
                                                    f"——————————————————\n"
                                                    f"🚫 Политические дискуссии\n"
                                                    f"🚫 Несанкционированная реклама\n"
                                                    f"Скам участника чата  - БАН",
                                                    parse_mode=ParseMode.HTML)
def register_user_handlers(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(setContent, F.text.lower()=="автопостинг", StateFilter(None))
    dp.message.register(setText, PostState.text)
    dp.message.register(addImg, PostState.addImg)
    dp.message.register(setImg, PostState.image, F.photo)
    dp.message.register(setCounts, PostState.setCount)
    dp.message.register(refactoring, PostState.refactor)
    dp.message.register(profile, F.text.lower() == "профиль")
    dp.callback_query.register(myMessage, F.data == "myMessage")
    dp.callback_query.register(backProfile, F.data == "backProfile")
    dp.message.register(rules, F.text.lower() == "правила")