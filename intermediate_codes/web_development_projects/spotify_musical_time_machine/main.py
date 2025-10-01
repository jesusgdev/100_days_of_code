from bs4 import BeautifulSoup
import requests
import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36"
}
date = "2000-08-12"

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=URL)
response.encoding = "utf-8"
billboard_web = response.text

soup = BeautifulSoup(billboard_web, features="html.parser")

# with open(file="billboard_2012_chart.html", mode="w") as file:
#     file.write(soup.prettify())


song_title_class = ("c-title a-font-basic u-letter-spacing-0010 u-max-width-397 lrv-u-font-size-16 "
                    "lrv-u-font-size-14@mobile-max u-line-height-22px u-word-spacing-0063 "
                    "u-line-height-normal@mobile-max a-truncate-ellipsis-2line lrv-u-margin-b-025 "
                    "lrv-u-margin-b-00@mobile-max")

band_title_class = ("c-label a-no-trucate a-font-secondary u-font-size-15 u-font-size-13@mobile-max "
                    "u-line-height-18px@mobile-max u-letter-spacing-0010 u-line-height-21px "
                    "a-children-link-color-black a-children-link-color-brand-secondary:hover "
                    "lrv-a-children-link-decoration-underline:hover lrv-u-display-block "
                    "a-truncate-ellipsis-2line u-max-width-397 u-max-width-230@tablet-only "
                    "u-max-width-300@mobile-max")

# band_tags = soup.find_all(name="span", class_=band_title_class)
# songs_tags = soup.find_all("h3", class_=song_title_class)


# for song in songs_tags:
#     print(song.getText().strip())

# for band in band_tags:
#     print(band.getText().strip())

# Connecting with Spotipy
load_dotenv()

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                              client_secret=SPOTIFY_CLIENT_SECRET,
                              redirect_uri=SPOTIPY_REDIRECT_URI,
                              scope="user-library-read",
                              show_dialog=True,
                              cache_path="token.txt",
                              username="jesusdev")
)

user_id = sp.current_user()["id"]

# taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
#
# results = sp.artist_albums(taylor_uri, album_type='album')
# albums = results['items']
# while results['next']:
#     results = sp.next(results)
#     albums.extend(results['items'])
#
# for album in albums:
#     print(album['name'])


