import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from dotenv import load_dotenv
import os

from config import TOKEN

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('//')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except BaseException:
        print("Бот выключен")