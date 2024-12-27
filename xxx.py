import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from googletrans import Translator as gt

from keys.config import API_RECIPES
from database import *


class Translator:
    """Класс для работы с переводчиком"""
    
    def __init__(self):
        self.translator =  gt()
    
    def getTrans(self, text: str, old_lang: str, new_lang: str) -> str:
        return (
            self.translator
            .translate(
                text,
                src=old_lang,
                dest=new_lang
            )
            .text
        )
    
    def getRusText(self, text: str) -> str:
        return self.getTrans(text=text, old_lang='en', new_lang='ru')
    
    def getEnText(self, text: str) -> str:
        return self.getTrans(text=text, old_lang='ru', new_lang='en')


class DB:
    def __init__(self):
        self.connection = my_db.connection
        self.cursor = self.connection.cursor()
    
    def query(self, query_text: str):
        """Запрос в БД"""

        self.cursor.execute(query_text)  
        return self.cursor.fetchall()
    
    def save_recipe(self, recipe: dict) -> None:
        """Сохраняет рецепт в БД"""
        
        query = '''
            INSERT INTO recipes (recipe_id, title, ingredients, instructions, image) VALUES (%s, %s, %s, %s, %s)
        '''
        self.cursor.execute(
            query, (
                recipe['id'], 
                recipe['title'], 
                recipe['ingredients'], 
                recipe['instructions'], 
                recipe['image']
            )
        )
        self.connection.commit()
    
    def get_recipe(self, recipe_id: int) -> tuple | None:
        """Достает рецепт из БД"""
        
        query = f'''SELECT * FROM recipes WHERE recipe_id = {recipe_id}'''
        result = self.query(query)
        return result[0] if result else None
        
    def save_buffer(self, chat_id: int, user_id: int, recipes_id: list) -> None:
        """Сохраняет инфу о рецептах в буффер"""
        
        query = '''INSERT INTO buffer (chat_id, user_id, recipe_id) VALUES (%s, %s, %s)'''
        for recipe_id in recipes_id:
            self.cursor.execute(query % chat_id % user_id % recipe_id)
        self.connection.commit()
        
    def get_count_recipes(self, chat_id: int, user_id: int) -> int:
        """Достает количество оставшихся рецептов из буффера"""
        
        query = '''SELECT COUNT(1) FROM buffer WHERE chat_id = %s AND user_id = %s'''
        result = self.query(query, (chat_id, user_id))  
        return result[0][0] if result else 0
    
    def drop_recipe_in_buffer(self, chat_id: int, user_id: int, recipe_id: int) -> None:
        """Удаляет рецепт из буффера"""
        
        query = '''DELETE FROM buffer WHERE chat_id = %s AND user_id = %s AND recipe_id = %s'''
        self.cursor.execute(query, (chat_id, user_id, recipe_id))  
        self.connection.commit()
        
    def drop_user_buffer(self, chat_id: int, user_id: int) -> None:
        """Удаляет буффер по пользователю"""
        
        query = '''DELETE FROM buffer WHERE chat_id = %s AND user_id = %s'''
        self.cursor.execute(query, (chat_id, user_id))  
        self.connection.commit()
        
        
class Spoonacular:
    """Класс для работы с Spoonacular api"""
    
    def __init__(self, translator: Translator):
        self.translator = translator
        self.spoonacular_link = 'https://api.spoonacular.com/recipes'
        
    async def query(self, query_text: str, query_params: dict, timeout: int = 5) -> dict:
        """Запрос в API Spoonacular"""
        
        return requests.get(query_text, params=query_params, timeout=timeout).json()
                
    def get_list_recipes(self, recipe_name: str) -> list:
        """Получает рецепы по названию"""

        link = f'{self.spoonacular_link}/complexSearch'
        params = {
            'query': self.translator.getEnText(recipe_name),
            'apiKey': API_RECIPES
        }
        
        return self.query(query_text=link, query_params=params)
    
    def get_detail_recipe(self, recipe_id):
        """Получает рецепт по id"""

        link = f'{self.spoonacular_link}/{recipe_id}/information'
        params = {'apiKey': API_RECIPES}
        
        return self.query(query_text=link, query_params=params)
        

class Recipe:
    """Класс рецепта"""
    
    def __init__(self,
                 recipe_id: int,
                 translator: Translator,
                 spoonacular: Spoonacular,
                 db: DB,
                 ) -> None:
        self.translator = translator
        self.spoonacular = spoonacular
        self.db = db
        
        recipe = self.get_recipe(recipe_id=recipe_id)
        
        self.id = recipe['id']
        self.name = recipe['title']
        self.instructions = recipe['instructions']
        self.ingredients = recipe['ingredients']
        self.img = recipe['image']
    
    def get_recipe(self, recipe_id: int) -> dict:
        """Достает рецепт"""
        
        recipe = self.get_recipe_in_DB(recipe_id=recipe_id)
        if not recipe:
            recipe = self.get_recipe_in_API(recipe_id=recipe_id)
        
        recipe['title'] = self.translator.getRusText(recipe['title'])
        recipe['instructions'] = self.translator.getRusText(
            self.clean_html(recipe['instructions'])
        )
        recipe['ingredients'] = ', '.join([
            self.translator.getRusText(ingredient['name']).capitalize()
            for ingredient in recipe['extendedIngredients']
        ])
        
        return recipe
        
    def get_recipe_in_DB(self, recipe_id) -> dict | None:
        """Получает рецепт из БД"""
        
        return self.db.get_recipe(recipe_id=recipe_id)
        
    def get_recipe_in_API(self, recipe_id: int) -> dict | None:
        """Получает рецепт из api"""
        
        return self.spoonacular.get_detail_recipe(recipe_id)
      
    def clean_html(self, html_text: str):
        """Очищает текст от тегов"""

        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()

    def get_text_message_recipe(self) -> str:
        """Формирует сообщение рецепта"""
        
        return (
            f'Названиe: {self.name}\n\n'
            f'Ингредиенты: {self.ingredients}\n\n'
            f'Инструкция:\n{self.instructions}\n\n'
            f'{self.img}\n'
        )


my_trans = Translator()
db = DB()
my_spoonacular = Spoonacular(my_trans)


