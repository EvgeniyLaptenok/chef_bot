import requests
import asyncio
from bs4 import BeautifulSoup
from googletrans import Translator

from config import API_RECIPES

translator = Translator()
class Recipe:
    def __init__(self, recipe_id: int) -> None:
        recipe = self.get_recipe_in_DB(recipe_id)
        if not recipe:
            recipe = self.get_recipe_in_API(recipe_id)
        
        self.id = recipe_id
        self.name = recipe['title']
        self.instructions = clean_html(recipe['instructions'])
        self.ingredients = [ingredient['name'] for ingredient in recipe['extendedIngredients']]
      
    def get_recipe_in_DB(self, recipe_id) -> dict | None:
        """Получает рецепт из БД"""
        
        
    

    def get_recipe_in_API(self, recipe_id) -> dict | None:
        """Получает рецепт из api"""

        return get_detail_recipe(recipe_id)
    

      
def clean_html(html_text):
    """Очищает текст от тегов"""

    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()        


async def request_spoonacular(query: str, params: dict={}) -> dict:
    """Возращает рецепты в json"""

    return requests.get(query, params=params, timeout=5).json()


def get_detail_recipe(recipe_id):
    """Получает рецепт по id"""

    link = f'https://api.spoonacular.com/recipes{recipe_id}/information'
    params = {'apiKey': API_RECIPES}
    
    return asyncio.run(request_spoonacular(query=link, params=params))


def get_list_recipes(recipe_name):
    """Получает рецепы по названию"""

    link = 'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'query': recipe_name,
        'apiKey': API_RECIPES
    }
    return asyncio.run(request_spoonacular(query=link, params=params))








