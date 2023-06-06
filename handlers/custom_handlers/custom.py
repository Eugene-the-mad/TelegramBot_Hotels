from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from API_requests import api_requests, current_rate_USD
from states import UserState
from utils import found_hotels, hotels_info
from keyboards.inline import *
from database import *
import datetime

router = Router()


@router.message(Command('custom'))
@router.message(Text('Поиск по параметрам'))
async def send_custom(message: types.Message, state: FSMContext) -> None:
    """
    Этот обработчик будет вызываться при нажатии на кнопку
    Поиск по параметрам либо по команде /custom
    """
    # запись в историю просмотренные отели, если был совершен некорректный выход из просмотра списка отелей путем
    # вызова другой команды
    all_data = await state.get_data()
    if 'hotels_review' in all_data.keys():
        hotels_names = 'Просмотренные отели: ' + ', '.join(all_data['hotels_review'])
        await insert_user_action((message.from_user.id, datetime.datetime.now(), hotels_names))
    await state.clear()
    await insert_user_action((message.from_user.id, datetime.datetime.now(), 'Поиск по параметрам пользователя:'))
    now_rate: int = current_rate_USD()
    await state.update_data(sort_price='custom', now_rate=now_rate)
    await message.answer('В каком городе будем искать отели? Напишите название города:')
    await state.set_state(UserState.cities)


@router.callback_query(Text(startswith='customphotoLoad_'))
async def check_photo_custom(callback: types.CallbackQuery, state: FSMContext) -> None:
    photo_load = callback.data.split('_')[1]
    await state.update_data(hot_photo=photo_load)
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(f'Загружать фото отелей: <b>{photo_load}</b>')
    await callback.message.answer('Перейдем к выбору порога цен номеров. Валюта - рубль.\nУкажите минимальную цену:')
    await state.set_state(UserState.price_min)


@router.message(UserState.price_min)
async def check_price_min(message: types.Message, state: FSMContext) -> None:
    min_price = message.text

    if not min_price.isdigit():
        await message.answer(
            'Видимо опечатка. Введите значение только арабскими цифрами. Попробуйте еще раз.'
            '\nУкажите минимальную цену:'
        )
        await state.set_state(UserState.price_min)
    else:
        await state.update_data(price_val=min_price)
        await message.answer(f'Минимальная цена за номер: <b>{min_price}</b>')
        await message.answer(f'Укажите максимальную цену за номер:')
        await state.set_state(UserState.price_max)


@router.message(UserState.price_max)
async def check_price_max(message: types.Message, state: FSMContext) -> None:
    max_price = message.text
    all_data = await state.get_data()

    if not max_price.isdigit():
        await message.answer(
            'Видимо опечатка. Введите значение только арабскими цифрами. Попробуйте еще раз.'
            '\nУкажите максимальную цену:'
        )
        await state.set_state(UserState.price_max)

    elif int(max_price) <= int(all_data['price_val']):
        await message.answer(
            '<Будьте внимательны. Максимальная цена должна быть больше минимальной. Попробуйте еще раз.'
            '\nУкажите максимальную цену:'
        )
        await state.set_state(UserState.price_max)

    else:
        await state.update_data(price_val=[all_data['price_val'], max_price])
        await message.answer(f'Максимальная цена за номер: <b>{max_price}</b>')
        await state.set_state(state=None)
        await message.answer(
            f'Выбор отелей ни ниже общего рейтинга гостей:',
            reply_markup=rate_guests()
        )


@router.callback_query(Text(startswith='rate_guests:'))
async def check_rate_guest(callback: types.CallbackQuery, state: FSMContext) -> None:
    r_guests = callback.data.split(':')
    await state.update_data(rate_guests=[r_guests[2], r_guests[1]], star_hotel={})
    await callback.message.delete()
    await callback.message.answer(f'Общий рейтинг отелей: <b>{r_guests[1]}</b>.')
    await callback.message.answer(
        'Перейдем к выбору звёзд отеля.\nВыберите количество звёзд и нажмите кнопку <b>Продолжить</b> ('
        'возможен выбор нескольких вариантов) или <b>Нажмите не учитывать звёзды отеля</b>:',
        reply_markup=star_hotel()
    )


@router.callback_query(Text(startswith='star_hotel:'))
async def check_hotel_star(callback: types.CallbackQuery, state: FSMContext) -> None:
    stars = callback.data.split(':')
    all_data = await state.get_data()
    if stars[2] == 'not':
        await state.update_data(star_hotel='not')
        await callback.message.delete()
        if 'm_id' in all_data.keys():
            await callback.message.chat.delete_message(message_id=all_data['m_id'])
        await callback.message.answer(f'Выбранное количество звезд: <b>{stars[1]}</b>.')
        await callback.message.answer(
            'Укажите крайний параметр поиска - Максимальное расстояние от отеля до центра города в метрах:')
        await state.set_state(UserState.distance)

    elif stars[2] == 'end':
        await callback.message.delete()
        if not all_data['star_hotel']:
            await state.update_data(star_hotel='not')
            await callback.message.answer(f'Выбранное количества звезд: <b>Не учитывать количество звезд отеля</b>.')
        await callback.message.answer(
            'Укажите крайний параметр поиска - Максимальное расстояние от отеля до центра города в метрах:')
        await state.set_state(UserState.distance)

    else:
        num_stars = all_data['star_hotel']
        num_stars[stars[2]] = stars[1]
        await state.update_data(star_hotel=num_stars)
        chosen_star = dict(sorted(num_stars.items(), key=lambda i: i[0])).values()
        if len(chosen_star) == 1:
            m_id = await callback.message.answer(f'Выбранные количества звезд: <b>{", ".join(chosen_star)}</b>.')
            await state.update_data(m_id=m_id.message_id)
        else:
            await callback.message.chat.delete_message(message_id=all_data['m_id'])
            m_id = await callback.message.answer(
                text=f'Выбранные количества звезд: <b>{", ".join(chosen_star)}</b>.'
            )
            await state.update_data(m_id=m_id.message_id)


@router.message(UserState.distance)
async def check_info_search_custom(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or message.text == '0':
        await message.answer(
            'Видимо опечатка. Расстояние должно быть только арабскими цифрами, целым числом и не'
            'равно нолю. Повторите ввод:'
        )
        await state.set_state(UserState.distance)
    else:
        await state.update_data(distance=int(message.text))
        await state.set_state(state=None)
        all_data = await state.get_data()
        chosen_star = 'Не учитывать количество звезд отеля'
        if all_data['star_hotel'] != 'not':
            chosen_star = ', '.join(dict(sorted(all_data['star_hotel'].items(), key=lambda i: i[0])).values())

        await message.answer(
            'Отлично. Проверьте еще раз выбранные данные и нажмите кнопку <b>Продолжить</b>. '
            'Если хотите изменить данные - нажмите кнопку '
            '<b>Отмена</b>.\n\n'
            f'Город: <b>{all_data["city"]}</b>,\n'
            f'Дата заезда: <b>{all_data["check_in"][1]}</b>,\n'
            f'Дата выселения: <b>{all_data["check_out"][1]}</b>,\n'
            f'Количество персон: <b>{all_data["num_pers"]}</b>,\n'
            f'Максимально количество отелей: <b>{all_data["num_hotels"]}</b>,\n'
            f'Минимальная цена за номер: <b>{all_data["price_val"][0]} руб.</b>,\n'
            f'Максимальная цена за номер: <b>{all_data["price_val"][1]} руб.</b>,\n'
            f'Рейтинг отеля гостями: <b>{all_data["rate_guests"][1]}</b>.\n'
            f'Количество звезд: <b>{chosen_star}</b>.\n'
            f'Расстояние от отеля до центра города: <b>{all_data["distance"]} м</b>.\n'
            f'Загружать фото отелей: <b>{all_data["hot_photo"]}</b>.',
            reply_markup=next_canc(all_data['sort_price'] + 'search:')
        )


@router.callback_query(Text(startswith='customsearch:Продолжить'))
async def hotels_find_custom(callback: types.CallbackQuery, state: FSMContext) -> None:
    detail_info = 'Параметры поиска:\n' + callback.message.text.split('\n\n')[1]
    await insert_user_action((callback.from_user.id, datetime.datetime.now(), detail_info))
    await callback.message.delete_reply_markup()
    all_data = await state.get_data()
    now_rate = all_data['now_rate']

    waiting = await callback.message.answer('\U000023F3')
    params = {
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
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": int(all_data["num_hotels"]),
        "sort": "PRICE_RELEVANT",
        "filters": {
            "price": {
                "max": int(int(all_data["price_val"][1]) / now_rate),
                "min": int(int(all_data["price_val"][0]) / now_rate)
            },
            "availableFilter": "SHOW_AVAILABLE_ONLY"
        }
    }
    if all_data['star_hotel'] != 'not':
        params["filters"]["star"] = [i for i in all_data['star_hotel'].keys()]
    if all_data['rate_guests'] != 'not':
        params["filters"]["guestRating"] = all_data['rate_guests'][0]

    search_hotels = api_requests(
        method_endswith='properties/v2/list',
        method='post',
        params=params
    )
    await callback.message.chat.delete_message(message_id=waiting.message_id)

    if 'errors' in search_hotels.keys():
        await insert_user_action((callback.from_user.id, datetime.datetime.now(), 'По Вашему запросу отели не найдены'))
        await callback.message.answer(
            '<b>По Вашему запросу отели не найдены.</b>\n'
            'Повторить поиск по новым параметрам - нажмите <b>Продолжить</b>, '
            'или чтобы вернуться в главное меню бота нажмите <b>Отмена</b>.',
            reply_markup=next_canc(elem='not_result:')
        )

    else:
        all_hotels_find: dict[str, str] = found_hotels(search_hotels, num_h=None, distance=all_data['distance'])
        all_hotels_find_info: dict[str, list[int]] = hotels_info(
            search_hotels, all_data['check_in'][0], all_data['check_out'][0]
        )
        await state.update_data(all_hotels=all_hotels_find)
        await state.update_data(all_hotels_info=all_hotels_find_info)
        await callback.message.answer(
            "Выберите отель из списка:",
            reply_markup=select_kb(all_hotels_find, val='hotels:'),
        )
