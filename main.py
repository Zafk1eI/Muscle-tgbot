from os import getenv
from aiogram.enums import ParseMode
import asyncio
import database as db
from dotenv import load_dotenv

import keyboard
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

load_dotenv()
bot = Bot(getenv("TOKEN"))
dp = Dispatcher(bot=bot, parse_mode=ParseMode.HTML)


async def on_startup() -> None:
    await db.db_start()
    print("Бот и база данных запущены")


@dp.message(F.text.lower() == 'начать')  # первая кнопка
async def start_game(message: Message) -> None:
    record = await db.get_random_record()
    print(record)
    muscle = FSInputFile(record)
    await message.answer_photo(muscle, reply_markup=keyboard.il_kb)


@dp.message(Command('help'))
async def command_help(message: Message) -> None:
    await message.answer('HELP')


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'''Привет! Добро пожаловать в тест на знание названий мышц!
Готов проверить свои знания? Просто отвечай на вопросы о названиях различных мышц. 
Попробуй дать правильные ответы!Если тебе нужна помощь или справка о доступных командах, просто напиши /help. 
Удачи в тестировании своих знаний!''', reply_markup=keyboard.main_kb)


async def main():
    await on_startup()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
