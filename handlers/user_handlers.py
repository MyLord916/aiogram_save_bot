import io

from aiogram import F, types, Router
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from create_bot import bot
from file_managment.ya_file_manager import YaDisk, path_list
from keyboards.user_keyboards import get_gir_keyboard
from utils.utils import move_to_folders_on_disk, FolderFilter


router = Router()


@router.message(Command('start'))
async def start_message(message: types.message):
    path_list.clear()
    await message.answer(
        text='''
Бот перемещает выбранные изображения из галереи устройства
или чата (группы) телеграм в папку вашего облачного хранилища.
        
Выберите путь к нужной папке, отправьте боту файлы - он сохранит их в облачном хранилище.
После этого изображения будут удалены из этого чата. 
        
Ниже будет отображаться путь к выбранной папке в облаке.
👇
''')
    await message.answer('Выберите папку:', reply_markup=await get_gir_keyboard())


@router.message(F.text, FolderFilter())
async def move_to_dir(message: types.Message, bot: bot):
    """Смена клавиатуры при переходе по директориям"""
    await message.answer('Идет запрос к директориям диска...')
    move_to_folders_on_disk(message.text)
    await message.answer(YaDisk.set_correct_path(path_list) if len(path_list) else 'Корневая директория/',
                         reply_markup=await get_gir_keyboard())
    mes_id_list = [message.message_id + 1, message.message_id, message.message_id - 1]
    try:
        for i in mes_id_list:
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        if ex.message == 'Bad Request: message to delete not found':
            print('Список id пуст')


@router.message(F.photo)  # Хендлер на присланные фотографии
async def download_photo(message: types.Message, bot: bot):
    buffer = io.BytesIO()  # Объект буфера
    await bot.send_chat_action(message.from_user.id, 'upload_photo', message_thread_id=message.message_id)
    await bot.download(message.photo[-1], destination=buffer)

    await YaDisk.upload_img(io.BytesIO(buffer.read()))
    await bot.delete_message(message.from_user.id, message.message_id)


@router.message(Command('clear'))
async def cmd_clear(message: types.Message, bot: bot):
    try:
        for i in range(message.message_id, 0, -1):
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        if ex.message == 'Bad Request: message to delete not found':
            print('Все сообщения удалены')
