import aiogram.exceptions
from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto
from API_requests import api_requests, current_rate_USD
from states import UserState
from utils import found_cities, beautiful_date, found_hotels, hotels_info, policies
from keyboards.inline import *
from keyboards.reply import def_keyboard
from aio_calendar import dialog_cal_callback, DialogCalendar
import datetime
from typing import Any

router = Router()


@router.message(Command('low'))
@router.message(Text('Наименьшая стоимость'))
async def send_low(message: types.Message, state: FSMContext) -> None:
    """
    Этот обработчик будет вызываться при нажатии на кнопку
    Наименьшая стоимость либо по команде /low
    """
    now_rate: int = current_rate_USD()
    await state.update_data(sort_price='low', now_rate=now_rate)
    await message.answer('В каком городе будем искать отели? Напишите название города:')
    await state.set_state(UserState.cities)


@router.message(UserState.cities)
async def send_city(message: types.Message, state: FSMContext) -> None:
    """
    Этот обработчик будет вызываться при вводе названия города пользователем
    """
    if not message.text.isalpha():
        await message.answer(
            'В названии города не должность быть цифр и других символов, отличных от букв алфавита. '
            'Введите название города ещё раз:'
        )
        await state.set_state(UserState.cities)

    else:
        waiting = await message.answer('\U000023F3')
        search_city = api_requests(
            method_endswith='locations/v3/search',
            method='get',
            params={"q": message.text, "locale": "en_US"}
        )
        await message.chat.delete_message(message_id=waiting.message_id)

        if search_city['rc'] == 'GOOGLE_AUTOCOMPLETE':
            await message.answer(
                'Бот не знает такого города. Введите другое название:'
            )
            await state.set_state(UserState.cities)

        else:
            all_city_find: dict[str, str] = found_cities(search_city)

            if not all_city_find:
                await message.answer(
                    'Бот не знает такого города. Введите другое название:'
                )
                await state.set_state(UserState.cities)

            else:
                await state.update_data(all_city=all_city_find)
                await message.answer("Уточните поиск по локации из списка:",
                                     reply_markup=select_kb(all_city_find, val='gaiaID:'))


@router.callback_query(Text(startswith='gaiaID'))
async def check_city(callback: types.CallbackQuery, state: FSMContext) -> None:
    all_cities = await state.get_data()
    await state.set_state(state=None)
    id_city = callback.data.split(':')[1]
    main_city = [
        elem for elem, val in all_cities['all_city'].items()
        if val == id_city
    ]
    await state.update_data(city=main_city[0], id=id_city)
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(f'Отлично. Выбранная локация:\n<b>{main_city[0]}</b>\n')
    await callback.message.answer(
        'Выберите дату заселения:',
        reply_markup=await DialogCalendar().start_calendar()
    )


@router.callback_query(dialog_cal_callback.filter())
async def check_in_date(callback_query: CallbackQuery, callback_data: dict, state: FSMContext) -> None:
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        data_mem = await state.get_data()
        if not data_mem.get('check_in'):
            if date >= datetime.datetime.now():
                beautfl_date = beautiful_date(date)
                await state.update_data(check_in=[date, beautfl_date])
                await callback_query.message.edit_text(
                    f'Дата заселения: <b>{beautfl_date}</b>.'
                )
                await callback_query.message.answer(
                    'Выберите дату выселения:',
                    reply_markup=await DialogCalendar().start_calendar()
                )
            else:
                await callback_query.message.edit_text(
                    '<b>Видимо, ошиблись.</b> Дата заселения не должна быть в прошлом.\n'
                    'Выберите дату заселения еще раз:',
                    reply_markup=await DialogCalendar().start_calendar()
                )
        else:
            if date > data_mem['check_in'][0]:
                beautfl_date = beautiful_date(date)
                await state.update_data(check_out=[date, beautfl_date])
                await callback_query.message.edit_text(
                    f'Дата выселения: <b>{beautfl_date}</b>.'
                )
                await callback_query.message.answer(
                    'Укажите количество персон для заселения:',
                    reply_markup=num_person()
                )
            else:
                await callback_query.message.edit_text(
                    '<b>Видимо, ошиблись.</b> Дата выселения должна быть позже даты заселения.\n'
                    'Выберите дату выселения еще раз:',
                    reply_markup=await DialogCalendar().start_calendar()
                )


@router.callback_query(Text(startswith='person'))
async def check_person(callback: types.CallbackQuery, state: FSMContext) -> None:
    num_pers = callback.data.split('_')[1]
    await state.update_data(num_pers=num_pers)
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(f'Количество персон: <b>{num_pers}</b>.')
    await callback.message.answer(
        'Какое максимальное количество отелей показать? Введите количество: '
    )
    await state.set_state(UserState.hotels)


@router.message(UserState.hotels)
async def select_photo(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() or message.text == '0':
        await message.answer('Количество отелей должно быть только арабской цифрой и больше нуля! Повторите ввод.')
        await state.set_state(UserState.hotels)
    else:
        all_data = await state.get_data()
        cust_param = ''
        if all_data['sort_price'] == 'custom':
            cust_param = 'custom'
        await state.set_state(state=None)
        await state.update_data(num_hotels=message.text)
        await message.answer(f'Максимальное количество отелей: <b>{message.text}</b>.')
        await message.answer(
            'Выберите, загружать ли фото отелей:',
            reply_markup=y_n(cust_param + 'photoLoad_')
        )


@router.callback_query(Text(startswith='photoLoad_'))
async def check_info_search(callback: types.CallbackQuery, state: FSMContext) -> None:
    photo_load = callback.data.split('_')[1]
    await state.update_data(hot_photo=photo_load)
    all_data = await state.get_data()
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(f'Загружать фото отелей: <b>{photo_load}</b>')
    await callback.message.answer(
        'Отлично. Проверьте еще раз выбранные данные и нажмите кнопку <b>Продолжить</b>. '
        'Если хотите изменить даты заселения/выселения, количество персон - нажмите кнопку '
        '<b>Отмена</b>.\n\n'
        f'Город: <b>{all_data["city"]}</b>,\n'
        f'Дата заезда: <b>{all_data["check_in"][1]}</b>,\n'
        f'Дата выселения: <b>{all_data["check_out"][1]}</b>,\n'
        f'Количество персон: <b>{all_data["num_pers"]}</b>,\n'
        f'Максимально количество отелей: <b>{all_data["num_hotels"]}</b>,\n'
        f'Загружать фото отелей: <b>{all_data["hot_photo"]}</b>.',
        reply_markup=next_canc(all_data['sort_price'] + 'search:')
    )


@router.callback_query(Text(endswith='search:Отмена'))
async def return_to_middle(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(check_in=None, check_out=None)
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        '<b>Выберем данные повторно</b>.\nВыберите дату заселения:',
        reply_markup=await DialogCalendar().start_calendar()
    )


@router.callback_query(Text(startswith='lowsearch:Продолжить'))
async def hotels_find_low(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete_reply_markup()
    all_data = await state.get_data()

    waiting = await callback.message.answer('\U000023F3')
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
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": int(all_data["num_hotels"]),
            "sort": "PRICE_LOW_TO_HIGH",
            "filters": {
                "price": {
                    "max": 1000000,
                    "min": 1
                },
                'availableFilter': 'SHOW_AVAILABLE_ONLY'
            }
        }
    )
    await callback.message.chat.delete_message(message_id=waiting.message_id)

    if 'errors' in search_hotels.keys():
        await callback.message.answer(
            '<b>По Вашему запросу отели не найдены.</b>\n'
            'Повторить поиск, указав новые значения - нажмите <b>Продолжить</b>.\n'
            'Чтобы вернуться в главное меню бота нажмите <b>Отмена</b>.',
            reply_markup=next_canc(elem='not_result:')
        )

    else:
        all_hotels_find: dict[str, str] = found_hotels(search_hotels, num_h=None)
        all_hotels_find_info: dict[str, list[int]] = hotels_info(
            search_hotels, all_data['check_in'][0], all_data['check_out'][0]
        )
        await state.update_data(all_hotels=all_hotels_find)
        await state.update_data(all_hotels_info=all_hotels_find_info)
        await callback.message.answer(
            "Выберите отель из списка:",
            reply_markup=select_kb(all_hotels_find, val='hotels:'),
        )


@router.callback_query(Text(startswith='not_result:Продолжить'))
async def return_to_begin(callback: types.CallbackQuery, state: FSMContext) -> None:
    all_data = await state.get_data()
    now_rate = all_data['now_rate']
    sort_price = all_data['sort_price']
    await state.clear()
    await callback.message.edit_reply_markup()
    await state.update_data(sort_price=sort_price, now_rate=now_rate)
    await callback.message.answer('В каком городе будем искать отели? Напишите название города:')
    await state.set_state(UserState.cities)


@router.callback_query(Text(startswith='hotels:'))
async def check_search_info(callback: types.CallbackQuery, state: FSMContext) -> None:
    id_hotel: str = callback.data.split(':')[1]
    all_data = await state.get_data()
    await callback.message.delete()

    waiting = await callback.message.answer('\U000023F3')
    detail_hotel: dict[Any, Any] = api_requests(
        method_endswith='properties/v2/detail',
        method='post',
        params={
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": id_hotel
        }
    )

    if all_data['hot_photo'] == 'Да':
        images_list = list()
        for i in range(30):
            try:
                image = InputMediaPhoto(
                    media=detail_hotel['data']['propertyInfo']['propertyGallery']['images'][i]['image']['url']
                )
                images_list.append(image)
            except (KeyError, IndexError):
                break
        while True:
            try:
                if images_list:
                    await callback.message.answer_media_group(media=images_list)
                    break
                else:
                    await callback.message.answer('Для данного отеля нет фотографий.')
            except aiogram.exceptions.TelegramBadRequest:
                del images_list[-1]

    await callback.message.chat.delete_message(message_id=waiting.message_id)
    name_hotel = detail_hotel["data"]["propertyInfo"]["summary"]["name"]
    now_rate = all_data['now_rate']

    await callback.message.answer(
        f'Название отеля: <b>{name_hotel}</b>.\n'
        f'<i><b>"{policies(detail_hotel["data"]["propertyInfo"]["summary"]["tagline"].rstrip())}"</b></i>.\n'
        'Количество звезд: <b>'
        f'{policies(detail_hotel["data"]["propertyInfo"]["summary"]["overview"]["propertyRating"])}</b>.\n'
        'Оценка отеля по отзывам: <b>'
        f'{policies(detail_hotel["data"]["propertyInfo"]["reviewInfo"]["summary"]["overallScoreWithDescriptionA11y"]["value"])}'
        '</b>.\n\n'
        'Транспортные и иные услуги:\n<i>'
        f'{policies(detail_hotel["data"]["propertyInfo"]["summary"]["policies"]["checkinInstructions"])}'
        '</i>\n'
        f'Адрес: <b>{policies(detail_hotel["data"]["propertyInfo"]["summary"]["location"]["address"]["addressLine"])}</b>.\n'
        f'Цена за номер: <b>{round(all_data["all_hotels_info"][name_hotel][0] * now_rate, 2)} руб</b>.\n'
        f'Цена за указанные период: <b>{round(all_data["all_hotels_info"][name_hotel][1] * now_rate, 2)} руб</b>.\n'
        f'Расстояние до центра города: <b>{all_data["all_hotels_info"][name_hotel][2]}</b>.'
    )

    await callback.message.answer(
        'Что делаем дальше? Выберите один из вариантов действий:\n'
        'ОТМЕНА - заканчиваем поиск,\n'
        'ПРОДОЛЖИТЬ - просмотреть список отелей.',
        reply_markup=next_canc('list_hotels:')
    )


@router.callback_query(Text(startswith='list_hotels:Продолжить'))
async def continue_show(callback: types.CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    all_data = await state.get_data()
    all_hotels_find = all_data['all_hotels']
    await callback.message.answer(
        "Выберите отель из списка:",
        reply_markup=select_kb(all_hotels_find, val='hotels:')
    )


@router.callback_query(Text(startswith=['list_hotels:Отмена', 'not_result:Отмена']))
async def return_start(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        'Выберите действие для бота из кнопок ниже:',
        reply_markup=def_keyboard
    )
