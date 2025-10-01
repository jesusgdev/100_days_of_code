import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
response = requests.get(url=URL)
response.encoding = "utf-8"
empire_web_page = response.text

soup = BeautifulSoup(empire_web_page, features="html.parser")

with open(file="soup.html", mode="w", encoding="utf-8") as file:
    file.write(soup.prettify())

movies = soup.find_all('h3', class_="title")[::-1]

with open(file="movies.txt", mode="w") as file:
    for movie in movies:
        file.write(f"{movie.getText()}\n")

