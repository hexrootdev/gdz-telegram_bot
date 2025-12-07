from aiogram.fsm.state import State, StatesGroup

class Classes(StatesGroup):
    enter_class = State()

class Gdz(StatesGroup):
    enter_subject = State()
    enter_author = State()
    enter_paragraph = State()