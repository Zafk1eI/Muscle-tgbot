from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                              input_field_placeholder="Выберете из меню ниже",
                              keyboard=[
                                  [
                                      KeyboardButton(text="Начать"),
                                      KeyboardButton(text="QUIZ")
                                  ]
                              ])


def generate_answer_keyboard():
    answer = []
    builder = InlineKeyboardBuilder()
    for item in answer:
        builder.add(InlineKeyboardButton(text=item, callback_data='Правильно'))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

