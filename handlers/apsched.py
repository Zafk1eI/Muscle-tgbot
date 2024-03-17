import keyboard
from aiogram import Bot
from aiogram.types import FSInputFile
import database as db


async def start_game(bot: Bot, user_id: int) -> None:
    record = await db.get_random_record()
    if not await db.user_has_seen_all_records(user_id):
        while await db.is_record_in_db(user_id, record[0]):
            record = await db.get_random_record()
        print(record[2])
        kb = await keyboard.generate_list(record[1])
        muscle = FSInputFile(record[2])
        await bot.send_photo(chat_id=user_id, photo=muscle, reply_markup=keyboard.generate_answer_keyboard(kb, record[1]))
    else:
        await bot.send_message(chat_id=user_id, text="Вы ответили на все предложенные вопросы. Теперь они будут повторяться. Нажмите еще раз, чтобы начать.")
        db.delete_record(user_id)


