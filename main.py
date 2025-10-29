import requests
import re
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, date as date_cls


BASE_URL = 'https://www.billboard.com/charts/hot-100/'
SPOTIFY_CLIENT_ID = '64822ce98bbc45c9a1ada1c233647d24'
SPOTIFY_CLIENT_SECRET = '0621f3d75e83426db01f596ef7f13449'
SPOTIFY_REDIRECT_URI = 'https://example.com/'
YOUR_SPOTIFY_DISPLAY_NAME = 'notxap55'

# get_date = input('Which date do you want to travel to?  Type the date in this format YYYY-MM-DD: ')
# date = '2010-02-02'

def get_valid_date_str():
    min_date = date_cls(1958, 8, 4)
    max_date = date_cls.today()
    while True:
        user_input = input('Which date do you want to travel to?  Type the date in this format YYYY-MM-DD: ')
        try:
            d = datetime.strptime(user_input, '%Y-%m-%d').date()
        except ValueError:
            print("❌ Invalid format. Please use YYYY-MM-DD (e.g., 1991-07-20).")
            continue
        if not (min_date <= d <= max_date):
            print(f"❌ Date must be between {min_date} and {max_date}.")
            continue
        return d.isoformat()
    
date = get_valid_date_str()  # <-- only change: validated date string

header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0"}
response = requests.get(url=f'{BASE_URL}{date}', headers=header)

soup = BeautifulSoup(response.text, 'html.parser')
list_items = soup.select('li ul li')
songs = [
  {
    'title': li.find('h3').get_text().strip(),
    'artist': li.find('span').get_text().strip()
  }
  for li in soup.select('li ul li')
  if li.find('h3') and li.find('span')
]

sp = spotipy.Spotify(
  auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-modify-private",
    show_dialog=True,
    cache_path="token.txt",
  )
)
print("Auth OK. User:", sp.current_user()["display_name"])
print("Getting your selection.  This may take a minute...")
user_id = sp.current_user()["id"]

song_uris = []
year = date.split('-')[0]

for song in songs:
    result = sp.search(q=f'track: {song} year: {year}', type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
    description="Top 100 songs from Billboard on " + date
)
print(f"✅ Created playlist: {playlist['name']}")

sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
print("✅ Added tracks successfully!")
print("Open in Spotify:", playlist['external_urls']['spotify'])