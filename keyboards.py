from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_kb_download():
    kb_download = ReplyKeyboardBuilder()
    kb_download.add(KeyboardButton(text='Загрузить файл'))
    return kb_download.as_markup(resize_keyboard=True)
