from database.history_base import *
from datetime import *
from typing import Any, List


def history_rec_func(user_name: str, command: str, data: Any, from_price: int = None,
                     to_price: int = None, from_distance: float = None, to_distance: float = None,
                     photos_amount: int = None, hotels_list: List = None) -> None:
    """
    Вспомогательная общая функция принимает данные и заносит их в базу данных.
    :param photos_amount: Количество запрошенных фотографий.
    :param hotels_list: Список найденных отелей.
    :param user_name: Имя пользователя.
    :param command: Тип команды запроса.
    :param data: Общие данные из состояний пользователя на момент запроса.
    :param from_price: Нижняя планка цены.
    :param to_price: Верхняя планка цены.
    :param from_distance: Минимальное расстояние от центра.
    :param to_distance: Максимальное расстояние от центра.
    """
    Request.create_table()
    Request.create(user_name=user_name,
                   command=command,
                   location=data['city'],
                   from_price=from_price,
                   to_price=to_price,
                   from_distance=from_distance,
                   to_distance=to_distance,
                   result_range=data['hotels_amount'],
                   photos=data['photos_need'],
                   photos_amount=photos_amount,
                   from_date=date(int(data['from_date'][2]),
                                  int(data['from_date'][1]),
                                  int(data['from_date'][0])),
                   to_date=date(int(data['to_date'][2]),
                                int(data['to_date'][1]),
                                int(data['to_date'][0])),
                   date_of_request=datetime.now(),
                   hotels_found=hotels_list
                   )
