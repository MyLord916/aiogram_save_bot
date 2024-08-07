from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


system_buttons = {  # Кнопки возврата в предыдущую директорию или в корневую
    'home': '🏠',
    'back': '🔙'
    }


def get_gir_keyboard(buttons, path_list):
    """Компоновка клавиатуры из видимых директорий"""
    builder = ReplyKeyboardBuilder()
    if len(path_list):
        [builder.add(KeyboardButton(text=el)) for el in buttons]
    else:
        [builder.add(KeyboardButton(text=el)) for el in buttons[2:]]
    builder.adjust(2)
    return builder
