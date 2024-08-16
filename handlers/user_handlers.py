import io

from aiogram import F, types, Router
from aiogram.filters import Command, BaseFilter
from aiogram.exceptions import TelegramBadRequest

from create_bot import bot
from file_managment.ya_file_manager import upload_img, get_directories_in
from file_managment.file_moving_manager import get_dt_name, move_to_folders_on_disk, path_list, set_correct_path
from keyboards.user_keyboards import get_gir_keyboard, system_buttons


router = Router()


def buttons() -> list:
    """Список кнопок на которые должен реагировать хендлер смены директории"""
    but = [*system_buttons.values(), *get_directories_in(path_list)]
    return but


@router.message(Command('start'))
async def start_message(message: types.message):
    path_list.clear()
    await message.answer(
        text='Бот для сохранения пересылаемых изображений в облако. Как в папке выбираешь директорию в которую желаешь поместить файл и отправляешь репост или фото')
    await message.answer('Выбери директорию:',
                         reply_markup=get_gir_keyboard(buttons(), path_list).as_markup(resize_keyboard=True)
                         )


class FolderFilter(BaseFilter):
    """Хендлер кнопок для предстоящего перехода по директориям"""

    async def __call__(self, message: types.Message) -> bool:
        if message.text in buttons():
            return True
        else:
            return False


# TOODO: Хендлер не видит новые значения попадаемые в обрабатываемый список
@router.message(F.text, FolderFilter())
async def move_to_dir(message: types.Message, bot: bot):
    """Смена клавиатуры при переходе по директориям"""
    await message.answer('Идет запрос к директориям диска...')
    move_to_folders_on_disk(message.text)
    await message.answer(set_correct_path(path_list) if len(path_list) else 'Корневая директория/',
                         reply_markup=get_gir_keyboard(buttons(), path_list).as_markup(resize_keyboard=True))
    mes_id = [message.message_id + 1, message.message_id, message.message_id - 1]
    try:
        for i in mes_id:
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        if ex.message == 'Bad Request: message to delete not found':
            print('Список id пуст')


@router.message(F.photo)  # Хендлер на присланные фотографии
async def download_photo(message: types.Message, bot: bot):
    file_name = get_dt_name()
    buffer = io.BytesIO()  # Объект буфера
    await bot.send_chat_action(message.from_user.id, 'upload_photo', message_thread_id=message.message_id)
    await bot.download(message.photo[-1], destination=buffer)

    upload_img(io.BytesIO(buffer.read()), set_correct_path(path_list) + file_name)
    print(f'file processing: {file_name}')  # Проверочка между делом
    await bot.delete_message(message.from_user.id, message.message_id)


@router.message(Command('clear'))
async def cmd_clear(message: types.Message, bot: bot):
    try:
        for i in range(message.message_id, 0, -1):
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        if ex.message == 'Bad Request: message to delete not found':
            print('Все сообщения удалены')
