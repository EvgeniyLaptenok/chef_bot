from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import keyboards as kb
from xxx import *
from database import *

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
    recipes = await my_spoonacular.get_list_recipes(recipe_name)
    recipes = recipes['results']

    if len(recipes) == 0:
        raise('Не нашлось рецептов')
    elif len(recipes) == 1:
        recipe_id = await my_spoonacular.get_detail_recipe(recipes[0]['id'])
    else:
        db.save_buffer(chat_id=chat_id, user_id=user_id, recipes_id=[recipe['id'] for recipe in recipes])
        recipe_id = await my_spoonacular.get_detail_recipe(recipes[0]['id'])
    
    my_recipe = Recipe(
        recipe_id=recipe_id,
        translator=my_trans,
        spoonacular=my_spoonacular,
        db=db,
    )
    print(my_recipe.get_text_message_recipe())

