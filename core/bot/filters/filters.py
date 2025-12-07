from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter

from core.bot.keyboards.inline import subjects

rang = [str(i) for i in list(range(1, 12))]
class IsTheClassInTheRange(BaseFilter):
    async def __call__(self, message: Message):
        return str(message.text) in rang

class IsTheSubject(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        return str(callback.data) in subjects.values()
