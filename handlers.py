from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from googletrans import Translator

import keyboards as kb
from xxx import *
from database import *

translator = Translator()

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f'Привет, шеф {message.from_user.first_name}! Нажми на кнопку "Поиск рецепта"', 
        reply_markup=kb.search_bt
    )

@router.message(F.text == 'Поиск рецепта')
async def input_recipe(message: Message):
    await message.answer('Введи название рецепта')

@router.message()
async def search_recipe(message: Message):
    recipe_name = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    get_recipe_id(recipe_name)
       
    

    