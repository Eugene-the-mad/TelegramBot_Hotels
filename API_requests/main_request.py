import requests
from typing import Any, Union
from config_data.config import config


def api_requests(method_endswith: str, method: str, params: dict[Any, Any]):
    """ Функция выполнения API запросов """
    url = f'https://hotels4.p.rapidapi.com/{method_endswith}'
    headers = {
        'X-RapidAPI-Key': config.x_rapid_api_key.get_secret_value(),
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }
    if method == 'get':
        return get_request(url, params, headers)
    else:
        return post_request(url, params, headers)


def get_request(url: str, params: dict[Any, Any], headers: dict[str, str]) -> Union[dict[Any, Any], int]:
    """ Функция выполнения get API запросов """
    req = requests.get(
        url=url,
        headers=headers,
        params=params,
        timeout=40
    )
    if req.status_code == requests.codes.ok:
        return req.json()
    else:
        return req.status_code


def post_request(url: str, params: dict[Any, Any], headers: dict[str, str]) -> dict[Any, Any]:
    """ Функция выполнения post API запросов """
    req = requests.post(
        url=url,
        json=params,
        headers=headers,
        timeout=40
    )
    if req.status_code == requests.codes.ok:
        return req.json()


def current_rate_USD() -> int:
    """ Функция выполнения API запроса на текущий курс доллара к рублю """
    key_api = config.currencyconverterapi.get_secret_value()
    data = requests.get(
        f'https://free.currconv.com/api/v7/convert?q=USD_RUB&compact=ultra&apiKey={key_api}'
    )
    if data.status_code == requests.codes.ok:
        return data.json()['USD_RUB']
    elif data.status_code == 400:
        print('Ваш токен к "currencyconverterapi.com" не верный. Проверьте его ещё раз либо запросите новый. '
              'Расчёт курса будет вестись по среднему значению равному 1 к 60.')
        return 60
