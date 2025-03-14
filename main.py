import requests

BASE_URL = 'https://www.billboard.com/charts/hot-100/'

# get_date = input('Which year do you want to travel to?  Type the date in this format YYYY-MM-DD: ')
get_date = '2010-02-02'

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

response = requests.get(url=f'{BASE_URL}{get_date}', headers = header)
