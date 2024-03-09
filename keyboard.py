from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_random_record
import random
main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                              input_field_placeholder="Выберете из меню ниже",
                              keyboard=[
                                  [
                                      KeyboardButton(text="Начать"),
                                      KeyboardButton(text="QUIZ")
                                  ]
                              ])


async def generate_list(correct_answer):
    answer = [correct_answer]
    while len(answer) != 4:
        record = await get_random_record()
        if record[1] not in answer:
            answer.append(record[1])
    print(answer)
    random.shuffle(answer)
    return answer


def generate_answer_keyboard(answer: list, correct_answer):
    builder = InlineKeyboardBuilder()
    for item in answer:
        if item == correct_answer:
            builder.add(InlineKeyboardButton(text=item, callback_data='Правильно'))
        else:
            builder.add(InlineKeyboardButton(text=item, callback_data='Неправильно'))
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)


