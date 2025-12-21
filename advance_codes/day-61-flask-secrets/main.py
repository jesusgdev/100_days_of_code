from wtforms import StringField, PasswordField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email, length
from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from dotenv import load_dotenv
import os

# Login credentials
load_dotenv()
csrf_token = os.getenv("CSRF_TOKEN")
my_email = os.getenv("MY_EMAIL")
my_password = os.getenv("MY_PASSWORD")

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()], )
    password = PasswordField(label='Password', validators=[DataRequired(), length(min=8)])
    submit = SubmitField(label="Log In")

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = os.getenv('CSRF_TOKEN')

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password =login_form.password.data
        if email == my_email and password == my_password:
            return redirect(url_for('success'))
        else:
            return redirect(url_for('denied'))
    return render_template(
        template_name_or_list='login.html',
        form=login_form
    )

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/denied")
def denied():
    return render_template("denied.html")

if __name__ == '__main__':
    app.run(debug=True)
