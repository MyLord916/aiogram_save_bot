import os
import httpx
from datetime import datetime

import yadisk

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


TOKEN = os.getenv('YA_TOKEN')

path_list = []  # Список из элементов которого будет сформирован корректный путь к директориям диска


def infinite_current_gen():
    current = 0
    while True:
        if current > 99:
            current = 0
        yield current
        current += 1


infinite_current = infinite_current_gen()


class YaDisk:

    @staticmethod
    def set_correct_path(path) -> str:
        """Функция составляет корректную запись пути к запрашиваемой директории"""
        return '/'.join(path) + '/'

    @staticmethod
    def get_dt_name() -> str:
        """Функция задает имя файла в формате времени год/месяц/день/минуты/(последовательный номер уникальности)"""
        dt = datetime.now()
        dt_name = dt.strftime('%Y%m%d%H%M') + f'({str(next(infinite_current))})' + '.jpg'
        return dt_name

    @classmethod
    async def get_directories_in(cls, path) -> list:
        """Формирование списка с именами директорий на диске"""
        async with yadisk.AsyncClient(token=TOKEN, session='aiohttp') as client:
            folder_env = [list_dir async for list_dir in client.listdir(cls.set_correct_path(path))]
            try:
                directories = []
                for el in folder_env:
                    if el['type'] == 'dir':
                        directories.append(el['name'])
                return directories
            except yadisk.exceptions.PathNotFoundError as ex:
                return ex

    @classmethod
    async def upload_img(cls, path_to_file: bytes):
        """Функция осуществляет выгрузку файлов на облако"""
        async with yadisk.AsyncClient(token=TOKEN, session='aiohttp') as client:
            try:
                await client.upload(path_to_file, cls.set_correct_path(path_list) + cls.get_dt_name())
            except yadisk.exceptions.PathExistsError:
                print('Файл с таким именем уже существует или некорректно указан путь')
