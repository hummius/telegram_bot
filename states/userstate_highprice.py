from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """
    Класс с группой состояний пользователя для функции highprice.
    """
    city_for_hp = State()
    hotels_amount_hp = State()
    need_photo_hp = State()
    photos_amount_hp = State()
    from_date_hp = State()
    to_date_hp = State()
    end_of_searching_hp = State()