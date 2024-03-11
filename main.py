from os import getenv
from aiogram.enums import ParseMode
import asyncio
import database as db
from dotenv import load_dotenv

import keyboard
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command

load_dotenv()
bot = Bot(getenv("TOKEN"))
dp = Dispatcher(bot=bot, parse_mode=ParseMode.HTML)
record_ = None


async def on_startup() -> None:
    await db.db_start()
    print("Бот и база данных запущены")


@dp.message(F.text.lower() == 'начать')  # первая кнопка
async def start_game(message: Message) -> None:
    global record
    record = await db.get_random_record()
    if not await db.user_has_seen_all_records(message.from_user.id):
        while await db.is_record_in_db(message.from_user.id, record[0]):
            record = await db.get_random_record()
        print(record[2])
        kb = await keyboard.generate_list(record[1])
        muscle = FSInputFile(record[2])
        await message.answer_photo(muscle, reply_markup=keyboard.generate_answer_keyboard(kb, record[1]))
    else:
        await message.answer("Вы ответили на все предложенные вопросы. Теперь они будут повторятся."
                             "Нажмите еще раз начать.")
        db.delete_record(message.from_user.id)


@dp.callback_query(F.data == "Правильно")
async def send_random_value_yes(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer(text='Молодец, правильно!')
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=None)
    if not await db.is_record_in_db(callback.from_user.id, record[0]):
        await db.insert_record(callback.from_user.id, record[0])


@dp.callback_query(F.data == "Неправильно")
async def send_random_value_no(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer(text=f'Неправильно, это {record[1]}')
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id,
                                        message_id=callback.message.message_id,
                                        reply_markup=None)


@dp.message(Command('help'))
async def command_help(message: Message) -> None:
    await message.answer('Для начала нажмите кнопку "НАЧАТЬ"')


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'''Привет! Добро пожаловать в тест на знание названий мышц!
Готов проверить свои знания? Просто отвечай на вопросы о названиях различных мышц. 
Попробуй дать правильные ответы!Если тебе нужна помощь или справка о доступных командах, просто напиши /help. 
Удачи в тестировании своих знаний!''', reply_markup=keyboard.main_kb)


async def main() -> None:
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
