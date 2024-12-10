from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from googletrans import Translator

import keyboards as kb
from xxx import *

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
    recipes_data = get_list_recipes(recipe_name)
    recipe = Recipe(recipes_data['results'][0]['id'])
    

    
   
    
    
    
    
    # def clean_html(html_text):
    #     soup = BeautifulSoup(html_text, 'html.parser')
    #     return soup.get_text()
    # class Recipe():
    #     def __init__(self, title, ingredients_list, info, img, count):
    #         self.title = title
    #         self.ingredients_list = ingredients_list
    #         self.info = info
    #         self.img = img
    #         self.count = count

    #     async def recipe_print(self):
    #         await message.answer(
    #             (
    #                 f'Названиe:\n{self.title}\n'
    #                 f'Ингредиенты:\n{self.ingredients_list}\n'
    #                 f'Инструкция:\n{self.info}\n'
    #                 f'{self.img}\n'
    #                 f'{self.count}'
    #             ),
    #             reply_markup=kb.next_bt
    #         )

    # class RecipeApi():
    #     def __init__(self, url):
    #         self.url = url
        
    #     def get_recipe(self):
    #         response = requests.get(f'{self.url}/recipes/complexSearch?query={recipe_name}&number=1&apiKey={API}')
    #         data = response.json()

    #         if data['results']:
    #             recipe_id = data['results'][0]['id']
    #             recipe_data = requests.get(
    #                 f'{self.url}/recipes/{recipe_id}/information', 
    #                     params={'apiKey': API}
    #             ).json()
    #             ingredients = recipe_data['extendedIngredients']

    #             return Recipe(
    #                 title = recipe_data['title'],
    #                 ingredients_list = ', '.join([ingredient['name'] for ingredient in ingredients]),
    #                 info = clean_html(recipe_data['instructions']),
    #                 img = recipe_data['image'],
    #                 count = data['totalResults']
    #             )
            
    # url = f'https://api.spoonacular.com'

    # api_recipe = RecipeApi(url)
    # recipe = api_recipe.get_recipe()
    # recipe.recipe_print()

# @router.message(F.text == 'Ещё рецепт')
# async def recipe_next(message: Message):
    
#     await message.answer('')