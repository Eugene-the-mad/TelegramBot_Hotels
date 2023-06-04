from typing import Optional
from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from keyboards.reply import def_keyboard
from states import UserState
from database import check_name

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    """
    Этот обработчик будет вызываться по команде /start.
    Проверяет на наличие нового пользователя, выводит окно приветствия для начала работы бота.
    """
    user_name: Optional[tuple[str]] = await check_name(message.from_user.id)
    if user_name:
        await message.answer(
            f'Привет, {user_name[0]}. Рад снова Вас видеть. Начнем работу.'
            f'\nВыберите действие для бота из кнопок ниже:',
            reply_markup=def_keyboard
            )
    else:
        await message.answer(
            f"Привет {message.from_user.first_name}, я EugeneBot, готов оказать Вам помощь в поиске "
            f"отелей по различным критериям. Для начала познакомимся. Как Вас зовут?"
            )
        await state.set_state(UserState.name)
