from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from states import UserState
from keyboards.inline import *
from aio_calendar import dialog_cal_callback, DialogCalendar
from database import *

router = Router()


@router.message(Command('history'))
@router.message(Text('История запросов'))
async def send_history(message: types.Message) -> None:
    """
    Этот обработчик будет вызываться при нажатии на кнопку История запросов либо по команде /history.
    Выводит инлайн-клавиатуру для выбора критериев истории запросов.
    """
    await message.answer('Выберите период отображения Ваших запросов:', reply_markup=history_selection())


@router.callback_query(Text(startswith='history:today'))
async def history_today(callback: CallbackQuery) -> None:
    """
    Этот обработчик будет вызываться при нажатии на инлайн-кнопку Сегодня.
    Выводит историю запросов пользователя за текущий день.
    """
    param = callback.data.split(':')[1]
    history_log = await search_user_action(user_id=callback.from_user.id, param=param)
    await callback.message.delete()

    if history_log:
        await callback.message.answer(history_log)
    else:
        await callback.message.answer('Сегодня Вы не делали запросы.')

    await history_end(callback.message)


@router.callback_query(Text(startswith='history:yesterday'))
async def history_yesterday(callback: CallbackQuery) -> None:
    """
    Этот обработчик будет вызываться при нажатии на инлайн-кнопку Вчера.
    Выводит историю запросов пользователя за вчерашний день.
    """
    param = callback.data.split(':')[1]
    history_log = await search_user_action(user_id=callback.from_user.id, param=param)
    await callback.message.delete()

    if history_log:
        await callback.message.answer(history_log)
    else:
        await callback.message.answer('Вчера у Вас не было запросов.')

    await history_end(callback.message)


@router.callback_query(Text(startswith='history:custom'))
async def history_custom(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Этот обработчик будет вызываться при нажатии на инлайн-кнопку Указать дату.
    Переводит пользователя к выбору даты запросов через инлайн-календарь.
    """
    await callback.message.delete()
    await callback.message.answer(
        'Выберите дату для просмотра истории запросов:',
        reply_markup=await DialogCalendar().start_calendar()
    )
    await state.set_state(UserState.history_select)


@router.callback_query(UserState.history_select, dialog_cal_callback.filter())
async def check_in_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    """
    Этот обработчик будет вызываться после выбора даты пользователем в инлайн-календаре.
    Выводит запросы пользователя за указанную дату.
    """
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        param = 'custom'
        history_log = await search_user_action(user_id=callback_query.from_user.id, param=param, date_user=date)
        if history_log:
            await callback_query.message.answer(history_log)
        else:
            await callback_query.message.answer(f'{date.date()} у Вас не было запросов.')
        await state.set_state(state=None)
        await history_end(callback_query.message)


@router.callback_query(Text(startswith='history:all'))
async def history_custom(callback: types.CallbackQuery) -> None:
    """
    Этот обработчик будет вызываться при нажатии на инлайн-кнопку За всё время.
    Выводит пользователю всю историю его запросов, сортирую по датам.
    """
    param = callback.data.split(':')[1]
    history_log = await search_user_action(user_id=callback.from_user.id, param=param)
    await callback.message.delete()

    if history_log:
        await callback.message.answer(history_log)
    else:
        await callback.message.answer('У Вас еще не было запросов.')

    await history_end(callback.message)


@router.callback_query(Text(startswith='history:Продолжить'))
async def history_start(callback: types.CallbackQuery) -> None:
    """
    Этот обработчик будет вызываться при нажатии на инлайн-кнопку Продолжить.
    Возвращает пользователя к выбору критериев вывода запросов.
    """
    await callback.message.delete()
    await send_history(callback.message)


async def history_end(message: types.Message) -> None:
    """
    Функция, при обращении к которой, выводит инлайн-клавиатуру с дальнейшими действиями
    """
    await message.answer('Что делаем дальше?\n'
                         '<b>Продолжить</b> - указать другие условия истории запросов,\n'
                         '<b>Отмена</b> - вернуться в главное меня Бота',
                         reply_markup=next_canc(elem='history:'))
