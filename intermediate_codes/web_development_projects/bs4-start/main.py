from bs4 import BeautifulSoup
import requests

response = requests.get(url="https://news.ycombinator.com/news")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

with open(file="soup.html", mode="w") as file:
    file.write(soup.prettify())

posts = soup.find_all('tr', class_='athing submission')

post_titles = [posts[idx].select(".titleline a")[0].getText() for idx in range(len(posts))]

hyperlinks = [posts[idx].select(".titleline a")[0].get("href") for idx in range(len(posts))]


# Lista para guardar los scores
scores = []

# Recorrer cada post
for post in posts:
    # Buscar la siguiente fila (ahí está el score)
    next_row = post.find_next_sibling('tr')

    # Buscar el span con clase 'score' en esa fila
    score_element = next_row.find('span', class_='score')

    # Si encontramos el score, extraer el número
    if score_element:
        # score_element.text da algo como "847 points"
        # .split()[0] toma solo "847"
        score_number = score_element.text.split()[0]
        scores.append(int(score_number))
    else:
        # Si no hay score (como en job posts), poner 0
        scores.append(0)

max_score = max(scores)
idx = scores.index(max_score)

print(f'The post with maximun amount of points is '
      f'"{post_titles[idx]}" and its likn address is '
      f'{hyperlinks[idx]}')

