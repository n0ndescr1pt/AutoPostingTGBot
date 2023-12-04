


from typing import Optional
from aiogram.filters.callback_data import CallbackData

class NumbersCallbackFactory(CallbackData, prefix="check_crypto_bot"):
    id: int

class IdsCallbackFactory(CallbackData, prefix="users_id"):
    user_id: int