import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

import keyboards as kb

from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет шеф! Нажми на кнопку "Поиск рецепта"', reply_markup=kb.start_bt)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except BaseException:
        print("Бот выключен")