import asyncio
import logging

from create_bot import dp, bot
from handlers.user_handlers import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
