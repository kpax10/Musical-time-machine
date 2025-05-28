import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.billboard.com/charts/hot-100/'

# get_date = input('Which year do you want to travel to?  Type the date in this format YYYY-MM-DD: ')
get_date = '2010-02-02'

header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0"}

response = requests.get(url=f'{BASE_URL}{get_date}', headers=header)

soup = BeautifulSoup(response.text, 'html.parser')
with open('songs.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

songs_h3 = soup.select('li ul li h3')

# for song in songs_h3:
#     print(song.get_text().strip())

song_names = [song.get_text().strip() for song in songs_h3]

print(song_names)