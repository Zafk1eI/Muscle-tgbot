from aiogram.fsm.state import StatesGroup, State


class Storage(StatesGroup):
    RECORD_DATA = State()


class Form(StatesGroup):
    input = State()
