from states.userstate_bestdeal import UserInfoState
from loader import bot
from telebot.types import Message
import requests
from utils import API_list, API_id, API_details, general_functions
from database import history_record


@bot.message_handler(commands=['bestdeal'])
def bestdeal_search(message: Message) -> None:
    """
    Функция подхватывает команду bestdeal и запускает дальнейший процесс.
    :param message:
    """
    bot.set_state(message.from_user.id, UserInfoState.city_for_bd, message.chat.id)
    bot.reply_to(message, 'Введите город поиска')


@bot.message_handler(state=UserInfoState.city_for_bd)
def bestdeal_hotels(message: Message) -> None:
    """
    Функция принимает от пользователя город для поиска, и запускает
    следующую функцию запроса.
    :param message:
    """
    if not ''.join(message.text.split()).isalpha():
        bot.send_message(message.from_user.id, 'Ошибка: Название города должно содержать только текст.')

    else:
        bot.set_state(message.from_user.id, UserInfoState.from_price_bd, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите нижнюю планку цены:')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text


@bot.message_handler(state=UserInfoState.from_price_bd)
def from_price(message: Message) -> None:
    """
    Функция принимает от пользователя нижнюю планку цены для фильтра поиска,
    и запускает следующую функцию.
    :param message:
    """
    if message.text.isdigit():
        bot.set_state(message.from_user.id, UserInfoState.to_price_bd, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите верхнюю планку цены')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['from_price'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Цена должна содержать только числа.')


@bot.message_handler(state=UserInfoState.to_price_bd)
def to_price(message: Message) -> None:
    """
    Функция принимает от пользователя верхнюю планку цены для фильтра поиска,
    и запускает следующую функцию.
    :param message:
    """
    if message.text.isdigit():
        bot.set_state(message.from_user.id, UserInfoState.from_distance_bd, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите минимальное расстояние '
                                               'местонахождения отеля, от центра (в милях)')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['to_price'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Цена должна содержать только числа.')


@bot.message_handler(state=UserInfoState.from_distance_bd)
def from_distance(message: Message) -> None:
    """
    Функция принимает от пользователя минимальную дистанцию отеля от центра для фильтра поиска,
    и запускает следующую функцию.
    :param message:
    """
    if message.text.isdigit():
        bot.set_state(message.from_user.id, UserInfoState.to_distance_bd, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите максимальное расстояние '
                                               'местонахождения отеля, от центра (в милях)')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['from_distance'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Расстояние должно содержать только числа.')


@bot.message_handler(state=UserInfoState.to_distance_bd)
def to_distance(message: Message) -> None:
    """
    Функция принимает от пользователя минимальную дистанцию отеля от центра для фильтра поиска,
    и запускает следующую функцию.
    :param message:
    """
    if message.text.isdigit():
        bot.set_state(message.from_user.id, UserInfoState.hotels_amount_bd, message.chat.id)
        bot.send_message(message.from_user.id, 'Какое количество результатов вывести?')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['to_distance'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Расстояние должно содержать только числа.')


@bot.message_handler(state=UserInfoState.hotels_amount_bd)
def set_hotels_amount(message: Message) -> None:
    """
    Функция перехватывает сообщение и передает в основную функцию из utils.
    :param message:
    """
    general_functions.set_hotels_amount(message, UserInfoState.need_photo_bd)


@bot.message_handler(state=UserInfoState.need_photo_bd)
def set_need_photo(message: Message) -> None:
    """
    Функция перехватывает сообщение и передает в основную функцию из utils.
    :param message:
    """
    general_functions.set_need_photo(message, UserInfoState.photos_amount_bd,
                                     UserInfoState.from_date_bd)


@bot.message_handler(state=UserInfoState.photos_amount_bd)
def set_photos_amount(message: Message) -> None:
    """
    Функция перехватывает сообщение и передает в основную функцию из utils.
    :param message:
    """
    general_functions.set_photos_amount(message, UserInfoState.from_date_bd)


@bot.message_handler(state=UserInfoState.from_date_bd)
def set_from_date(message: Message) -> None:
    """
    Функция перехватывает сообщение и передает в основную функцию из utils.
    :param message:
    """
    general_functions.set_from_date(message, UserInfoState.to_date_bd)


@bot.message_handler(state=UserInfoState.to_date_bd)
def set_to_date_bd(message: Message) -> None:
    """
    Функция принимает ответ на запрос о дате последнего дня прибывания в отеле,
    и запускает функции работающие с API запросами для получения данных.
    В итоге функция, выводит сообщением бота запрошенную информацию пользователю в чат.
    :param message:
    """
    bd_found_list = list()

    if ''.join(message.text.split('.')).isdigit():
        bot.send_message(message.from_user.id, 'Идет поиск отелей...')
        with bot.retrieve_data(message.from_user.id, message.chat.id, ) as data:
            data['to_date'] = message.text.split('.')

        try:
            hotels_list = API_list.get_hotels_list(API_id.get_location_id(data['city']),
                                                   data['from_date'], data['to_date'],
                                                   {'availableFilter': 'SHOW_AVAILABLE_ONLY',
                                                    'price': {'max': data['to_price'], 'min': data['from_price']}},
                                                   sort="PRICE_LOW_TO_HIGH",
                                                   )
            counter = data['hotels_amount']
            for key in hotels_list:
                if counter <= 0:
                    break
                else:
                    distance = key['destinationInfo']['distanceFromDestination']['value']
                    if data['from_distance'] <= distance <= data['to_distance']:
                        name, address, destination, price, \
                            total_price, photos_list, hotel_id = API_details.get_hotel_details(key)
                        bd_found_list.append(name)
                        counter -= 1
                        bot.send_message(message.from_user.id,
                                         f"\n\n** {name} ** \n\n"
                                         f"Адрес -- {address}\n"
                                         f"От центра -- {destination} миль\n"
                                         f"Цена за ночь -- {price}\n"
                                         f"Сумма за весь срок -- {total_price}"
                                         )

                        if data['photos_need']:
                            count = data['photos_amount']
                            for photo in photos_list:
                                if count <= 0:
                                    break
                                else:
                                    count -= 1
                                    bot.send_photo(message.from_user.id, photo['image']['url'])

                        bot.send_message(message.from_user.id,
                                         f'https://www.hotels.com/h{hotel_id}.Hotel-Information')
                        bot.send_message(message.from_user.id, '*' * 33)

            if data['photos_need']:
                history_record.history_rec_func(message.from_user.full_name, '/bestdeal', data,
                                                data['from_price'], data['to_price'],
                                                data['from_distance'], data['to_distance'],
                                                photos_amount=data['photos_amount'],
                                                hotels_list=bd_found_list
                                                )
            else:
                history_record.history_rec_func(message.from_user.full_name, '/bestdeal', data,
                                                data['from_price'], data['to_price'],
                                                data['from_distance'], data['to_distance'],
                                                hotels_list=bd_found_list
                                                )
        except requests.exceptions.ReadTimeout:
            bot.send_message(message.from_user.id, 'Ошибка: лимит времени ожидания запроса был исчерпан')
            bot.set_state(message.from_user.id, UserInfoState.end_of_searching_bd)
        except TypeError:
            bot.send_message(message.from_user.id, 'К сожалению, ничего не найдено...')
            bot.set_state(message.from_user.id, UserInfoState.end_of_searching_bd)
        except (KeyError, IndexError):
            bot.send_message(message.from_user.id, 'Что-то пошло не так...')
            bot.set_state(message.from_user.id, UserInfoState.end_of_searching_bd)
    else:
        bot.send_message(message.from_user.id, 'Ошибка: в дате должны быть только цифры.')

    bot.send_message(message.from_user.id, 'Вывод результата завершен.')
    bot.set_state(message.from_user.id, UserInfoState.end_of_searching_bd)
