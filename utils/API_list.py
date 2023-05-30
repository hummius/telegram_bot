import requests
from config_data import config
from typing import List, Dict, Any


def get_hotels_list(location_id: str, start_date: List, final_date: List,
                    filter_settings, hotels_amount: int = 200,
                    sort: str = "PRICE_LOW_TO_HIGH",) -> Dict:
    """
    Функция делает запрос на список отелей в API с параметром в виде ID локации.
    Получив ответ, извлекает и возвращает полученный список отелей с данными в формате json.

    :param filter_settings: параметры фильтра для поиска.
    :param sort: Принцип сортировки.
    :param location_id: ID локации.
    :param start_date: Дата въезда для поиска подходящих отелей.
    :param final_date: Дата последнего дня прибывания для поиска подходящих отелей.
    :param hotels_amount: Количество отелей запрашиваемое пользователем.
    :return: Список отелей с данными в формате json.
    """
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {'currency': 'USD',
               'eapid': 1,
               'siteId': 300000001,
               'destination': {
                   'regionId': location_id
               },
               'checkInDate': {'day': int(start_date[0]), 'month': int(start_date[1]),
                               'year': int(start_date[2])},
               'checkOutDate': {'day': int(final_date[0]), 'month': int(final_date[1]),
                                'year': int(final_date[2])},
               'rooms': [{'adults': 1}],
               'resultsStartingIndex': 0,
               'resultsSize': hotels_amount,
               'sort': sort,
               'filters': filter_settings
               }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers, timeout=20)

    return response.json()['data']['propertySearch']['properties']
