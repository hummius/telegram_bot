from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """
    Класс с группой состояний пользователя для функции bestdeal.
    """
    city_for_bd = State()
    from_price_bd = State()
    to_price_bd = State()
    from_distance_bd = State()
    to_distance_bd = State()
    distance_filter = State()
    hotels_amount_bd = State()
    need_photo_bd = State()
    photos_amount_bd = State()
    from_date_bd = State()
    to_date_bd = State()
    end_of_searching_bd = State()
