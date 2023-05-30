from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_yes = KeyboardButton('ДА')
button_no = KeyboardButton('НЕТ')

keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(button_yes, button_no)
