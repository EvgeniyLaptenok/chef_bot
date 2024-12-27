import psycopg2
from keys.config import USER_DB, PASSWORD_DB

class MyDB:
    host = '90.154.74.21'
    database = 'hubbledjdb'
    port = '5432'

    def __init__(self, user_name: str, user_pass: str):
        self.connection = self.create_connect(
        user_name=user_name,
        user_pass=user_pass 
        )
        self.cursor = self.connection.cursor()
    
    @classmethod
    def create_connect(cls, user_name: str, user_pass: str):
        """Генерирует коннект"""
        
        connect = psycopg2.connect(
            host=cls.host,
            port=cls.port,
            database=cls.database,
            user=user_name,
            password=user_pass,
        )
        return connect
    
    def create_table(self):
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
        self.connection.commit()
    
    def create_buffer(self):
        """Создает таблицу, если её нет"""

        table_buffer = '''
            CREATE TABLE IF NOT EXISTS buffer (
                id SERIAL PRIMARY KEY,
                chat_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                recipe_id INTEGER NOT NULL
            )
        '''
        self.cursor.execute(table_buffer)
        self.connection.commit()

my_db = MyDB(user_name=USER_DB, user_pass=PASSWORD_DB)
my_db.create_table()
my_db.create_buffer()


    
