from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from API_requests import api_requests, current_rate_USD
from handlers.custom_handlers.low import err_end
from states import UserState
from utils import found_hotels, hotels_info
from keyboards.inline import *
from database import *
import datetime

router = Router()


@router.message(Command('high'))
@router.message(Text('Наибольшая стоимость'))
async def send_high(message: types.Message, state: FSMContext) -> None:
    """
    Этот обработчик будет вызываться при нажатии на кнопку
    Наибольшая стоимость либо по команде /high
    """
    # запись в историю просмотренные отели, если был совершен некорректный выход из просмотра списка отелей путем
    # вызова другой команды
    all_data = await state.get_data()
    if 'hotels_review' in all_data.keys():
        hotels_names = 'Просмотренные отели: ' + ', '.join(all_data['hotels_review'])
        await insert_user_action((message.from_user.id, datetime.datetime.now(), hotels_names))

    await state.clear()
    now_rate: int = current_rate_USD()
    await insert_user_action((message.from_user.id, datetime.datetime.now(), 'Поиск по наибольшей стоимости:'))
    await state.update_data(sort_price='high', now_rate=now_rate)
    await message.answer(
        'В каком городе будем искать отели <b>(города РФ временно не доступны)</b>? Напишите название города:'
    )
    await state.set_state(UserState.cities)


@router.callback_query(Text(startswith='highsearch:Продолжить'))
async def hotels_find_high(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Этот обработчик будет вызываться при нажатии инлайн-кнопки Продолжить для подтверждения
    параметров запроса на поиск отелей по наибольшей цене.
    Производит запрос к api сервера меняя порог минимальной величины стоимости отелей до тех пор,
    пока не будет в ответе не более 200 отелей для дальнейшей их сортировки по убыванию цены.
    """
    detail_info = 'Параметры поиска:\n' + callback.message.text.split('\n\n')[1]
    await insert_user_action((callback.from_user.id, datetime.datetime.now(), detail_info))
    await callback.message.delete_reply_markup()
    all_data = await state.get_data()
    all_hotels_find = dict()

    hourglass_emoji = '\U000023F3'
    waiting = await callback.message.answer(hourglass_emoji)
    min_num = 50
    while True:
        search_hotels = api_requests(
            method_endswith='properties/v2/list',
            method='post',
            params={
                "currency": "USD",
                "eapid": 1,
                "locale": "en_US",
                "siteId": 300000001,
                "destination": {"regionId": str(all_data["id"])},
                "checkInDate": {
                    "day": int(all_data["check_in"][0].strftime("%d")),
                    "month": int(all_data["check_in"][0].strftime("%m")),
                    "year": int(all_data["check_in"][0].strftime("%Y"))
                },
                "checkOutDate": {
                    "day": int(all_data["check_out"][0].strftime("%d")),
                    "month": int(all_data["check_out"][0].strftime("%m")),
                    "year": int(all_data["check_out"][0].strftime("%Y"))
                },
                "rooms": [
                    {
                        "adults": int(all_data["num_pers"]),
                        "children": []
                    }
                ],
                "resultsStartingIndex": 0,
                "resultsSize": 200,
                "sort": "PRICE_LOW_TO_HIGH",
                "filters": {
                    "price": {
                        "max": 1000000,
                        "min": min_num
                    },
                    'availableFilter': 'SHOW_AVAILABLE_ONLY'
                }
            }
        )

        if not search_hotels:
            await err_end(callback.message, state)
            break

        if 'errors' in search_hotels.keys():
            break
        elif len(search_hotels['data']['propertySearch']['properties']) == 200:
            min_num += 20
            continue
        else:
            all_hotels_find: dict[str, str] = found_hotels(search_hotels, num_h=all_data["num_hotels"])
            break

    await callback.message.chat.delete_message(message_id=waiting.message_id)

    if not all_hotels_find:
        await insert_user_action(
            (callback.from_user.id, datetime.datetime.now(), 'По Вашему запросу отели не найдены')
        )
        await callback.message.answer(
            '<b>По Вашему запросу отели не найдены.</b>\n'
            'Повторить поиск по новым параметрам - нажмите <b>Продолжить</b>, '
            'или чтобы вернуться в главное меню бота нажмите <b>Отмена</b>.',
            reply_markup=next_canc(elem='not_result:')
        )

    else:
        all_hotels_find_info: dict[str, list[int]] = hotels_info(
            search_hotels, all_data['check_in'][0], all_data['check_out'][0]
        )
        await state.update_data(all_hotels=all_hotels_find)
        await state.update_data(all_hotels_info=all_hotels_find_info)
        await callback.message.answer(
            "Выберите отель из списка:",
            reply_markup=select_kb(all_hotels_find, val='hotels:'),
        )
