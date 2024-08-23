import os
import httpx

import yadisk

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


TOKEN = os.getenv('YA_TOKEN')

path_list = []  # Список из элементов которого будет сформирован корректный путь к директориям диска


class YaDisk:

    @staticmethod
    def set_correct_path(path) -> str:
        """Функция составляет корректную запись пути к запрашиваемой директории"""
        return '/'.join(path) + '/'

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
    async def upload_img(cls, path_to_file: bytes, dst_path: str):
        """Функция осуществляет выгрузку файлов на облако"""
        async with yadisk.AsyncClient(token=TOKEN, session='aiohttp') as client:
            try:
                await client.upload(path_to_file, dst_path)
            except yadisk.exceptions.PathExistsError:
                print('Файл с таким именем уже существует или некорректно указан путь')


if __name__ == "__main__":
    pass