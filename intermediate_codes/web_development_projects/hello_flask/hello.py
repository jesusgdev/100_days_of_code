from flask import Flask
app = Flask(__name__)

def make_bold(function):
    def wrapper_function():
        return f"<b>{function()}</b>"
    return wrapper_function

def make_emphasis(function):
    def wrapper_function():
        return f"<em>{function()}</em>"
    return wrapper_function

def make_underlined(function):
    def wrapper_function():
        return f"<u>{function()}</u>"
    return wrapper_function

# Give a message to the root of the web.
@app.route('/')
def hello_world():
    return ('<h1 style="text-align:center">Hello, World!</h1>'
            '<div style="text-align:center">'
            '<img src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHZscDNxN2IybnNyOGpxazZ4N2ZxMzU3eGQ5eXBrZG1meno1N3NuYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/O0zVNAjUC0m3jxiflK/giphy.gif" width=600>'
            '</div>'
            '<p style="text-align:center">Traveling for the space</p>')

# Different routes using the app.route decorator.
@app.route('/bye')
@make_bold
@make_emphasis
@make_underlined
def bye():
    return "<h1>Bye!</h1>"

# Creating variables paths and converting the path to a specified data type.
@app.route('/username/<name>/<int:number>')
def greet(name, number):
    return f"Hello there {name}, you are {number} years old!"

if __name__ == "__main__":
    # Run the app in debug mode to auto-reload.
    app.run(debug=True)

