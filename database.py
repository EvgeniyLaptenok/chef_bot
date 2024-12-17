import psycopg2
from config import USER_DB, PASSWORD_DB

class MyDB:
    host = '90.154.74.21',
    database = 'hubbledjdb',
    port = '5432'

    def __init__(self, user_name: str, user_pass: str):
        self.cursor = self.create_connect(
        user_name=user_name,
        user_pass=user_pass 
        )
    
    @classmethod
    def create_connect(cls, user_name: str, user_pass: str) -> 'psycopg2.extensions.cursor':
        """Генерирует коннект"""
        
        connect = psycopg2.connect(
            host=cls.host,
            port=cls.port,
            database=cls.database,
            user=user_name,
            password=user_pass,
        )
        return connect.cursor()
    
    def creat_table(self):
        """Создает таблицу, если её нет"""

        table_recipes = '''
            CREATE TABLE IF NOT EXISTS recipes (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                ingredients TEXT[] NOT NULL,
                instructions TEXT NOT NULL,
                image TEXT NOT NULL
            )
        '''
        self.cursor.execute(table_recipes)
        self.cursor.connection.commit()

    def query(self, txt_query: str) -> list:
        """Запрос в db"""
        
        return self.cursor.execute(txt_query)

my_db = MyDB(user_name=USER_DB, user_pass=PASSWORD_DB)
my_db.query('select * from recipes limit 10')


class BufferRecipe:
    def __init__(self, chat_id, user_id, recipe_id):
        self.chat_id = chat_id
        self.user_id = user_id
        self.recipe_id = recipe_id
    
    def save_info_user (self) -> None:
        """Сохраняет инфу о пользователе в базе данных"""
        
        insert_query = '''
            INSERT INTO buffer_recipe (chat_id, user_id, recipe_id)
            VALUES (%s, %s, %s)
        '''
        
    def del_info_user(self):

    
buffer = BufferRecipe()