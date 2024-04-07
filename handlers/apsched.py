from aiogram import Bot, Router, F
from aiogram.types import FSInputFile, CallbackQuery
from db.methods import *
from keyboards.keyboard import *

apscheduler_router = Router()


async def every_day(bot: Bot, ) -> None:
    users = await models.User.all()
    for user in users:
        record = await get_random_record()
        answer_list = await generate_list(record.name)
        image_path = FSInputFile(record.image_path)
        await bot.send_photo(chat_id=user.user_id,
                             photo=image_path,
                             reply_markup=generate_every_day(answer_list, record.name))


@apscheduler_router.callback_query(lambda f: f.data == 'Молодец' or f.data == 'Плохо')
async def callback_every_day(call: CallbackQuery):
    await call.answer()
    if call.data == "Молодец":
        await call.message.answer(text='Молодец, правильно ответил на ежедневный вопрос!')
    elif call.data == "Плохо":
        await call.message.answer(text=f'Попробуй в следующий раз')
    await call.message.delete_reply_markup()

