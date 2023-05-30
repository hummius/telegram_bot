from loader import bot
from telebot.types import Message


@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message) -> None:
    """
    Пользовательская функция выводящая ответ
    на текстовое сообщение "Привет"

    :param message: сообщение от пользователя
    """
    if message.text.lower() == 'привет' or message.text.lower() == 'hello':
        bot.reply_to(message, f'Привет, {message.from_user.full_name}! Чем могу помочь?')
