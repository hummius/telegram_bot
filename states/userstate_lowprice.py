from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """
    Класс с группой состояний пользователя для функции lowprice.
    """
    city_for_search = State()
    hotels_amount = State()
    need_photo = State()
    photos_amount = State()
    from_date = State()
    to_date = State()
    end_of_searching = State()
