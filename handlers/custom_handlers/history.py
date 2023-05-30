import peewee

from loader import bot
from telebot.types import Message
from database.history_base import *


@bot.message_handler(commands=['history'])
def get_history(message: Message) -> None:
    """
    Функция подхватывает команду history и выводит историю запросов из базы данных.
    :param message:
    """
    try:
        for request in Request.select().where(Request.user_name == message.from_user.full_name):
            lines_list = [f"Команда: {request.command}",
                          f"Запрашиваемая локация: {request.location}",
                          f"Количество результатов: {request.result_range}",
                          f"Даты запроса: от {request.from_date} до {request.to_date}",
                          f"Время создания запроса: {request.date_of_request}",
                          f"Найденные отели: {request.hotels_found}"
                          ]
            if request.command == '/bestdeal':
                lines_list.insert(2, f"Диапазон дистанции от центра: {request.from_distance} - "
                                     f"{request.to_distance} миль")
                lines_list.insert(2, f"Диапазон цен: {request.from_price} - {request.to_price}")
                if request.photos == 1:
                    lines_list.insert(5, f"Количество фото: {request.photos_amount}")
            else:
                if request.photos == 1:
                    lines_list.insert(4, f"Количество фото: {request.photos_amount}")

            bot.send_message(message.from_user.id, '\n'.join(lines_list))

    except peewee.OperationalError:
        bot.send_message(message.from_user.id, 'Нет записи в базе данных')
