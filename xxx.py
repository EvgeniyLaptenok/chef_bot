import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import asyncio

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
        ingredients_numerate = '\t\n'.join(f'{num}. {ingredient}' for num, ingredient in enumerate(self.ingredients, 1))
        ingredients_translate = translator.translate(ingredients_numerate, src='en', dest='ru').text
        info_translate = translator.translate(self.info, src='en', dest='ru').text
        return (
            f'Названиe:\n{title_translate}\n'
            f'Ингредиенты:\n{ingredients_translate}\n'
            f'Инструкция:\n{info_translate}\n'
            f'{self.img}\n'
            f'Найдено рецептов: {self.count}'
        )


class Recipe:
    def __init__(self, recipe_id: int) -> None:
        recept = self.getRecipeInDB(recipe_id)
        if not recept:
            recept = self.getRecipeInAPI(recipe_id)
        
        self.name = recept['name']
        self.id = recipe_id
        
        
    def getRecipeInDB(self, recipe_id) -> dict | None:
        pass
        
        
    def getRecipeInAPI(self, recipe_id) -> dict | None:
        pass
        


async def request_spoonacular(query: str, params: dict={}) -> dict:
    return requests.get(query, params=params, timeout=5).json()


def get_detail_recipe(recipe_id):
    
    link = f'https://api.spoonacular.com/recipes{recipe_id}/information'
    params={'apiKey': API}
    
    return asyncio.run(request_spoonacular(query=link, params=params))
    

def get_list_recipes(recipe_name):
    
    link = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'query': recipe_name,
        'apiKey': API
    }
    return asyncio.run(request_spoonacular(query=link, params=params))