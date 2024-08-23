from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from file_managment.ya_file_manager import path_list
from file_managment.ya_file_manager import YaDiskClient


system_buttons = {  # Кнопки возврата в предыдущую директорию или в корневую
    'home': '🏠',
    'back': '🔙'
    }


async def get_gir_keyboard():
    """Компоновка клавиатуры из видимых директорий"""
    builder = ReplyKeyboardBuilder()
    if len(path_list):
        [builder.add(KeyboardButton(text=el)) for el in system_buttons.values()]
    [builder.add(KeyboardButton(text=el)) for el in await YaDiskClient.get_directories_in(path_list)]
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
