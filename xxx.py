import requests
from bs4 import BeautifulSoup
from googletrans import Translator

from config import API

translator = Translator()

recipes = []
class Recipe():
    def __init__(self, title, ingredients, info, img, count):
        self.title = title
        self.ingredients = ingredients
        self.info = info
        self.img = img
        self.count = count
    
    @staticmethod
    def from_respons_api(data, recipes_data):
        return Recipe(
            title = data['title'],
            ingredients = [ingredient['name'] for ingredient in data['extendedIngredients']],
            info = Recipe.clean_html(data['instructions']),
            img = data['image'],
            count = recipes_data['totalResults']
        )
    
    @staticmethod
    def clean_html(html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()
    
    def display_recipe_ru(self):
        title_translate = translator.translate(self.title, src='en', dest='ru').text
        ingredients_numerate = '\n'.join(f'{i + 1}. {ingredient}' for i, ingredient in enumerate(self.ingredients))
        ingredients_translate = translator.translate(ingredients_numerate, src='en', dest='ru').text
        info_translate = translator.translate(self.info, src='en', dest='ru').text
        return (
            f'Названиe:\n{title_translate}\n'
            f'Ингредиенты:\n{ingredients_translate}\n'
            f'Инструкция:\n{info_translate}\n'
            f'{self.img}\n'
            f'Найдено рецептов: {self.count}'
        )

async def get_list_recipes(recipe_name):
    response = requests.get(f'https://api.spoonacular.com/recipes/complexSearch?query={recipe_name}&number=1&apiKey={API}')
    return response.json()

async def get_detail_recipe(recipe_id):
    response = requests.get(
        f'https://api.spoonacular.com/recipes/{recipe_id}/information', 
        params={'apiKey': API}
    )
    return response.json()







