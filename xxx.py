import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.russianfood.com/'
page = requests.get(url)
soup = bs(page.text, "html.parser")
all_name_recept = []
name_recept = []
all_name_recept = soup.findAll('a', class_='title')
