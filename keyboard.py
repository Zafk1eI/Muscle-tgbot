from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                              input_field_placeholder="Выберете из меню ниже",
                              keyboard=[
                                  [
                                      KeyboardButton(text="Начать"),
                                      KeyboardButton(text="QUIZ")
                                  ]
                              ])

il_kb = InlineKeyboardMarkup(resize_keyboard=True,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text='Россия', url='https://t.me'),
                                     InlineKeyboardButton(text='Европа', url='https://t.me')
                                 ],
                                 [
                                     InlineKeyboardButton(text='Белорусь', url='https://t.me'),
                                     InlineKeyboardButton(text='Польша', url='https://t.me')
                                 ]
                             ])

