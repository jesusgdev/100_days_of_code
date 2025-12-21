from flask import Flask
from random import randint

app = Flask(__name__)

@app.route('/')
def home():
    return ('<h1 style="text-align:center">Guess a number between 0 and 9</h1>'
            '<div style="text-align: center;">'
                '<img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmc3ZjF4ZWJiZG94d293YndieWM4MHByNzI4ejZ1OGRlYWhubjI5ciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3V33ssIjg0BUGafaU0/giphy.gif">'
            '</div>')

random_number = randint(0, 9)

@app.route("/<number>")
def user_choice(number):
    number = int(number)
    if number > random_number:
        return ("<h1 style='text-align:center; color:red;'>It's to high</h1>"
                '<div style="text-align: center;">'
                '<img src="https://media1.giphy.com/media/'
                'v1.Y2lkPTc5MGI3NjExc2FtOWx0b3R1Z2IycW1xYnl6c2luMG'
                'JiaWhtbTV5cWN6NDk4YWFjOSZlcD12MV9pbnRlcm5hbF9naWZf'
                'YnlfaWQmY3Q9Zw/P88Joa1ZRwgVWXH0te/giphy.gif">'
                '</div>')
    elif number < random_number:
        return ("<h1 style='text-align:center; color:blue;'>It's to low</h1>"
                '<div style="text-align: center;">'
                '<img src="https://media2.giphy.com/media/'
                'v1.Y2lkPTc5MGI3NjExdDdyeGg2bDU4bmxvY2kyM2p2ZmZ'
                '4OXdmc29hOW9ycTNqbGY1cXV1byZlcD12MV9pbnRlcm5hbF9'
                'naWZfYnlfaWQmY3Q9Zw/2ytlNeRGtmPJXaFbZT/giphy.gif">'
                '</div>')
    else:
        return ("<h1 style='text-align:center; color:green;'>You found me!</h1>"
                '<div style="text-align: center;">'
                '<img src="https://media0.giphy.com/media/'
                'v1.Y2lkPTc5MGI3NjExbng2YWl4NWRreWluZzh4MGM4NHNxem'
                'RvdTh3cjI1MTJ5MTJ2NXAyMiZlcD12MV9pbnRlcm5hbF9naWZ'
                'fYnlfaWQmY3Q9Zw/cXblnKXr2BQOaYnTni/giphy.gif">'
                '</div>')


if __name__ == '__main__':
    app.run(debug=True)
