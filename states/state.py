from aiogram.fsm.state import StatesGroup, State


class PostState(StatesGroup):
    text = State()
    addImg = State()
    image = State()
    setCount = State()
    refactor = State()

class CryproBot(StatesGroup):
    sum = State()
    currency = State()

class ConfigState(StatesGroup):
    mailing = State()
    setPrice = State()