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
    url = f'https://api.spoonacular.com/recipes/complexSearch?query={recipe_name}&number=1&apiKey={API}'
    response = requests.get(url)
    data = response.json()
    if data['results']:
        recipe_id = data['results'][0]['id']
        recipe_data = requests.get(f'https://api.spoonacular.com/recipes/{recipe_id}/information', 
                                   params={'apiKey': API}).json()
        recipe_title = recipe_data['title']
        recipe_info = recipe_data['instructions']
        recipe_img = recipe_data['image']
        ingredients = recipe_data['extendedIngredients']
        ingredients_list = ', '.join([ingredient['name'] for ingredient in ingredients])
        count_recipe = data['totalResults']

        await message.answer(f'Название:\n{recipe_title}\n{ingredients_list}\nИнструкция:\n{recipe_info}\n{recipe_img}\n{count_recipe}',
                             reply_markup=kb.next_bt)
    else:
        await message.answer('рецепт не найден')

# @router.message(F.text == 'Ещё рецепт')
# async def recipe_next(message: Message):
    
#     await message.answer('')