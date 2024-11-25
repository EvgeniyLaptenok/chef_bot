from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)

search_bt = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Поиск рецепта')]], 
                                resize_keyboard=True, one_time_keyboard=True)