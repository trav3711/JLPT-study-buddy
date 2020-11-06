import requests
from bs4 import BeautifulSoup as bs

BASE_URL = "https://www.kanshudo.com/collections/wikipedia_jlpt/WPJLPT-N1-2201"

page = requests.get(BASE_URL)
soup = bs(page.content, 'html.parser')
row = soup.find(id='jk_265183')
container = row.find_all()

print(row.prettify())
