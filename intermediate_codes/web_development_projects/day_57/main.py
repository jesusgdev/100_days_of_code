from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

@app.route('/')
def home():
    current_year = datetime.now().year
    return render_template("index.html", year=current_year)


@app.route('/guess/<input_name>')
def guess_age_gender(input_name):
    agify_age = requests.get(f'https://api.agify.io?name=jesus').json()['age']
    genderize_gender = requests.get(f'https://api.genderize.io?name={input_name}').json()['gender']
    return render_template(
        'guess.html',
        name=input_name.title(),
        age=agify_age,
        gender=genderize_gender
    )

@app.route('/blog')
def blog():
    blog_response = requests.get('https://api.npoint.io/c790b4d5cab58020d391')
    all_posts = blog_response.json()
    return render_template('blog.html', posts=all_posts)

if __name__ == '__main__':
    app.run(debug=True)
