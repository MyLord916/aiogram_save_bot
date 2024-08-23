import os
import httpx
from datetime import datetime

import yadisk

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


TOKEN = os.getenv('YA_TOKEN')

path_list = []  # Список из элементов которого будет сформирован корректный путь к директориям диска

subsequence = 1  # Последнее значение в нейминге файлов для уникальности имени


class YaDisk:

    @staticmethod
    def set_correct_path(path) -> str:
        """Функция составляет корректную запись пути к запрашиваемой директории"""
        return '/'.join(path) + '/'

    @staticmethod
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
