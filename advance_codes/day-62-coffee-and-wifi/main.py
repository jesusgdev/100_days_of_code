from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from dotenv import load_dotenv
import os
import csv

app = Flask(__name__)
Bootstrap5(app)

# Credentials
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


class CafeForm(FlaskForm):
    cafe_name = StringField(label='Cafe name', validators=[DataRequired()])
    location_url = StringField(label='Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open_time = StringField(label='Open Time e.g. 8:00AM', validators=[DataRequired()])
    closing_time = StringField(label='Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField(
        label='Coffee Rating',
        choices=[('☕', '☕'), ('☕☕', '☕☕'), ('☕☕☕', '☕☕☕'), ('☕☕☕☕', '☕☕☕☕'), ('☕☕☕☕☕', '☕☕☕☕☕')],
        validators=[DataRequired()]
    )
    wifi_rating = SelectField(
        label='Wi-Fi Strength Rating',
        choices=[('✘', '✘'), ('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'),
                 ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')],
        validators=[DataRequired()]
    )
    power_outlet_rating = SelectField(
        label='Power Outlet Rating',
        choices=[('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'),
                 ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')],
        validators=[DataRequired()]
    )
    submit = SubmitField(label='Submit', render_kw={'class':'btn btn-light'})


# Exercise:
# add: Location URL, open time, closing time, coffee rating, Wi-Fi rating, power outlet rating fields
# make coffee/Wi-Fi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
        cafe_name = form.cafe_name.data
        location_url = form.location_url.data
        open_time = form.open_time.data
        closing_time = form.closing_time.data
        coffee_rating = form.coffee_rating.data
        wifi_rating = form.wifi_rating.data
        power_outlet_rating = form.power_outlet_rating.data

        with open("cafe-data.csv", mode="a", encoding="utf-8") as f:
            f.write(f"\n{cafe_name},{location_url},{open_time},{closing_time},"
                    f"{coffee_rating},{wifi_rating},{power_outlet_rating}")
        return redirect(url_for('cafes'))
    return render_template(template_name_or_list='add.html', form=form)


@app.route('/cafes')
def cafes():
    with open(file='cafe-data.csv', mode='r', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = list(csv_data)
        header = list_of_rows[0]
        rows = list_of_rows[1:]
    return render_template('cafes.html', cafes_header=header, cafes_rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
