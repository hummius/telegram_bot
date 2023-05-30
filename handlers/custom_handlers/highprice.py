from states.userstate_highprice import UserInfoState
from loader import bot
from telebot.types import Message
import requests
from utils import API_list, API_id, API_details, general_functions
from database import history_record


@bot.message_handler(commands=['highprice'])
def highprice_search(message: Message) -> None:
    """
    Функция подхватывает команду highprice и запускает дальнейший процесс.
    :param message:
    """
    bot.set_state(message.from_user.id, UserInfoState.city_for_hp, message.chat.id)
    bot.reply_to(message, 'Введите город поиска')


@bot.message_handler(state=UserInfoState.city_for_hp)
def highprice_hotels(message: Message) -> None:
    """
    Функция перехватывает сообщение и передает в основную функцию из utils.
    :param message:
    """
    general_functions.set_city_name(message, UserInfoState.hotels_amount_hp)


@bot.message_handler(state=UserInfoState.hotels_amount_hp)
def set_hotels_amount(message: Message) -> None:
    """
    Функция перехватывает сообщение и передает в основную функцию из utils.
    :param message:
    """
    general_functions.set_hotels_amount(message, UserInfoState.need_photo_hp)


@bot.message_handler(state=UserInfoState.need_photo_hp)
def set_need_photo(message: Message) -> None:
    """
    Функция перехватывает сообщение и передает в основную функцию из utils.
    :param message:
    """
    general_functions.set_need_photo(message, UserInfoState.photos_amount_hp,
                                     UserInfoState.from_date_hp)


@bot.message_handler(state=UserInfoState.photos_amount_hp)
def set_photos_amount(message: Message) -> None:
    """
    Функция перехватывает сообщение и передает в основную функцию из utils.
    :param message:
    """
    general_functions.set_photos_amount(message, UserInfoState.from_date_hp)


@bot.message_handler(state=UserInfoState.from_date_hp)
def set_from_date(message: Message) -> None:
    """
    Функция перехватывает сообщение и передает в основную функцию из utils.
    :param message:
    """
    general_functions.set_from_date(message, UserInfoState.to_date_hp)


@bot.message_handler(state=UserInfoState.to_date_hp)
def set_to_date_hp(message: Message) -> None:
    """
    Функция принимает ответ на запрос о дате последнего дня прибывания в отеле,
    и запускает функции работающие с API запросами для получения данных.
    В итоге функция, выводит сообщением бота запрошенную информацию пользователю в чат.
    :param message:
    """
    hp_found_list = list()

    if ''.join(message.text.split('.')).isdigit():
        bot.send_message(message.from_user.id, 'Идет поиск отелей...')
        with bot.retrieve_data(message.from_user.id, message.chat.id, ) as data:
            data['to_date'] = message.text.split('.')

        try:
            hotels_list = API_list.get_hotels_list(API_id.get_location_id(data['city']),
                                                   data['from_date'], data['to_date'],
                                                   {'availableFilter': 'SHOW_AVAILABLE_ONLY'},
                                                   hotels_amount=data['hotels_amount'],
                                                   sort="PRICE_HIGH_TO_LOW")
            for key in hotels_list:
                name, address, destination, price, \
                    total_price, photos_list, hotel_id = API_details.get_hotel_details(key)
                hp_found_list.append(name)
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
                history_record.history_rec_func(message.from_user.full_name, '/highprice',
                                                data, hotels_list=hp_found_list,
                                                photos_amount=data['photos_amount'])
            else:
                history_record.history_rec_func(message.from_user.full_name, '/highprice',
                                                data, hotels_list=hp_found_list)

        except requests.exceptions.ReadTimeout:
            bot.send_message(message.from_user.id, 'Ошибка: лимит времени ожидания запроса был исчерпан')
            bot.set_state(message.from_user.id, UserInfoState.end_of_searching_hp)
        except TypeError:
            bot.send_message(message.from_user.id, 'К сожалению, ничего не найдено...')
            bot.set_state(message.from_user.id, UserInfoState.end_of_searching_hp)
        except (KeyError, IndexError):
            bot.send_message(message.from_user.id, 'Что-то пошло не так...')
            bot.set_state(message.from_user.id, UserInfoState.end_of_searching_hp)
    else:
        bot.send_message(message.from_user.id, 'Ошибка: в дате должны быть только цифры.')

    bot.send_message(message.from_user.id, 'Вывод результата завершен.')
    bot.set_state(message.from_user.id, UserInfoState.end_of_searching_hp)
