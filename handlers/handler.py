from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from utils.fsm import Form
import keyboards.keyboard as kb
from db import methods, models

router = Router()


@router.message(F.text.lower() == 'начать')
async def start_game(message: Message, state: FSMContext) -> None:
    record = await methods.get_random_record()
    all_record = await methods.user_has_seen_all_records(message.from_user.id)
    if all_record:
        while await models.UsersMuscles.exists(user_id=message.from_user.id, muscle_id_id=record.id):
            record = await methods.get_random_record()
            print(record.name)
        await state.update_data(RECORD_DATA=record)
        image_path = FSInputFile(record.image_path)
        print(image_path.path)
        answer_list = await kb.generate_list(record.name)
        await message.answer_photo(image_path, reply_markup=kb.generate_answer_keyboard(answer_list, record.name))
    else:
        await message.answer(
            'Вы ответили на все предложенные вопросы. Теперь они будут повторятся, но вам придется отвечать письменно'
            'Нажмите еще раз начать.', reply_markup=kb.main_keyboard(all_record))
        await models.UsersMuscles.filter(user_id=message.from_user.id).delete()


@router.message(F.text.lower() == 'топ')
async def get_top_users(message: Message):
    users = await methods.get_top_10_users()
    message_text = "Top 10 пользователей:\n"
    for i, user in enumerate(users, start=1):
        message_text += f"{i}. {user.username} уже ответил на {user.answer_count} вопросов👍\n"
    await message.answer(message_text)


@router.message(F.text.lower() == 'вопрос')
async def difficult_game(message: Message, state: FSMContext) -> None:
    record = await methods.get_random_record()
    if await methods.user_has_seen_all_records(message.from_user.id):
        while await models.UsersMuscles.exists(user_id=message.from_user.id, muscle_id_id=record.id):
            record = await methods.get_random_record()
            print(record.name)
        await state.update_data(RECORD_DATA=record)
        image_path = FSInputFile(record.image_path)
        print(image_path.path)
        await message.answer_photo(image_path)
        await message.answer("Напиши ответ при помощи текста")
        await state.set_state(Form.input)
    else:
        await message.answer(
            'Вы ответили на все предложенные вопросы. Теперь они будут повторятся, но вам придется отвечать письменно'
            ' Нажмите еще раз начать.',
            reply_markup=kb.main_keyboard(await methods.user_has_seen_all_records(message.from_user.id)))
        await models.UsersMuscles.filter(user_id=message.from_user.id).delete()


@router.message(F.text.lower() == 'назад')
async def process_answer(message: Message) -> None:
    await message.answer('Вы вернулись к стандартной сложности',
                         reply_markup=kb.main_keyboard(await methods.user_has_seen_all_records(message.from_user.id)))


@router.message(Form.input)
async def process_answer(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    record = data.get('RECORD_DATA')
    user_answer = message.text.lower().strip()
    correct_answer = record.name.lower().strip()
    if user_answer == correct_answer:
        await message.answer("Правильно!")
        new_answer = await models.UsersMuscles(user_id=message.from_user.id, muscle_id_id=record.id)
        await new_answer.save()
        user = await models.User.get(user_id=message.from_user.id)
        user.answer_count += 1
        await user.save()
    else:
        await message.answer("Неправильно. Попробуйте еще раз!")
        await message.answer(text=f'Неправильно, это {record.name}')
    await state.clear()


@router.callback_query(lambda f: f.data == 'Правильно' or f.data == 'Неправильно')
async def callback_input_data(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    record = data.get('RECORD_DATA')
    print("Retrieved record:", record)
    if callback.data == "Правильно":
        await callback.message.answer(text='Молодец, правильно!')
        if not await models.UsersMuscles.exists(user_id=callback.from_user.id, muscle_id_id=record.id):
            new_answer = await models.UsersMuscles(user_id=callback.from_user.id, muscle_id_id=record.id)
            await new_answer.save()
        user = await models.User.get(user_id=callback.from_user.id)
        user.answer_count += 1
        await user.save()
    elif callback.data == "Неправильно":
        await callback.message.answer(text=f'Неправильно, это {record.name}')
    await callback.message.delete_reply_markup()
    await state.clear()


@router.message(Command('help'))
async def command_help(message: Message) -> None:
    await message.answer('Для начала нажмите кнопку "НАЧАТЬ"')


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'''Привет! Добро пожаловать в тест на знание названий мышц!
Готов проверить свои знания? Просто отвечай на вопросы о названиях различных мышц. 
Попробуй дать правильные ответы! Если тебе нужна помощь или справка о доступных командах, просто напиши /help. 
Удачи в тестировании своих знаний!''', reply_markup=kb.main_keyboard(True))
