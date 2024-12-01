from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import requests

from config import API

import keyboards as kb

# from xxx import recipe_info

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, шеф {message.from_user.first_name}! Нажми на кнопку "Поиск рецепта"', 
                         reply_markup=kb.search_bt)

@router.message(F.text == 'Поиск рецепта')
async def input_recept(message: Message):
    await message.answer('Введи название рецепта')

@router.message()
async def search_recept(message: Message):
    recipe_name = message.text
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={recipe_name}&number=1&apiKey={API}"
    response = requests.get(url)
    data = response.json()
    await message.answer(f'{data}')