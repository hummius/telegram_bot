import requests
from config_data import config
import re


def get_location_id(location: str) -> str:
    """
    Функция делает запрос в API с параметром в виде введенного названия локации от пользователя.
    После чего, извлекает из ответа и возвращает ID локации.

    :param location: локация из сообщения пользователя.
    :return: str: строка с ID локации
    """
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": location}
    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring, timeout=20)
    location_id = re.findall(r'gaiaId":"(\d+)"', response.text)[0]

    return location_id