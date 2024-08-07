from aiogram import Bot, Dispatcher

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TELE_TOKEN'))  # Объявление объекта бота и диспетчера
dp = Dispatcher()
