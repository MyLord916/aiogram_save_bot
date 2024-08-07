import yadisk

from file_managment.fail_moving_manager import set_correct_path

import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
y = yadisk.YaDisk(token=os.getenv('YA_TOKEN'))


def token_valid() -> bool:
    return y.check_token()


def upload_img(path_to_file: bytes, dst_path: str):
    """Выгрузка файла на диск"""
    try:
        y.upload(path_to_file, dst_path)
    except yadisk.exceptions.PathExistsError:
        print('Файл с таким именем уже существует или некорректно указан путь')


def get_directories_in(path) -> list:
    """Формирование списка с именами директорий на диске"""
    try:
        folder_env = y.listdir(set_correct_path(path))

        directories = []
        for el in folder_env:
            if el['type'] == 'dir':
                directories.append(el['name'])
        return directories
    except yadisk.exceptions.PathNotFoundError as ex:
        return ex