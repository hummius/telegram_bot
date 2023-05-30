from states.userstate_lowprice import UserInfoState
from loader import bot
from telebot.types import Message
import requests
from utils import API_list, API_id, API_details, general_functions
from database import history_record


@bot.message_handler(commands=['lowprice'])
def low_price_search(message: Message) -> None:
    """
    Функция подхватывает команду lowprice и запускает дальнейший процесс.
    :param message:
    """
    bot.set_state(message.from_user.id, UserInfoState.city_for_search, message.chat.id)
    bot.reply_to(message, 'Введите город поиска')


@bot.message_handler(state=UserInfoState.city_for_search)
def low_price_hotels(message: Message) -> None:
    """
    Функция принимает от пользователя город для поиска, и запускает
    следующую функцию запроса.
    :param message:
    """
    general_functions.set_city_name(message, UserInfoState.hotels_amount)


@bot.message_handler(state=UserInfoState.hotels_amount)
def set_hotels_amount(message: Message) -> None:
    """
    Функция принимает от пользователя количество отелей для вывода, и запускает
    следующую функцию запроса.
    :param message:
    """
    general_functions.set_hotels_amount(message, UserInfoState.need_photo)


@bot.message_handler(state=UserInfoState.need_photo)
def set_need_photo(message: Message) -> None:
    """
    Функция принимает ответ на запрос о необходимости вывода фотографий отелей.
    В случае положительного ответа запускает запрос на количество фотографий на отель.
    Иначе переходит сразу на следующий запрос.
    :param message:
    """
    general_functions.set_need_photo(message, UserInfoState.photos_amount, UserInfoState.from_date)


@bot.message_handler(state=UserInfoState.photos_amount)
def set_photos_amount(message: Message) -> None:
    """
    Функция принимает ответ на запрос о количестве фотографий для вывода,
    и запускает следующий запрос.
    :param message:
    """
    general_functions.set_photos_amount(message, UserInfoState.from_date)


@bot.message_handler(state=UserInfoState.from_date)
def set_from_date(message: Message) -> None:
    """
    Функция принимающая ответ на запрос о дате въезда в отель,
    и запускающая следующий запрос.
    :param message:
    """
    general_functions.set_from_date(message, UserInfoState.to_date)


@bot.message_handler(state=UserInfoState.to_date)
def set_to_date(message: Message) -> None:
    """
    Функция принимает ответ на запрос о дате последнего дня прибывания в отеле,
    и запускает функции работающие с API запросами для получения данных.
    В итоге функция, выводит сообщением бота запрошенную информацию пользователю в чат.
    :param message:
    """
    lp_found_list = list()
    if ''.join(message.text.split('.')).isdigit():
        bot.send_message(message.from_user.id, 'Идет поиск отелей...')
        with bot.retrieve_data(message.from_user.id, message.chat.id, ) as data:
            data['to_date'] = message.text.split('.')

        try:
            hotels_list = API_list.get_hotels_list(API_id.get_location_id(data['city']),
                                                   data['from_date'], data['to_date'],
                                                   {'availableFilter': 'SHOW_AVAILABLE_ONLY'},
                                                   hotels_amount=data['hotels_amount'],
                                                   sort="PRICE_LOW_TO_HIGH")

            for key in hotels_list:
                name, address, destination, price, \
                    total_price, photos_list, hotel_id = API_details.get_hotel_details(key)
                lp_found_list.append(name)
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
                bot.send_message(message.from_user.id, f'https://www.hotels.com/h{hotel_id}.Hotel-Information')
                bot.send_message(message.from_user.id, '*' * 33)

            if data['photos_need']:
                history_record.history_rec_func(message.from_user.full_name, '/lowprice',
                                                data, hotels_list=lp_found_list,
                                                photos_amount=data['photos_amount'])
                bot.send_message(message.from_user.id, 'Сделал запись с фото')
            else:
                history_record.history_rec_func(message.from_user.full_name, '/lowprice',
                                                data, hotels_list=lp_found_list)
                bot.send_message(message.from_user.id, 'Сделал запись без фото')

        except requests.exceptions.ReadTimeout:
            bot.send_message(message.from_user.id, 'Ошибка: лимит времени ожидания запроса был исчерпан')
            bot.set_state(message.from_user.id, UserInfoState.end_of_searching)
        except TypeError:
            bot.send_message(message.from_user.id, 'К сожалению, ничего не найдено...')
            bot.set_state(message.from_user.id, UserInfoState.end_of_searching)
        except (KeyError, IndexError):
            bot.send_message(message.from_user.id, 'Что-то пошло не так... Ошибка ключа')
            bot.set_state(message.from_user.id, UserInfoState.end_of_searching)
    else:
        bot.send_message(message.from_user.id, 'Ошибка: в дате должны быть только цифры.')

    bot.send_message(message.from_user.id, 'Вывод результата завершен.')
    bot.set_state(message.from_user.id, UserInfoState.end_of_searching)
