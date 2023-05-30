from keyboards.reply import agreement_request
from loader import bot
from telebot.types import Message


PHOTOS_LIMIT_CONSTANT = 6
HOTEL_WITHDRAWAL_LIMIT_CONSTANT = 10


def set_city_name(message: Message, next_state) -> None:
    """
    Функция принимает от пользователя город для поиска, и запускает
    следующую функцию запроса.
    :param next_state: Назначение следующей переменной.
    :param message:
    """
    if not ''.join(message.text.split()).isalpha():
        bot.send_message(message.from_user.id, 'Ошибка: Название города должно содержать только текст.')

    else:
        bot.set_state(message.from_user.id, next_state, message.chat.id)
        bot.send_message(message.from_user.id, 'Какое количество результатов вывести?')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text


def set_hotels_amount(message: Message, next_state) -> None:
    """
    Функция принимает от пользователя количество отелей для вывода, и запускает
    следующую функцию запроса.
    :param next_state: Следующее состояние пользователя.
    :param message:
    """
    if message.text.isdigit():
        bot.set_state(message.from_user.id, next_state, message.chat.id)
        bot.send_message(message.from_user.id, 'Желаете информацию с фотографиями? (Да/Нет)',
                         reply_markup=agreement_request.keyboard)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_amount'] = min(int(message.text), HOTEL_WITHDRAWAL_LIMIT_CONSTANT)
    else:
        bot.send_message(message.from_user.id, 'Количество должно содержать числа.')


def set_need_photo(message: Message, next_state, alt_next_state) -> None:
    """
    Функция принимает ответ на запрос о необходимости вывода фотографий отелей.
    В случае положительного ответа запускает запрос на количество фотографий на отель.
    Иначе переходит сразу на следующий запрос.
    :param alt_next_state: Следующее состояние, в случае отрицательного ответа пользователя.
    :param next_state: Следующее состояние пользователя.
    :param message:
    """
    if message.text.lower() == 'да':
        bot.set_state(message.from_user.id, next_state, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите количество фотографий для вывода.',
                         reply_markup=agreement_request.ReplyKeyboardRemove())
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photos_need'] = True
    elif message.text.lower() == 'нет':
        bot.set_state(message.from_user.id, alt_next_state, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите дату въезда (в формате 1.1.2023)',
                         reply_markup=agreement_request.ReplyKeyboardRemove())
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photos_need'] = False
    else:
        bot.send_message(message.from_user.id, 'Введите ответ в формате - да/нет.')


def set_photos_amount(message: Message, next_state) -> None:
    """
    Функция принимает ответ на запрос о количестве фотографий для вывода,
    и запускает следующий запрос.
    :param next_state: Следующее состояние пользователя.
    :param message:
    """
    if message.text.isdigit():
        bot.set_state(message.from_user.id, next_state, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите дату въезда (в формате 1.1.2023)')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photos_amount'] = min(int(message.text), PHOTOS_LIMIT_CONSTANT)
    else:
        bot.send_message(message.from_user.id, 'Количество должно содержать только числа.')


def set_from_date(message: Message, next_state) -> None:
    """
    Функция принимающая ответ на запрос о дате въезда в отель,
    и запускающая следующий запрос.
    :param next_state: Следующее состояние пользователя.
    :param message:
    """
    if ''.join(message.text.split('.')).isdigit():
        bot.set_state(message.from_user.id, next_state, message.chat.id)
        bot.send_message(message.from_user.id, 'Введите дату выезда (в формате 1.1.2023)')
        with bot.retrieve_data(message.from_user.id, message.chat.id, ) as data:
            data['from_date'] = message.text.split('.')
    else:
        bot.send_message(message.from_user.id, 'Ошибка: в дате должны быть только цифры.')
