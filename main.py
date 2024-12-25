import asyncio
from aiogram import Bot, Dispatcher

from keys.config import TOKEN_BOT
from handlers import router

bot = Bot(TOKEN_BOT)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except BaseException:
        print("Бот выключен")