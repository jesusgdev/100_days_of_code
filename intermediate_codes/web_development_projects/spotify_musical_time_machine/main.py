from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import spotipy
import json
import os

# 1. Get user input for the Billboard chart date
is_valid = True
while is_valid:
    date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        print("Ivalid date format. Use YYYY-MM-DD")
    else:
        is_valid = False

# 2. Configure web scraping settings

# User-Agent Header to identify the browser making the request
HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36"
}

# Billboard Hot 100 chart URL with the specified date
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

# 3. Fetch and parse Billboard webpage
try:
    response = requests.get(url=URL, headers=HEADER)
    response.encoding = "utf-8"
    response.raise_for_status()  # Raise error for bad status codes
    billboard_html = response.text
except requests.exceptions.RequestException as e:
    print(f"Error fetching Billboard data: {e}")
    exit()

# Parse HTML content with BeautifulSoup
soup = BeautifulSoup(billboard_html, features="html.parser")

# 4. Extract song and artist information

# CSS classes for song titles (these may change over time)
SONG_TITLE_CLASS = ("c-title a-font-basic u-letter-spacing-0010 u-max-width-397 lrv-u-font-size-16 "
                    "lrv-u-font-size-14@mobile-max u-line-height-22px u-word-spacing-0063 "
                    "u-line-height-normal@mobile-max a-truncate-ellipsis-2line lrv-u-margin-b-025 "
                    "lrv-u-margin-b-00@mobile-max")

# CSS classes for artist names
ARTIST_CLASS = ("c-label a-no-trucate a-font-secondary u-font-size-15 u-font-size-13@mobile-max "
                    "u-line-height-18px@mobile-max u-letter-spacing-0010 u-line-height-21px "
                    "a-children-link-color-black a-children-link-color-brand-secondary:hover "
                    "lrv-a-children-link-decoration-underline:hover lrv-u-display-block "
                    "a-truncate-ellipsis-2line u-max-width-397 u-max-width-230@tablet-only "
                    "u-max-width-300@mobile-max")

# Find all song and artist tags
artist_tags = soup.find_all(name="span", class_=ARTIST_CLASS)
song_tags = soup.find_all(name="h3", class_=SONG_TITLE_CLASS)

# Verify we found 100 songs
if len(song_tags) < 100 or len(artist_tags) < 100:
    print(f"Warning: Only found {len(song_tags)} songs and {len(artist_tags)} artists")

# Create search queries in Spotify format: "track:Song Name artist:Artist Name"
search_queries = [
    f"track:{song_tags[i].get_text().strip()} artist:{artist_tags[i].get_text().strip()}"
    for i in range(min(len(song_tags), len(artist_tags)))
]

print(f"Found {len(search_queries)} songs from Billboard")

# 5. Authenticate with Spotify API

# Load environment variables from .env file
load_dotenv()

# Retrieve Spotify credentials from environment variables
SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]

# Verify credentials are loaded
if not all([SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI]):
    print("Error: Missing Spotify credentials in .env file")
    exit()

# Initialize Spotify client with OAuth authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                              client_secret=SPOTIFY_CLIENT_SECRET,
                              redirect_uri=SPOTIPY_REDIRECT_URI,
                              scope="playlist-modify-public "
                                    "playlist-modify-private ",
                              show_dialog=True,
                              cache_path="token.txt",
                              username="jesusdev")
)

# Get authenticated user's ID
user_id = sp.current_user()["id"]
print(f"Usuario Autenticado: {user_id}")


track_uris = []
songs_not_found = []
# Go throght each search query
for i in range(len(search_queries)):
    query = search_queries[i]

    try:
        # Search for the song in Spotify
        result = sp.search(q=query, type="track", limit=1)

        # Check if you found any song
        if result["tracks"]["items"]:
            # Extract the URI of the first song found
            track_uri = result["tracks"]["items"][0]["uri"]
            track_uris.append(track_uri)
            print(f"✓ Found song {i + 1}/100")
        else:
            # The song is not available in Spotify
            song_name = song_tags[i].get_text().strip()
            songs_not_found.append(song_name)
            print(f"✗ Not found: {song_name}")

    except Exception as e:
        print(f"✗ Error searching song {i + 1}: {e}")

# Create the playlist using the list of uris tracks found.
if track_uris:
    playlist = sp.user_playlist_create(
        user=user_id,
        name=f"Billboard Hot 100 - {date}",
        public=True,
        description=f"Top 100 songs from Billboard on {date}. Created with Python."
    )

    playlist_id = playlist["id"]
    print(f"Playlist created: {playlist['name']}")

# Save the playlist ID and print it was created.
print(f"Added {len(track_uris)} songs to the playlist")
print(f"Playlist URL: https://open.spotify.com/playlist/{playlist_id}")

# Method to find and delete empty playlists
# Find all the playslists
playlists = sp.current_user_playlists(limit=50)
deleted_count = 0

for playlist in playlists["items"]:
    if playlist["owner"]["id"] == user_id and playlist["tracks"]["total"] == 0:
        sp.current_user_unfollow_playlist(playlist["id"])
        print(f"✓ Deleted empty playlist: {playlist['name']}")
        deleted_count += 1

if deleted_count > 0:
    print(f"Total empty playlists deleted: {deleted_count}")

