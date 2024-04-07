from db import methods
from random import shuffle
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder


main_kb = ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True,
                              input_field_placeholder="Выберете из меню ниже",
                              keyboard=[
                                  [
                                      KeyboardButton(text="Начать"),
                                      KeyboardButton(text="Топ")
                                  ],
                              ])


async def generate_list(correct_answer: str) -> list:
    answer = [correct_answer]
    while len(answer) != 4:
        record = await methods.get_random_record()
        if record.name not in answer:
            answer.append(record.name)
    print(answer)
    shuffle(answer)
    return answer


def generate_answer_keyboard(answer: list, correct_answer: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in answer:
        if item == correct_answer:
            builder.add(InlineKeyboardButton(text=item, callback_data='Правильно'))
        else:
            builder.add(InlineKeyboardButton(text=item, callback_data='Неправильно'))
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def generate_every_day(answer: list, correct_answer: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in answer:
        if item == correct_answer:
            builder.add(InlineKeyboardButton(text=item, callback_data='Молодец'))
        else:
            builder.add(InlineKeyboardButton(text=item, callback_data='Плохо'))
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup(resize_keyboard=True)