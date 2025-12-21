# Top 10 Movies Web App

## Descripción del Proyecto
Esta aplicación web permite gestionar tu colección de películas favoritas, calificarlas, agregar reseñas y mantener un ranking personalizado. Utiliza la API de TMDB (The Movie Database) para buscar y obtener información de películas.

## Tecnologías Utilizadas
- **Flask**: Framework web de Python
- **Bootstrap 5**: Framework CSS para diseño responsive
- **SQLAlchemy**: ORM para manejo de base de datos
- **Flask-WTF**: Manejo de formularios con validación
- **TMDB API**: API para información de películas
- **SQLite**: Base de datos local

---

## Paso 1: Configuración del Entorno

### 1.1 Instalar dependencias
Primero, crea un archivo `requirements.txt` con las siguientes librerías:

```txt
Flask
flask-bootstrap
Flask-SQLAlchemy
Flask-WTF
python-dotenv
requests
```

Instala las dependencias:
```bash
pip install -r requirements.txt
```

### 1.2 Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto con tus credenciales:

```env
SECRET_KEY=tu-clave-secreta-aqui
API_KEY_TOKEN=tu-token-de-tmdb
API_KEY=tu-api-key-de-tmdb
```

**¿Cómo obtener las credenciales de TMDB?**
1. Regístrate en https://www.themoviedb.org/
2. Ve a tu perfil → Configuración → API
3. Solicita una API Key (elige "Developer")
4. Copia tu API Key y tu Access Token (Bearer Token)

---

## Paso 2: Crear la Estructura de Carpetas

Organiza tu proyecto de esta manera:

```
project/
│
├── static/
│   └── css/
│       └── styles.css
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add.html
│   ├── select.html
│   └── edit.html
│
├── .env
├── app.py
└── requirements.txt
```

---

## Paso 3: Código Python Principal (app.py)

### 3.1 Importaciones y configuración inicial

```python
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange, Length
from dotenv import load_dotenv
import requests
import json
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
```

**Explicación:**
- Importamos todas las librerías necesarias
- `load_dotenv()` carga las variables de entorno desde el archivo `.env`
- Configuramos Flask con una clave secreta para sesiones y formularios
- Preparamos los headers para autenticarnos con la API de TMDB

### 3.2 Configurar la base de datos

```python
# CREATE DB
class Base(DeclarativeBase):
    pass

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Define Movie model
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False, default='0.0')
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=False, default="There isn't any review for this movie yet")
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

# CREATE TABLE
with app.app_context():
    db.create_all()
```

**Explicación:**
- Creamos una clase `Movie` que representa la tabla en la base de datos
- Cada atributo de la clase es una columna en la tabla
- `id` es la clave primaria (identificador único)
- `title` debe ser único para evitar duplicados
- `db.create_all()` crea la tabla si no existe

### 3.3 Crear formularios con validación

```python
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
            Length(min=5, max=250, message='Title must be between 5 and 250 characters')
        ],
        render_kw={'class': 'form-control'}
    )
    submit = SubmitField(label='Add Movie', render_kw={'class': 'btn btn-light'})
```

**Explicación:**
- `MovieEditForm`: Para editar la calificación y reseña de una película
- `MovieAddForm`: Para buscar y agregar nuevas películas
- Los `validators` aseguran que los datos ingresados sean correctos
- `render_kw` agrega clases CSS de Bootstrap a los campos

### 3.4 Función para buscar películas en TMDB

```python
def search_movie(title):
    # TMDB search endpoint
    movie_url = "https://api.themoviedb.org/3/search/movie"
    
    # Format title for URL (replace spaces with %20)
    formated_title = title.replace(" ", "%20")
    
    # Make API request
    response = requests.get(
        url=f"{movie_url}?query={formated_title}&include_adult=false&language=en-US&page=1&",
        headers=headers
    ).text
    
    # Parse JSON response
    movies = json.loads(response)['results']

    # Format movies data
    all_movies = []
    for movie in movies:
        all_movies.append({
            "id": movie.get('id'),
            "title": movie.get('title'),
            "year": movie.get('release_date'),
            "description": movie.get('overview'),
            "rating": movie.get('vote_average'),
            "ranking": None,
            "review": None,
            "img_url": movie.get('poster_path')
        })
    
    return all_movies
```

**Explicación:**
- Esta función busca películas en TMDB usando el título
- Formatea el título reemplazando espacios por `%20` (formato URL)
- Hace una petición GET a la API de TMDB
- Procesa la respuesta JSON y extrae los datos relevantes
- Retorna una lista de películas encontradas

### 3.5 Ruta principal (Home)

```python
@app.route("/")
def home():
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
```

**Explicación:**
- Obtiene todas las películas de la base de datos ordenadas por calificación
- Asigna un ranking: la película con menor rating obtiene el ranking más alto
- Guarda los cambios en la base de datos
- Renderiza la página principal con todas las películas

### 3.6 Ruta para agregar películas

```python
@app.route(rule='/add', methods=['GET', 'POST'])
def add():
    # Create form instance
    form = MovieAddForm()

    # Handle POST request (form submission)
    if request.method == 'POST':
        # Get movie title from form
        title = request.form.get('title').capitalize()

        # Search for movies using TMDB API
        all_movies = search_movie(title=title)

        # Redirect to selection page
        return render_template(template_name_or_list='select.html', movies=all_movies)

    # Handle GET request (show form)
    return render_template(template_name_or_list='add.html', form=form)
```

**Explicación:**
- Cuando se accede por GET, muestra el formulario para buscar películas
- Cuando se envía el formulario (POST), busca películas en TMDB
- Muestra los resultados en una página de selección

### 3.7 Ruta para seleccionar película específica

```python
@app.route(rule='/select/<int:id>')
def select(id):
    # TMDB endpoint for specific movie details
    url_search_by_id = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    # Get movie details from TMDB
    response = requests.get(url=url_search_by_id, headers=headers).text
    movie = json.loads(response)

    # Build full image URL
    img_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"

    # Create new movie instance
    new_movie = Movie(
        id=id,
        title=movie.get('title'),
        year=movie.get('release_date'),
        description=movie.get('overview'),
        rating=None,
        ranking=None,
        review=None,
        img_url=img_url
    )

    # Add to database and save
    db.session.add(new_movie)
    db.session.commit()

    # Redirect to edit page to add rating and review
    return redirect(url_for(endpoint='edit', id=id))
```

**Explicación:**
- Recibe el ID de la película seleccionada
- Obtiene los detalles completos de TMDB
- Crea una nueva entrada en la base de datos
- Redirige a la página de edición para agregar calificación y reseña

### 3.8 Ruta para editar película

```python
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    # Find movie in database by ID
    movie_to_update = db.session.execute(
        db.select(Movie).where(Movie.id == id)
    ).scalar()

    # Create form instance
    form = MovieEditForm()

    # Check if movie exists
    if not movie_to_update:
        return "<p>Movie not found</p>", 404

    # Handle POST request (form submission)
    if request.method == 'POST':
        # Get rating and review from form
        movie_rating = request.form.get('rating')
        movie_review = request.form.get('review')

        # Update movie data
        movie_to_update.rating = float(movie_rating)
        movie_to_update.review = movie_review

        # Save changes
        db.session.commit()

        # Redirect to home
        return redirect(url_for('home'))

    # Handle GET request (show form)
    return render_template(template_name_or_list="edit.html", movie=movie_to_update, form=form)
```

**Explicación:**
- Busca la película por ID en la base de datos
- Si existe, muestra el formulario para editar calificación y reseña
- Al enviar el formulario, actualiza los datos y redirige al home

### 3.9 Ruta para eliminar película

```python
@app.route(rule='/delete/<int:id>')
def delete(id):
    # Find movie in database by ID
    movie_to_delete = db.session.execute(
        db.select(Movie).where(Movie.id == id)
    ).scalar()

    # Delete movie from database
    db.session.delete(movie_to_delete)
    db.session.commit()

    # Redirect to home
    return redirect(url_for('home'))
```

**Explicación:**
- Busca la película por ID
- La elimina de la base de datos
- Redirige al home

### 3.10 Ejecutar la aplicación

```python
if __name__ == '__main__':
    app.run(debug=True)
```

**Explicación:**
- Ejecuta la aplicación en modo debug
- Permite ver errores detallados durante el desarrollo

---

## Paso 4: Templates HTML

### 4.1 base.html
Este es el template base que contiene la estructura HTML común:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no"/>

    {% block styles %}
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
    {{ bootstrap.load_css() }}

    <!-- Google Fonts -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Nunito+Sans:300,400,700"/>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Poppins:300,400,700"/>
    
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css"/>
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}"/>
    {% endblock %}

    <title>{% block title %}{% endblock %}</title>
</head>

<body>
{% block content %}{% endblock %}

<footer class="py-3"></footer>

<!-- Bootstrap JavaScript -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 4.2 index.html
Página principal que muestra todas las películas:

```html
{% extends 'base.html' %}

{% block title %}My Top 10 Movies{% endblock %}

{% block content %}
<div class="container mt-3">
    <h1 class="heading">My Top 10 Movies</h1>
    <p class="description" style="font-size: 20px">These are my all-time favourite movies.</p>

    {% if not movies %}
    <p class="description" style="text-align: center">There aren't any movie to show at the moment.</p>
    {% else %}

    {% for movie in movies %}
    <div class="card" style="width: 100%; max-width: 350px; height:500px">
        <!-- Front of card shows poster and ranking -->
        <div class="front" style="background-image: url('{{ movie.img_url }}');">
            <p class="large" style="font-size: 70px; color: yellow">{{ movie.ranking }}</p>
        </div>
        
        <!-- Back of card shows details -->
        <div class="back">
            <div>
                <div class="title" style="font-size: 18px">
                    {{ movie.title }} <span class="release_date">({{ movie.year.split('-')[0] }})</span>
                </div>
                <div class="rating">
                    <label>{{ movie.rating }}</label>
                    <i class="fas fa-star star"></i>
                </div>
                <p class="review" style="font-size: 16px">"{{ movie.review }}"</p>
                <p class="overview" style="text-align: justify; font-size: 14px;">
                    {{ movie.description }}
                </p>

                <!-- Action buttons -->
                <a href="{{ url_for('edit', id=movie.id) }}" class="button">Update</a>
                <a href="{{ url_for('delete', id=movie.id) }}" class="button delete-button">Delete</a>
            </div>
        </div>
    </div>
    {% endfor %}

    {% endif %}
</div>

<!-- Add movie button -->
<div class="container text-center add">
    <a href="{{ url_for('add') }}" class="button add-button">Add Movie</a>
</div>
{% endblock %}
```

### 4.3 add.html
Formulario para buscar películas:

```html
{% extends 'base.html' %}
{% from 'bootstrap5/form.html' import render_form %}

{% block title %}Add Movie{% endblock %}

{% block content %}
<div class="content mt-3">
    <h1 class="heading">Add a Movie</h1>
    {{ render_form(form, novalidate=True) }}
</div>
{% endblock %}
```

### 4.4 select.html
Lista de películas encontradas para seleccionar:

```html
{% extends 'base.html' %}

{% block title %}Select Movie{% endblock %}

{% block content %}
<div class="container my-3">
    <h1 class="heading">Select Movie</h1>
    {% for movie in movies %}
    <p>
        <a class="select-movie" href="{{ url_for('select', id=movie.id)}}">
            {{ movie.title + ' - ' + movie.year }}
        </a>
    </p>
    {% endfor %}
</div>
{% endblock %}
```

### 4.5 edit.html
Formulario para editar calificación y reseña:

```html
{% extends 'base.html' %}
{% from 'bootstrap5/form.html' import render_form %}

{% block title %}Edit Movies{% endblock %}

{% block content %}
<div class="content mt-4 ms-1">
    <h1 class="heading">{{ movie.title }}</h1>
    <p class="description">Edit Movie Rating</p>
    {{ render_form(form, novalidate=True) }}
</div>
{% endblock %}
```

---

## Paso 5: Ejecutar la Aplicación

1. Asegúrate de tener el archivo `.env` configurado
2. Abre la terminal en la carpeta del proyecto
3. Ejecuta:
```bash
python app.py
```
4. Abre tu navegador en: `http://127.0.0.1:5000/`

---

## Flujo de la Aplicación

1. **Página Principal**: Muestra todas las películas ordenadas por rating
2. **Agregar Película**: 
   - Click en "Add Movie"
   - Escribe el título de la película
   - Selecciona la película correcta de los resultados
   - Agrega tu calificación y reseña
3. **Editar Película**: Click en "Update" para cambiar rating o reseña
4. **Eliminar Película**: Click en "Delete" para quitar la película

---

## Sugerencias de Mejora para Principiantes

### 1. Manejo de errores mejorado
Actualmente, si la API de TMDB falla, la aplicación podría romperse. Agrega validación:

```python
def search_movie(title):
    try:
        movie_url = "https://api.themoviedb.org/3/search/movie"
        formated_title = title.replace(" ", "%20")
        response = requests.get(
            url=f"{movie_url}?query={formated_title}&include_adult=false&language=en-US&page=1&",
            headers=headers
        )
        
        # Check if request was successful
        if response.status_code == 200:
            movies = response.json()['results']
            # rest of the code...
        else:
            return []
    except Exception as e:
        print(f"Error searching movie: {e}")
        return []
```

**Por qué es importante:** Evita que tu aplicación se rompa si hay problemas con la conexión a internet o la API no responde.

### 2. Evitar duplicados al agregar películas
Antes de agregar una película, verifica si ya existe:

```python
@app.route(rule='/select/<int:id>')
def select(id):
    # Check if movie already exists
    existing_movie = db.session.execute(
        db.select(Movie).where(Movie.id == id)
    ).scalar()
    
    if existing_movie:
        # Redirect to edit if movie already exists
        return redirect(url_for(endpoint='edit', id=id))
    
    # Continue with adding new movie...
```

**Por qué es importante:** Previene errores cuando intentas agregar la misma película dos veces.

### 3. Simplificar obtención de datos del formulario
En lugar de usar `request.form.get()`, puedes usar `form.validate_on_submit()`:

```python
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    movie_to_update = db.session.execute(
        db.select(Movie).where(Movie.id == id)
    ).scalar()
    
    form = MovieEditForm()
    
    if not movie_to_update:
        return "<p>Movie not found</p>", 404

    # Simpler form validation
    if form.validate_on_submit():
        movie_to_update.rating = form.rating.data
        movie_to_update.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html", movie=movie_to_update, form=form)
```

**Por qué es importante:** Es más limpio y Flask-WTF maneja la validación automáticamente.

### 4. Mejorar legibilidad del código de búsqueda
Simplifica la construcción de la URL:

```python
def search_movie(title):
    movie_url = "https://api.themoviedb.org/3/search/movie"
    
    # Use params dictionary for cleaner code
    params = {
        'query': title,
        'include_adult': 'false',
        'language': 'en-US',
        'page': 1
    }
    
    response = requests.get(url=movie_url, headers=headers, params=params)
    movies = response.json()['results']
    # rest of the code...
```

**Por qué es importante:** Es más fácil de leer y requests maneja el formato de URL automáticamente.

### 5. Agregar validación en la ruta delete
Verifica que la película exista antes de eliminarla:

```python
@app.route(rule='/delete/<int:id>')
def delete(id):
    # Find movie in database by ID
    movie_to_delete = db.session.execute(
        db.select(Movie).where(Movie.id == id)
    ).scalar()
    
    # Check if movie exists before deleting
    if movie_to_delete:
        db.session.delete(movie_to_delete)
        db.session.commit()
    
    return redirect(url_for('home'))
```

**Por qué es importante:** Evita errores si intentas eliminar una película que no existe.

### 6. Mejorar el manejo del año en la base de datos
Considera guardar solo el año en lugar de la fecha completa:

```python
# In select route
year_only = movie.get('release_date').split('-')[0] if movie.get('release_date') else 'N/A'

new_movie = Movie(
    id=id,
    title=movie.get('title'),
    year=year_only,  # Store only the year
    # rest of the fields...
)
```

**Por qué es importante:** Simplifica el manejo de fechas y evita errores cuando la fecha no está disponible.

---

## Conclusión

¡Felicidades! Has creado una aplicación web completa para gestionar tu colección de películas. Este proyecto integra conceptos importantes de desarrollo web como:

- Manejo de bases de datos con SQLAlchemy
- Formularios con validación
- Consumo de APIs externas
- Templates con Jinja2
- Rutas y navegación con Flask

Continúa practicando y experimentando con nuevas funcionalidades. ¡El cielo es el límite!