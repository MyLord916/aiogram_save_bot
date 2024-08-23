from datetime import datetime

from keyboards.user_keyboards import system_buttons
from file_managment.ya_file_manager import path_list

subsequence = 1  # Последнее значение в нейминге файлов для уникальности имени


def get_dt_name() -> str:
    """Функция задает имя файла в формате времени год/месяц/день/минуты/(последовательный номер уникальности)"""
    global subsequence
    dt = datetime.now()
    dt_name = dt.strftime('%Y%m%d%H%M') + f'({str(subsequence)})' + '.jpg'
    if subsequence < 99:
        subsequence += 1
    else:
        subsequence = 1
    return dt_name


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

