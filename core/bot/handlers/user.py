from aiogram.types import Message, CallbackQuery, URLInputFile
from aiogram.filters import Command, CommandStart
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from core.bot.keyboards.reply import kb_classes
from core.bot.keyboards.inline import create_subjects_kb, create_authors_kb
from core.bot.fsm.fsm import Classes, Gdz
from core.bot.filters.filters import IsTheClassInTheRange, IsTheSubject

from core.gdz.gdz_finder import get_tasks, get_images

from core.database.database import create_database, add_user, add_class, is_class, get_class


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'<b>👋Здравствуйте, <em>{message.from_user.full_name}</em>.\n\nℹ️Для полного ознакомления с '
                         f'функционалом бота введите /help</b>')
    await create_database()
    await add_user(tg_id=message.from_user.id)


@router.message(Command('help'))
async def help(message: Message):
    await message.answer('<b><em>📋Вот список всех команд:\n\n</em>'
                         '1. /class - <em>указать свой класс\n</em>'
                         '2. /gdz - <em>найти готовое домашнее задание по любому предмету</em></b>')

@router.message(Command('class'))
async def classes(message: Message, state: FSMContext):
    await message.answer('🏫<b>Выберите ваш класс:</b>', reply_markup=await kb_classes())
    await state.set_state(Classes.enter_class)

@router.message(IsTheClassInTheRange(), Classes.enter_class)
async def enter_class(message: Message, state: FSMContext):
    await add_class(tg_id=message.from_user.id, class_=message.text)
    await message.answer(f'<b>✅Успешно.\nВаш класс: {message.text}</b>')
    await state.clear()

@router.message(Command('gdz'))
async def gdz(message: Message, state: FSMContext):
    cls = await get_class(tg_id=message.from_user.id)
    if not await is_class(tg_id=message.from_user.id):
        await message.answer('<b>❌Вы еще не выбрали класс!\n\nПожалуйста, выберите <em>/class</em></b>')
    else:
        await message.answer('<b>Выберите необходимый предмет: </b>', reply_markup=await create_subjects_kb(cls=cls))
    await state.set_state(Gdz.enter_subject)

@router.callback_query(IsTheSubject(), Gdz.enter_subject)
async def authors(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    cls = await get_class(tg_id=callback.from_user.id)
    await callback.message.answer('<b>Выберите автора:</b> ', reply_markup=await create_authors_kb(cls=cls, subject=str(callback.data))) # ОШИБКА
    await callback.answer()
    await state.set_state(Gdz.enter_author)


@router.callback_query(Gdz.enter_author)
async def paragraph(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    await state.update_data(url=callback.data)
    await callback.message.answer('<b>Введите остальные данные исходя из Вашего предмета и учебника.\n\nНапример, для литературы:'
                         '<em>1-8 (часть 1 страница 8)\nили для физики: 1-3-4 (упражнение 1, 3 - в зависимости от выпуска учебника, номер 4)</em></b>')
    await callback.answer()
    await state.set_state(Gdz.enter_paragraph)

@router.message(Gdz.enter_paragraph)
async def image(message: Message, state: FSMContext):
    print(message.text)
    data = await state.get_data()
    tasks = get_tasks(link=data['url'])

    task = tasks[message.text]
    images = get_images(link=task)

    album_builder = MediaGroupBuilder(caption='Держи бро')
    for image in images:
        file = URLInputFile(url='https:' + image)
        album_builder.add(media=file, type='photo')

    await message.answer_media_group(media=album_builder.build())
    await state.clear()