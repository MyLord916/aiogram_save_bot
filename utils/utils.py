from aiogram.filters import BaseFilter
from aiogram import types

from keyboards.user_keyboards import system_buttons
from file_managment.ya_file_manager import path_list, YaDisk


def move_to_folders_on_disk(folder) -> None:
    '''Функция осуществляет смену директорий путем добавления или удаления выбранной папки в список,
     из которого будет сформирован корректный путь'''
    if len(path_list) != 0 and folder in system_buttons.values():
        if folder == system_buttons['back']:
            path_list.pop(-1)
        elif folder == system_buttons['home']:
            path_list.clear()
    if folder not in ['', *system_buttons.values()]:
        path_list.append(folder)


class FolderFilter(BaseFilter):
    """Хендлер кнопок для предстоящего перехода по директориям"""
    async def __call__(self, message: types.Message) -> bool:
        result_handler_list = await YaDisk.get_directories_in(path_list) + list(system_buttons.values())
        if message.text in result_handler_list:
            return True
        else:
            return False
