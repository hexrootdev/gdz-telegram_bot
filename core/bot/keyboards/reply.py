from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder, KeyboardButton

async def kb_classes() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for i in range(1, 12):
        kb.add(KeyboardButton(text=str(i)))
        kb.adjust(3)
    return kb.as_markup()