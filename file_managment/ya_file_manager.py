import os
import asyncio

import yadisk

from utils.utils import set_correct_path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


TOKEN = os.getenv('YA_TOKEN')


class YaDiskClient:
    TOKEN = os.getenv('YA_TOKEN')
    client = yadisk.AsyncClient(token=TOKEN, session='aiohttp')

    async def token_valid(self):
        await self.client.check_token()
        await self.client.close()


path_list = []  # Список из элементов которого будет сформирован корректный путь к директориям диска


def token_valid():
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


async def main():
    async with yadisk.AsyncClient(token=os.getenv('YA_TOKEN'), session='aiohttp') as client:
        # print(await client.check_token())
        # print(await client.get_disk_info())
        print(await client.listdir(''))


if __name__ == "__main__":
    asyncio.run(main())
