from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import keyboards as kb

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, шеф {message.from_user.first_name}! Нажми на кнопку "Поиск рецепта"', 
                         reply_markup=kb.search_bt)

@router.message(F.text == 'Поиск рецепта')
async def input_recept(message: Message):
    await message.answer('Введи название рецепта')

