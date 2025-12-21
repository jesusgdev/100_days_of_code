from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange, Length
from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize Bootstrap
Bootstrap5(app)

# TMDB API credentials
API_KEY_TOKEN = os.getenv('API_KEY_TOKEN')
API_KEY = os.getenv('API_KEY')

# TMDB API headers for authentication
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY_TOKEN}"
}


# CREATE DB
class Base(DeclarativeBase):
    pass


# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Define Movie model - represents the movies table in database
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[str] = mapped_column(String(4), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=False,
                                        default="There isn't any review for this movie yet")
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


# CREATE TABLE
with app.app_context():
    db.create_all()


# Form for editing movie rating and review
class MovieEditForm(FlaskForm):
    rating = FloatField(
        'Your Rating Out of 10 e.g. 7.5:',
        validators=[
            DataRequired(message='Rating is required'),
            NumberRange(min=0, max=10, message='Rating must be between 0 and 10'),
        ],
        render_kw={'class': 'form-control'}
    )
    review = StringField(
        'Your Review',
        validators=[
            DataRequired(message='Review is required'),
            Length(min=5, max=250, message='Review must be between 5 and 250 characters')
        ],
        render_kw={'class': 'form-control'}
    )
    submit = SubmitField(label='Done', render_kw={'class': 'btn btn-light'})


# Form for adding a new movie
class MovieAddForm(FlaskForm):
    title = StringField(
        'Movie Title',
        validators=[
            DataRequired(message='Title is required'),
            Length(min=1, max=250, message='Title must be between 1 and 250 characters')
        ],
        render_kw={'class': 'form-control'}
    )
    submit = SubmitField(label='Add Movie', render_kw={'class': 'btn btn-light'})


def search_movie(title):
    """
    Search for movies in TMDB API by title
    Returns a list of movies or empty list if error occurs
    """
    try:
        # TMDB search endpoint
        movie_url = "https://api.themoviedb.org/3/search/movie"

        # Use params dictionary for cleaner code
        params = {
            'query': title,
            'include_adult': 'false',
            'language': 'en-US',
            'page': 1
        }

        # Make API request
        response = requests.get(url=movie_url, headers=headers, params=params)

        # Check if request was successful
        if response.status_code == 200:
            movies = response.json()['results']

            # Format movies data
            all_movies = []
            for movie in movies:
                # Extract year from release date, handle missing dates
                year = movie.get('release_date', 'N/A')
                if year and year != 'N/A':
                    year = year.split('-')[0]

                all_movies.append({
                    "id": movie.get('id'),
                    "title": movie.get('title'),
                    "year": year,
                    "description": movie.get('overview'),
                    "rating": movie.get('vote_average'),
                    "ranking": None,
                    "review": None,
                    "img_url": movie.get('poster_path')
                })

            return all_movies
        else:
            print(f"Error: API returned status code {response.status_code}")
            return []

    except Exception as e:
        print(f"Error searching movie: {e}")
        return []


@app.route("/")
def home():
    """
    Home page - displays all movies ordered by rating
    Assigns ranking based on rating (lower rating = higher rank number)
    """
    # Read all movies from database ordered by rating
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()

    # Assign ranking based on rating (highest rating = rank 1)
    rank = len(all_movies)
    if all_movies:
        for movie in all_movies:
            movie.ranking = rank
            rank -= 1

    # Save ranking changes
    db.session.commit()

    # Render home page with movies
    return render_template(template_name_or_list="index.html", movies=all_movies)


@app.route(rule='/add', methods=['GET', 'POST'])
def add():
    """
    Add movie page - allows user to search for movies
    GET: displays search form
    POST: searches TMDB and shows results
    """
    # Create form instance
    form = MovieAddForm()

    # Handle form submission
    if form.validate_on_submit():
        # Get movie title from form
        title = form.title.data

        # Search for movies using TMDB API
        all_movies = search_movie(title=title)

        # Check if any movies were found
        if not all_movies:
            flash('No movies found. Please try another search.', 'warning')
            return render_template(template_name_or_list='add.html', form=form)

        # Redirect to selection page
        return render_template(template_name_or_list='select.html', movies=all_movies)

    # Handle GET request (show form)
    return render_template(template_name_or_list='add.html', form=form)


@app.route(rule='/select/<int:id>')
def select(id):
    """
    Select movie - adds selected movie to database
    Checks for duplicates before adding
    """
    # Check if movie already exists in database
    existing_movie = db.session.execute(
        db.select(Movie).where(Movie.id == id)
    ).scalar()

    if existing_movie:
        # If movie already exists, redirect to edit page
        flash('This movie is already in your collection!', 'info')
        return redirect(url_for(endpoint='edit', id=id))

    try:
        # TMDB endpoint for specific movie details
        url_search_by_id = f"https://api.themoviedb.org/3/movie/{id}"

        params = {'language': 'en-US'}

        # Get movie details from TMDB
        response = requests.get(url=url_search_by_id, headers=headers, params=params)

        if response.status_code == 200:
            movie = response.json()

            # Build full image URL
            img_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"

            # Extract year from release date
            year = movie.get('release_date', 'N/A')
            if year and year != 'N/A':
                year = year.split('-')[0]

            # Create new movie instance
            new_movie = Movie(
                id=id,
                title=movie.get('title'),
                year=year,
                description=movie.get('overview'),
                rating=0.0,
                ranking=None,
                review="There isn't any review for this movie yet",
                img_url=img_url
            )

            # Add to database and save
            db.session.add(new_movie)
            db.session.commit()

            flash('Movie added successfully! Now add your rating and review.', 'success')

            # Redirect to edit page to add rating and review
            return redirect(url_for(endpoint='edit', id=id))
        else:
            flash('Error fetching movie details. Please try again.', 'error')
            return redirect(url_for('add'))

    except Exception as e:
        print(f"Error selecting movie: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('add'))


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    """
    Edit movie page - allows user to update rating and review
    GET: displays edit form
    POST: updates movie in database
    """
    # Find movie in database by ID
    movie_to_update = db.session.execute(
        db.select(Movie).where(Movie.id == id)
    ).scalar()

    # Create form instance
    form = MovieEditForm()

    # Check if movie exists
    if not movie_to_update:
        flash('Movie not found.', 'error')
        return redirect(url_for('home'))

    # Handle form submission
    if form.validate_on_submit():
        # Update movie data
        movie_to_update.rating = form.rating.data
        movie_to_update.review = form.review.data

        # Save changes
        db.session.commit()

        flash('Movie updated successfully!', 'success')

        # Redirect to home
        return redirect(url_for('home'))

    # Handle GET request (show form)
    return render_template(template_name_or_list="edit.html", movie=movie_to_update, form=form)


@app.route(rule='/delete/<int:id>')
def delete(id):
    """
    Delete movie - removes movie from database
    Validates movie exists before deleting
    """
    # Find movie in database by ID
    movie_to_delete = db.session.execute(
        db.select(Movie).where(Movie.id == id)
    ).scalar()

    # Check if movie exists before deleting
    if movie_to_delete:
        db.session.delete(movie_to_delete)
        db.session.commit()
        flash('Movie deleted successfully!', 'success')
    else:
        flash('Movie not found.', 'error')

    # Redirect to home
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)