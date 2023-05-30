import requests
from config_data import config
from typing import Dict, Any
import re


def get_hotel_details(properties: Dict) -> Any:
    """
    Функция совершает запрос в API для получения данных по отелю.
    После получения ответа на запрос извлекает и возвращает информацию для вывода пользовелю.

    :param properties: данные полученные из функции get_hotels_list
    :return: Название отеля, полный адрес, дистанция от запрашиваемой локации,
            цена за ночь, полная сумма учитывая даты, список со ссылками на фото-контент,
            ID отеля.
    """
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {
        "propertyId": properties['id']
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response_detail = requests.request("POST", url, json=payload, headers=headers, timeout=20).json()
    response_detail = response_detail['data']['propertyInfo']
    total_price = re.findall(r'(.\d+) total', str(properties))[0]

    return (
        response_detail['summary']['name'],
        response_detail['summary']['location']['address']['addressLine'],
        properties['destinationInfo']['distanceFromDestination']['value'],
        properties['price']['lead']['formatted'],
        total_price,
        response_detail['propertyGallery']['images'],
        properties['id']
        )
