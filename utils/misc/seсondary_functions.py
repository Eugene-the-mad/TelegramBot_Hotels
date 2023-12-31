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
        if val['type'] == 'CITY' or val['type'] == 'NEIGHBORHOOD'
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


def found_hotels(
        values: dict[Any, Any], num_h: Optional[str] = None, distance: Optional[int] = None
) -> dict[str, str]:
    """
    Функция для выборки из ответа от сервера названия отеля и его id.
    Если в функцию передаётся переменная num_h, то функция переворачивает список отелей и создаёт
    новый словарь с количеством элементов равным num_h.
    Если в функцию передаётся переменная distance, то функция исключает из списка отели, которые находятся
    на расстоянии от центра города больше значения данной переменой.
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

    elif distance:
        result = {val['name']: val['id'] for val in all_hotels
                  if (val['destinationInfo']['distanceFromDestination']['value']
                      and int(val['destinationInfo']['distanceFromDestination']['value']) <= distance / 1610)
                  or not val['destinationInfo']['distanceFromDestination']['value']}

    return result


def hotels_info(values: dict[str, Any], c_in: datetime, c_out: datetime) -> dict[str, list[int, str]]:
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
            destination = str(int(val['destinationInfo']['distanceFromDestination']['value'] * 1610)) + ' м'
        else:
            destination = 'Не указано'

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
            # ловим возможную некорректную стоимость за период бронирования: предполагаем, что отель может
            # максимально дать 50% скидку за длительное проживание.
            if (total_price / total_live) < (price / 2):
                total_price = total_live * price
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


def output_children(children: dict[Any, Any]) -> str:
    """
    Функция, принимающая словарь с сохраненными данными в памяти и форматирующуя текст для
    корректного вывода количества и возраста детей.
    :param children: dict[Any, Any] - словарь всех данных, занесенных в память
    :return: str - отформатированная строка
    """
    if children.get('num_childs') == 0:

        return 'без детей'

    else:
        age_list = [
            (
                f'{num}-го ребёнка {age} год(а)'
                if age in [1, 2, 3, 4]
                else f'{num}-го ребёнка {age} лет'
            )
            for num, age in children['age_children'].items()
        ]

        return f'{children.get("num_childs")}, возраст {", ".join(age_list)}'
