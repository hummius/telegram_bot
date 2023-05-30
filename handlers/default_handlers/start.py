from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Стандартная функция начала работы телеграм-бота (в разработке)

    :param message: сообщение от пользователя
    """
    bot.reply_to(message, f'Привет, {message.from_user.full_name}!')
