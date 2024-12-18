import asyncio
import aiohttp
from bs4 import BeautifulSoup
from googletrans import Translator as gt

from keys.config import API_RECIPES


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
        ...
    
    def query(self, query_text: str):
        """Запрос в БД"""
        
        ...
    
    def save_recipie(self, recipe: dict) -> None:
        """Сохраняет рецепт в БД"""
        
        ...
    
    def get_recipie(self, recipe_id: int) -> dict | None:
        """Достает рецепт из БД"""
        
        return None
        
    def save_buffer(self, chat_id: int, user_id: int, recipes_id: list) -> None:
        """Сохраняет инфу о рецептах в буффер"""
        
        ...
        
    def get_count_recipes(self, chat_id: int, user_id: int) -> int:
        """Достает количество оставшихся рецептов из буффера"""
        
        ...
    
    def drop_recipe_in_buffer(self, chat_id: int, user_id: int, recipe_id: int) -> None:
        """Удаляет рецепт из буффера"""
        
        ...
        
    def drop_user_buffer(self, chat_id: int, user_id: int) -> None:
        """Удаляет буффер по пользователю"""
        
        ...
        

class Spoonacular:
    """Класс для работы с Spoonacular api"""
    
    def __init__(self, translator):
        self.translator = translator
        self.spoonacular_link = 'https://api.spoonacular.com/recipes'
        
    async def query(self, query_text: str, query_params: dict, timeout: int = 5) -> dict:
        """Запрос в API Spoonacular"""
        
        async with aiohttp.ClientSession() as session:
            async with session.get(query_text, params=query_params) as resp:
                response = await resp.json()
                
        return response 
        
    def get_list_recipes(self, recipe_name: str) -> list:
        """Получает рецепы по названию"""

        link = f'{self.spoonacular_link}/complexSearch'
        params = {
            'query': self.translator.getEnText(recipe_name),
            'apiKey': API_RECIPES
        }
        return asyncio.run(self.query(query_text=link, query_params=params))['results']
    
    def get_detail_recipe(self, recipe_id):
        """Получает рецепт по id"""

        link = f'{self.spoonacular_link}/{recipe_id}/information'
        params = {'apiKey': API_RECIPES}
        
        return asyncio.run(self.query(query_text=link, query_params=params))


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
        
        self.id = recipe_id
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
            self.translator.getRusText(ingredient['name'])
            for ingredient in recipe['extendedIngredients']
        ])
        
        return recipe
        
    def get_recipe_in_DB(self, recipe_id) -> dict | None:
        """Получает рецепт из БД"""
        
        return self.db.get_recipie(recipe_id=recipe_id)
        
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
            f'Названиe:\n{self.name}\n\n'
            f'Ингредиенты:\n{self.ingredients}\n\n'
            f'Инструкция:\n{self.instructions}\n\n'
            f'{self.img}\n'
        )


if __name__ == '__main__':
    my_trans = Translator()
    my_db = DB()
    my_spoonacular = Spoonacular(my_trans)
    recipie_id = my_spoonacular.get_list_recipes('пицца')[0]['id']
    my_recipe = Recipe(
        recipe_id=recipie_id,
        translator=my_trans,
        spoonacular=my_spoonacular,
        db=my_db,
    )
    print(my_recipe.get_text_message_recipe())
