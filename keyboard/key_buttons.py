from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_keyboard = ReplyKeyboardBuilder()
start_keyboard.add(KeyboardButton(text='Надіслати локацію', request_location=True))


authenticate_keyboard = ReplyKeyboardBuilder()
authenticate_keyboard.add(
    KeyboardButton(text='Прогноз на сьогодні'),
    KeyboardButton(text='Прогноз на завтра'),
    KeyboardButton(text='Прогноз на 5 днів'),
)
authenticate_keyboard.adjust(2, 1)


change_location_keyboard = ReplyKeyboardBuilder()
change_location_keyboard.add(
    KeyboardButton(text='Отримати прогноз'),
    KeyboardButton(text='Змінити локацію'),
)
change_location_keyboard.adjust(1, 2)


delete_keyboard = ReplyKeyboardRemove()
