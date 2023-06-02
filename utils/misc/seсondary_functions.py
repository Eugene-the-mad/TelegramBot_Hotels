from typing import Any, Optional
import datetime
import locale
import json
import re


def found_cities(values: dict[str, Any]) -> dict[str, str]:
    """
    Функция для фильтрации ответа сервера по городам ('type': 'CITY)
    :return dic[str, str] - возвращает словарь, где ключ - название города,
                            а значение ключа - его gaiaId значение
    """
    all_city_find = values['sr']

    return {
        val['regionNames']['fullName']: val['gaiaId']
        for val in all_city_find
        if val['type'] == 'CITY'
    }


def beautiful_date(date: datetime) -> str:
    """
    Форматирование даты по локации: если не РФ, то строка переводится в нижний
    регистр, иначе принудительно устанавливается локация РФ,
    название месяца переводится в нижний регистр и меняется его падеж
    """
    if locale.getlocale()[0] in ('Russian_Russia', 'ru_RU'):
        locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
        date = date.strftime("%d %B %Y года").split(' ')
        month = date[1].lower()
        if month.startswith('авг') or month.startswith('мар'):
            month = month + 'а'
        else:
            month = month[:-1] + 'я'
        date[1] = month

        return ' '.join(date)

    else:
        date = date.strftime("%d %B %Y").lower()

        return date


def found_hotels(values: dict[Any, Any], num_h: Optional[str] = None) -> dict[str, str]:
    """
    Функция для выборки из ответа от сервера названия отеля и его id.
    Если в функцию передается переменная num_h, то функция переворачивает список отелей и создаёт
    новый словарь с количеством элементов равным num_h.
    :return dic[str, str] - возвращает словарь, где ключ - название отеля,
                            а значение ключа - его id значение
    """
    all_hotels = values['data']['propertySearch']['properties']
    result = {val['name']: val['id'] for val in all_hotels}

    if num_h:
        result = {
            key: val for key, val
            in list(reversed(result.items()))[:int(num_h)]
        }

        return result

    return result


def hotels_info(
        values: dict[str, Any], c_in: datetime, c_out: datetime, distance: int = 0
        ) -> dict[str, list[int]]:
    """
    Функция для фильтрации ответа сервера по определенный критериям отелей: стоимость за сутки,
    общая стоимость, расстояние от центра. Использует информацию об оплате из ответа от сервера,
    если отсутствует цена за сутки, то устанавливает цену равной нулю, если нет информации за
    общий период, то сама вычисляет из расчёта цена за сутки и общей продолжительности проживания.
    Если информация об расстоянии от центра отсутствует, то присваивает значение равно нулю.
    :return dic[str, list] - возвращает словарь, где ключ - название отеля, а значение ключа -
                            отфильтрованные значения в виде списка.
    """
    all_hotels = values['data']['propertySearch']['properties']
    all_hotels_info = dict()
    total_live = (c_out - c_in).days
    for val in all_hotels:
        name_hotel = val['name']

        if val['destinationInfo']['distanceFromDestination']['value']:
            destination = int(val['destinationInfo']['distanceFromDestination']['value'] * 1000.61)
            if destination > distance != 0:
                continue

        else:
            destination = 0
        val = json.dumps(val)
        pattern_price = r'(?<=formattedDisplayPrice":."\D)\d+[.,]*\d+(?=")'
        pattern_total_price = r'(?<=value":."\D)\d+[.,]*\d+(?=\Dtotal)'
        price = re.search(pattern_price, val)
        total_price = re.search(pattern_total_price, val)
        if price:
            price = price.group()
            price = int(re.sub('[^0-9]', '', price))
        else:
            price = 0
        if total_price:
            total_price = total_price.group()
            total_price = int(re.sub('[^0-9]', '', total_price))
        else:
            total_price = total_live * price
        all_hotels_info[name_hotel] = [price, total_price, destination]

    return all_hotels_info


def policies(val: Any) -> str:
    """
    Функция, проверяющая полученный объект на наличие в нём информации и
    возвращающая строку с заданным форматированием.
    """
    content = ''
    if val:
        if isinstance(val, list):
            content = '\n'.join(['- ' + text[:1].lower() + text[1:] + '.' for text in val])
        elif isinstance(val, str):
            content = val
        elif isinstance(val, dict):
            content = str(val['rating']) + '\U00002B50'
    else:
        content = 'на сайте нет информации'

    return content
