from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from states import UserState
from keyboards.reply import def_keyboard
from database import insert_user_data

router = Router()


@router.message(UserState.name)
async def get_username(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер, срабатывающий при вводе имени пользователя. Проверяет ввод на корректность (
    в имени должны быть только буквы), заносит имя в БД. Переводит пользователя к началу
    работы Бота.
    """
    if message.text.isalpha():
        await state.update_data(username=message.text)
        data = await state.get_data()
        send_data = (message.from_user.first_name, message.from_user.id, data['username'])
        await insert_user_data(send_data)
        await state.clear()
        await message.answer(
            f'Приятно познакомится, {data["username"]}. Начнем работу. '
            f'\nВыберите действие для бота из кнопок ниже:',
            reply_markup=def_keyboard
        )
    else:
        await message.answer('Некорректный ввод имени. Оно должно состоять только из букв. '
                             'Попробуйте еще раз.')
        await state.set_state(UserState.name)
