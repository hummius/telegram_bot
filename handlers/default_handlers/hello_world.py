from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['hello_world'])
def bot_hello_world(message: Message) -> None:
    """
    Стандартная функция выводящая информацию о телеграм-боте

    :param message: сообщение от пользователя
    """
    bot.reply_to(message, 'Приветствую! Меня зовут - Гриша, '
                          'и я - телеграм-бот турагенства Too Easy Travel.')