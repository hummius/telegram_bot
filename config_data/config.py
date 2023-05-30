import os
from dotenv import find_dotenv, load_dotenv


if not find_dotenv():
    exit('Переменные окружения не загружены, т.к. отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', 'запустить бота'),
    ('help', 'помощь по командам бота'),
    ('hello_world', 'информация о боте'),
    ('lowprice', 'вывод самых дешевых отелей в городе'),
    ('highprice', 'вывод самых дорогих отелей в городе'),
    ('bestdeal', 'вывод отелей, наиболее подходящих по цене и расположению от центра'),
    ('history', 'вывод истории запросов')
)