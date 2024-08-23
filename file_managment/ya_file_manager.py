import os
import asyncio

import yadisk

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


TOKEN = os.getenv('YA_TOKEN')


class YaDiskClient:

    @classmethod
    async def token_valid(cls):
        async with yadisk.AsyncClient(token=TOKEN, session='aiohttp') as client:
            res = await client.check_token()
            return res

    @staticmethod
    def set_correct_path(path) -> str:
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
        """Выгрузка файла на диск"""
        async with yadisk.AsyncClient(token=TOKEN, session='aiohttp') as client:
            try:
                await client.upload(path_to_file, dst_path)
            except yadisk.exceptions.PathExistsError:
                print('Файл с таким именем уже существует или некорректно указан путь')




path_list = []  # Список из элементов которого будет сформирован корректный путь к директориям диска


# def token_valid():
#     return y.check_token()


# def upload_img(path_to_file: bytes, dst_path: str):
#     """Выгрузка файла на диск"""
#     try:
#         y.upload(path_to_file, dst_path)
#     except yadisk.exceptions.PathExistsError:
#         print('Файл с таким именем уже существует или некорректно указан путь')


# def get_directories_in(path) -> list:
#     """Формирование списка с именами директорий на диске"""
#     try:
#         folder_env = y.listdir(set_correct_path(path))
#
#         directories = []
#         for el in folder_env:
#             if el['type'] == 'dir':
#                 directories.append(el['name'])
#         return directories
#     except yadisk.exceptions.PathNotFoundError as ex:
#         return ex




if __name__ == "__main__":
    print(asyncio.run(YaDiskClient.get_directories(['Фото', 'Фотосессии', '23'])))
