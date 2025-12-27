# 📝 Blog con Autenticación de Usuarios - Guía Completa

## 📖 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Requisitos Previos](#requisitos-previos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Paso 1: Configuración Inicial](#paso-1-configuración-inicial)
6. [Paso 2: Modelos de Base de Datos](#paso-2-modelos-de-base-de-datos)
7. [Paso 3: Formularios con WTForms](#paso-3-formularios-con-wtforms)
8. [Paso 4: Sistema de Autenticación](#paso-4-sistema-de-autenticación)
9. [Paso 5: Rutas de Usuario](#paso-5-rutas-de-usuario)
10. [Paso 6: Sistema de Comentarios](#paso-6-sistema-de-comentarios)
11. [Paso 7: Gestión de Posts](#paso-7-gestión-de-posts)
12. [Paso 8: Templates HTML](#paso-8-templates-html)
13. [Paso 9: Integración de Gravatar](#paso-9-integración-de-gravatar)
14. [Paso 10: Estilos CSS](#paso-10-estilos-css)
15. [Conceptos Clave](#conceptos-clave)
16. [Troubleshooting](#troubleshooting)

---

## Descripción del Proyecto

Este es un **blog completo** construido con Flask que incluye:

- ✅ Sistema de autenticación de usuarios (registro, login, logout)
- ✅ CRUD completo de posts de blog (solo para administradores)
- ✅ Sistema de comentarios para usuarios registrados
- ✅ Relaciones de base de datos (usuarios, posts, comentarios)
- ✅ Avatares de perfil con Gravatar
- ✅ Editor de texto enriquecido (CKEditor)
- ✅ Protección de rutas con decoradores
- ✅ Interfaz moderna con Bootstrap 5

---

## Requisitos Previos

### Conocimientos necesarios:
- Python básico (variables, funciones, clases)
- HTML/CSS básico
- Conceptos básicos de bases de datos

### Software necesario:
- Python 3.8 o superior
- Editor de código (VS Code, PyCharm, etc.)
- Navegador web moderno

---

## Estructura del Proyecto

```
blog-project/
│
├── main.py                 # Archivo principal de la aplicación
├── forms.py                # Formularios WTForms
├── .env                    # Variables de entorno (SECRET_KEY)
│
├── templates/              # Plantillas HTML
│   ├── header.html
│   ├── footer.html
│   ├── index.html
│   ├── post.html
│   ├── make-post.html
│   ├── register.html
│   ├── login.html
│   ├── about.html
│   └── contact.html
│
├── static/                 # Archivos estáticos
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── scripts.js
│   └── assets/
│       └── img/
│
└── instance/              # Base de datos SQLite
    └── posts.db
```

---

## Instalación y Configuración

### 1. Crear entorno virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install flask
pip install flask-sqlalchemy
pip install flask-wtf
pip install flask-login
pip install flask-ckeditor
pip install flask-bootstrap
pip install python-dotenv
pip install werkzeug
```

### 3. Crear archivo .env

Crea un archivo llamado `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-clave-super-secreta-aqui-cambiar-en-produccion
```

**Importante:** Nunca compartas tu `SECRET_KEY` públicamente.

---

## Paso 1: Configuración Inicial

### Crear `main.py` - Parte 1: Imports y configuración básica

```python
# ============================================================================
# STANDARD LIBRARY IMPORTS
# ============================================================================
import os
from datetime import date
from functools import wraps
import hashlib

# ============================================================================
# FLASK CORE
# ============================================================================
from flask import Flask, abort, render_template, redirect, url_for, flash

# ============================================================================
# FLASK EXTENSIONS - UI
# ============================================================================
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor

# ============================================================================
# FLASK EXTENSIONS - DATABASE
# ============================================================================
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column

# ============================================================================
# FLASK EXTENSIONS - AUTHENTICATION
# ============================================================================
from flask_login import (
    UserMixin, login_user, LoginManager, 
    current_user, logout_user
)
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================================
# ENVIRONMENT CONFIGURATION
# ============================================================================
from dotenv import load_dotenv

# ============================================================================
# LOCAL IMPORTS
# ============================================================================
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize extensions
ckeditor = CKEditor(app)
Bootstrap5(app)
```

### Explicación de los imports:

- **`os`**: Para acceder a variables de entorno
- **`date`**: Para obtener la fecha actual al crear posts
- **`wraps`**: Para crear decoradores personalizados
- **`hashlib`**: Para generar hashes MD5 (usado en Gravatar)
- **Flask core**: Funciones principales de Flask
- **Flask-Bootstrap**: Para usar Bootstrap 5 fácilmente
- **Flask-CKEditor**: Editor de texto enriquecido
- **SQLAlchemy**: ORM para base de datos
- **Flask-Login**: Manejo de sesiones de usuario
- **Werkzeug**: Para hashear contraseñas de forma segura
- **python-dotenv**: Para cargar variables de entorno desde `.env`

---

## Paso 2: Modelos de Base de Datos

### Configurar SQLAlchemy

```python
# CREATE DATABASE
class Base(DeclarativeBase):
    pass

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)
```

### Modelo User

```python
class User(db.Model, UserMixin):
    """
    User model - Represents registered users.
    
    Inherits from:
    - db.Model: Makes this a SQLAlchemy database table
    - UserMixin: Provides Flask-Login methods (is_authenticated, is_active, get_id)
    
    Relationships:
    - ONE User → MANY BlogPosts
    - ONE User → MANY Comments
    """
    __tablename__ = "users"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # User data
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Relationships - virtual properties
    posts: Mapped[list["BlogPost"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="comment_author",
        cascade="all, delete-orphan"
    )
    
    def avatar(self, size=100):
        """Return Gravatar URL for this user"""
        return gravatar_url(self.email, size=size)
    
    def __repr__(self):
        return f'<User: {self.name}>'
```

### Modelo BlogPost

```python
class BlogPost(db.Model):
    """
    BlogPost model - Represents blog articles.
    
    Relationships:
    - MANY BlogPosts → ONE User (author)
    - ONE BlogPost → MANY Comments
    """
    __tablename__ = "blog_posts"
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Foreign key - links to User
    author_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("users.id"), 
        nullable=False
    )
    
    # Post content
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    
    # Relationships - virtual properties
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="parent_post",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f'<BlogPost: {self.title}>'
```

### Modelo Comment

```python
class Comment(db.Model):
    """
    Comment model - Represents user comments on blog posts.
    
    Relationships:
    - MANY Comments → ONE User (comment author)
    - MANY Comments → ONE BlogPost (parent post)
    """
    __tablename__ = 'comments'
    
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Foreign key 1 - links to User
    author_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("users.id"), 
        nullable=False
    )
    
    # Foreign key 2 - links to BlogPost
    post_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("blog_posts.id"), 
        nullable=False
    )
    
    # Relationships - virtual properties
    comment_author: Mapped["User"] = relationship(back_populates="comments")
    parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")
    
    # Comment content
    text: Mapped[str] = mapped_column(Text, nullable=False)
    
    def __repr__(self):
        return f'<Comment by {self.comment_author.name}>'
```

### Crear las tablas

```python
# Create all tables
with app.app_context():
    db.create_all()
```

### Conceptos clave de los modelos:

1. **Primary Key (`id`)**: Identificador único de cada registro
2. **Foreign Key**: Columna que referencia el ID de otra tabla
3. **Relationship**: Propiedad virtual para acceder a objetos relacionados
4. **`back_populates`**: Conecta relaciones en ambas direcciones
5. **`cascade="all, delete-orphan"`**: Al eliminar un padre, elimina sus hijos

---

## Paso 3: Formularios con WTForms

Crear archivo `forms.py`:

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, Email, InputRequired, Length
from flask_ckeditor import CKEditorField


class CreatePostForm(FlaskForm):
    """
    Form for creating/editing blog posts.
    Only accessible by admin users.
    """
    title = StringField(
        label="Blog Post Title", 
        validators=[DataRequired()]
    )
    subtitle = StringField(
        label="Subtitle", 
        validators=[DataRequired()]
    )
    img_url = StringField(
        label="Blog Image URL", 
        validators=[DataRequired(), URL()]
    )
    body = CKEditorField(
        label="Blog Content", 
        validators=[DataRequired()]
    )
    submit = SubmitField(label="Submit Post")


class RegisterForm(FlaskForm):
    """
    Form for new user registration.
    """
    email = EmailField(
        label='Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        label='Password', 
        validators=[
            InputRequired(),
            Length(min=8, max=250, message='Password must be at least 8 characters')
        ]
    )
    name = StringField(
        label='Name', 
        validators=[DataRequired()]
    )
    submit = SubmitField(label='SIGN ME UP!')


class LoginForm(FlaskForm):
    """
    Form for user login.
    """
    email = EmailField(
        label='Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        label='Password', 
        validators=[
            InputRequired(),
            Length(min=8, max=250)
        ]
    )
    submit = SubmitField(label='LET ME IN!')


class CommentForm(FlaskForm):
    """
    Form for submitting comments on blog posts.
    Only accessible by logged-in users.
    """
    comment_text = CKEditorField(
        label="Comment", 
        validators=[DataRequired()]
    )
    submit = SubmitField(label="Submit Comment")
```

### Explicación de los validadores:

- **`DataRequired()`**: El campo no puede estar vacío
- **`Email()`**: Valida formato de email
- **`URL()`**: Valida formato de URL
- **`Length(min, max)`**: Longitud mínima y máxima
- **`InputRequired()`**: Similar a DataRequired pero más estricto

---

## Paso 4: Sistema de Autenticación

### Configurar Flask-Login

```python
# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login callback to reload user object from user ID in session.
    
    Args:
        user_id (str): The user ID stored in the session
    
    Returns:
        User object or None if user doesn't exist
    """
    return db.session.get(User, int(user_id))
```

### Función Gravatar

```python
def gravatar_url(email, size=50, default='retro', rating='g'):
    """
    Generate Gravatar URL from email address.
    
    Args:
        email (str): User's email address
        size (int): Image size in pixels (default: 50)
        default (str): Default image style if no Gravatar exists
        rating (str): Content rating ('g', 'pg', 'r', 'x')
    
    Returns:
        str: Gravatar image URL
    """
    # Create MD5 hash of email
    email_hash = hashlib.md5(email.lower().strip().encode('utf-8')).hexdigest()
    
    # Build and return URL
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d={default}&r={rating}"


# Make gravatar available in templates
app.jinja_env.globals['gravatar'] = gravatar_url
```

### Decorador admin_only

```python
def admin_only(f):
    """
    Decorator to restrict routes to admin users only (user_id = 1).
    Returns 403 Forbidden if user is not admin.
    
    Usage:
        @app.route('/admin-route')
        @admin_only
        def admin_function():
            ...
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Check if current user is admin (id = 1)
        if current_user.id != 1:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return wrapper
```

---

## Paso 5: Rutas de Usuario

### Ruta de Registro

```python
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    
    GET: Display registration form
    POST: Process registration and create new user
    """
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Get form data
        email = form.email.data
        name = form.name.data
        password = form.password.data
        
        # Hash password securely
        password_hashed = generate_password_hash(
            password=password,
            method="pbkdf2:sha256",
            salt_length=8
        )
        
        # Check if user already exists
        user = db.session.scalar(
            db.select(User).where(User.email == email)
        )
        
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!", "error")
            return redirect(url_for('login'))
        
        # Create new user
        new_user = User(
            email=email,
            password=password_hashed,
            name=name,
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Log in the new user
        login_user(new_user)
        
        return redirect(url_for('get_all_posts'))
    
    return render_template("register.html", form=form)
```

### Ruta de Login

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.
    
    GET: Display login form
    POST: Authenticate user and create session
    """
    form = LoginForm()
    
    if form.validate_on_submit():
        # Get form data
        provided_email = form.email.data
        provided_password = form.password.data
        
        # Find user by email
        user = db.session.scalar(
            db.select(User).where(User.email == provided_email)
        )
        
        # Validate credentials
        if not user:
            flash('That email does not exist, please try again', 'error')
            return redirect(url_for('login'))
        
        elif not check_password_hash(user.password, provided_password):
            flash('Password incorrect, please try again.', 'error')
            return redirect(url_for('login'))
        
        else:
            # Credentials valid - log in user
            login_user(user)
            return redirect(url_for('get_all_posts'))
    
    return render_template("login.html", form=form)
```

### Ruta de Logout

```python
@app.route('/logout')
def logout():
    """
    Log out current user and redirect to home page.
    """
    logout_user()
    return redirect(url_for('get_all_posts'))
```

---

## Paso 6: Sistema de Comentarios

### Ruta show_post con comentarios

```python
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    """
    Display individual blog post with comments.
    
    GET: Show post and comment form
    POST: Process new comment submission
    
    Args:
        post_id (int): ID of the blog post to display
    """
    # Get post or return 404 if not found
    requested_post = db.get_or_404(BlogPost, post_id)
    
    # Create comment form
    comment_form = CommentForm()
    
    # Process comment submission
    if comment_form.validate_on_submit():
        
        # Check if user is logged in
        if not current_user.is_authenticated:
            flash('You need to login or register to comment.', 'error')
            return redirect(url_for('login'))
        
        # Create new comment
        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
        
        flash('Comment added successfully!', 'success')
        return redirect(url_for('show_post', post_id=post_id))
    
    return render_template(
        "post.html",
        post=requested_post,
        form=comment_form
    )
```

---

## Paso 7: Gestión de Posts

### Ruta Home (listar todos los posts)

```python
@app.route('/')
def get_all_posts():
    """
    Display all blog posts on home page.
    """
    # Get all posts from database
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    
    return render_template("index.html", all_posts=posts)
```

### Ruta Crear Post (solo admin)

```python
@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    """
    Create a new blog post (admin only).
    
    GET: Display post creation form
    POST: Process and save new post
    """
    form = CreatePostForm()
    
    if form.validate_on_submit():
        # Create new post
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for("get_all_posts"))
    
    return render_template("make-post.html", form=form)
```

### Ruta Editar Post (solo admin)

```python
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    """
    Edit existing blog post (admin only).
    
    Args:
        post_id (int): ID of post to edit
    """
    # Get post or 404
    post = db.get_or_404(BlogPost, post_id)
    
    # Pre-populate form with existing data
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    
    if edit_form.validate_on_submit():
        # Update post with new data
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        
        return redirect(url_for("show_post", post_id=post.id))
    
    return render_template("make-post.html", form=edit_form, is_edit=True)
```

### Ruta Eliminar Post (solo admin)

```python
@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    """
    Delete a blog post (admin only).
    
    Args:
        post_id (int): ID of post to delete
    """
    # Get post or 404
    post_to_delete = db.get_or_404(BlogPost, post_id)
    
    # Delete post
    db.session.delete(post_to_delete)
    db.session.commit()
    
    return redirect(url_for('get_all_posts'))
```

### Rutas About y Contact

```python
@app.route("/about")
def about():
    """Display about page."""
    return render_template("about.html")


@app.route("/contact")
def contact():
    """Display contact page."""
    return render_template("contact.html")
```

---

## Paso 8: Templates HTML

### header.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Jesus's Blog</title>
    
    {% block styles %}
    {{ bootstrap.load_css() }}
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='assets/favicon.ico') }}" />
    <script src="https://use.fontawesome.com/releases/v6.3.0/js/all.js"></script>
    <link href="https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800" rel="stylesheet" />
    <link href="{{ url_for('static', filename='css/styles.css') }}" rel="stylesheet" />
    {% endblock %}
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light" id="mainNav">
        <div class="container px-4 px-lg-5">
            <a class="navbar-brand" href="/">Start Bootstrap</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive">
                Menu
                <i class="fas fa-bars"></i>
            </button>
            <div class="collapse navbar-collapse" id="navbarResponsive">
                <ul class="navbar-nav ms-auto py-4 py-lg-0">
                    <li class="nav-item">
                        <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('get_all_posts') }}">Home</a>
                    </li>
                    
                    {% if not current_user.is_authenticated %}
                    <li class="nav-item">
                        <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('login') }}">Login</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('register') }}">Register</a>
                    </li>
                    {% else %}
                    <li class="nav-item">
                        <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('logout') }}">Log Out</a>
                    </li>
                    {% endif %}
                    
                    <li class="nav-item">
                        <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('about') }}">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('contact') }}">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</body>
</html>
```

### post.html (con comentarios)

```html
{% from 'bootstrap5/form.html' import render_form %}
{% include "header.html" %}

<!-- Page Header -->
<header class="masthead" style="background-image: url('{{post.img_url}}')">
    <div class="container position-relative px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
            <div class="col-md-10 col-lg-8 col-xl-7">
                <div class="post-heading">
                    <h1>{{ post.title }}</h1>
                    <h2 class="subheading">{{ post.subtitle }}</h2>
                    <span class="meta">
                        Posted by
                        <a href="#">{{ post.author.name }}</a>
                        on {{ post.date }}
                    </span>
                </div>
            </div>
        </div>
    </div>
</header>

<!-- Post Content -->
<article>
    <div class="container px-4 px-lg-5">
        <div class="row gx-4 gx-lg-5 justify-content-center">
            <div class="col-md-10 col-lg-8 col-xl-7 mb-3">
                
                <!-- Post body -->
                {{ post.body|safe }}
                
                <!-- Edit button (admin only) -->
                {% if current_user.id == 1 %}
                <div class="d-flex justify-content-end mb-4">
                    <a class="btn btn-primary" href="{{url_for('edit_post', post_id=post.id)}}">
                        Edit Post
                    </a>
                </div>
                {% endif %}
                
                <hr class="my-4">
                
                <!-- Comments section -->
                <h3>Comments ({{ post.comments|length }})</h3>
                
                {% if post.comments %}
                    <ul class="commentList">
                        {% for comment in post.comments %}
                        <li>
                            <div class="commenterImage">
                                <img src="{{ gravatar(comment.comment_author.email) }}"
                                     alt="{{ comment.comment_author.name }}"/>
                            </div>
                            <div class="commentText">
                                {{ comment.text|safe }}
                                <span class="date sub-text">{{ comment.comment_author.name }}</span>
                            </div>
                        </li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <p class="text-muted">No comments yet. Be the first to comment!</p>
                {% endif %}
                
                <!-- Flash messages -->
                {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                    <p class="flash {{ category }}">{{ message }}</p>
                    {% endfor %}
                {% endif %}
                {% endwith %}
                
                <hr class="my-4">
                
                <!-- Comment form -->
                {{ render_form(form, novalidate=True) }}
                
            </div>
        </div>
    </div>
</article>

{% include "footer.html" %}

<!-- Load CKEditor -->
{{ ckeditor.load() }}
{{ ckeditor.config(name='comment_text') }}
```

---

##

____________________________________________________________________________________________________________

# 📝 Blog Project - Guía Completa de Desarrollo

## 📋 Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Configuración](#instalación-y-configuración)
- [Desarrollo Paso a Paso](#desarrollo-paso-a-paso)
- [Funcionalidades](#funcionalidades)
- [Explicación del Código](#explicación-del-código)

---

## 📖 Descripción del Proyecto

Este es un **blog completo** desarrollado con Flask que incluye:
- ✅ Sistema de autenticación de usuarios (registro y login)
- ✅ Creación, edición y eliminación de posts
- ✅ Sistema de comentarios con avatares Gravatar
- ✅ Permisos de administrador
- ✅ Editor de texto enriquecido (CKEditor)
- ✅ Diseño responsivo con Bootstrap 5

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de datos**: SQLite + SQLAlchemy
- **Autenticación**: Flask-Login + Werkzeug Security
- **Formularios**: Flask-WTF + WTForms
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Editor**: CKEditor
- **Avatares**: Gravatar

---

## 📁 Estructura del Proyecto

```
blog-project/
│
├── main.py                 # Archivo principal de la aplicación
├── forms.py                # Formularios WTForms
├── .env                    # Variables de entorno (SECRET_KEY)
├── requirements.txt        # Dependencias del proyecto
│
├── templates/              # Plantillas HTML
│   ├── header.html         # Navegación y encabezado
│   ├── footer.html         # Pie de página
│   ├── index.html          # Página principal
│   ├── post.html           # Vista de post individual
│   ├── make-post.html      # Crear/editar post
│   ├── register.html       # Registro de usuarios
│   ├── login.html          # Inicio de sesión
│   ├── about.html          # Página "Acerca de"
│   └── contact.html        # Página de contacto
│
├── static/                 # Archivos estáticos
│   ├── css/
│   │   └── styles.css      # Estilos personalizados
│   ├── js/
│   │   └── scripts.js      # JavaScript para navegación
│   └── assets/
│       └── img/            # Imágenes del blog
│
└── instance/              # Base de datos SQLite
    └── posts.db
```

---

## 🚀 Instalación y Configuración

### Paso 1: Requisitos Previos

Asegúrate de tener instalado:
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

Crea un archivo `requirements.txt` con el siguiente contenido:

```txt
Flask==3.0.0
Flask-Bootstrap==3.3.7.1
Flask-CKEditor==0.5.1
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
WTForms==3.1.1
python-dotenv==1.0.0
email-validator==2.1.0
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_super_segura_aqui_12345
```

**Nota**: Genera una clave secreta segura usando Python:
```python
import secrets
print(secrets.token_hex(32))
```

---

## 📝 Desarrollo Paso a Paso

### FASE 1: Configuración de Formularios (forms.py)

Primero creamos todos los formularios que usaremos en la aplicación.

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, Email, InputRequired, Length
from flask_ckeditor import CKEditorField


# ============================================================================
# FORM 1: Create Blog Post Form
# ============================================================================
# Purpose: Form to create or edit blog posts
# Used in: /new-post and /edit-post/<post_id> routes
class CreatePostForm(FlaskForm):
    """
    Form for creating or editing blog posts
    
    Fields:
        - title: Post title (required)
        - subtitle: Post subtitle (required)
        - img_url: Image URL for post header (required, must be valid URL)
        - body: Post content with rich text editor (required)
    """
    title = StringField(
        label="Blog Post Title", 
        validators=[DataRequired()]
    )
    subtitle = StringField(
        label="Subtitle", 
        validators=[DataRequired()]
    )
    img_url = StringField(
        label="Blog Image URL", 
        validators=[DataRequired(), URL()]
    )
    body = CKEditorField(
        label="Blog Content", 
        validators=[DataRequired()]
    )
    submit = SubmitField(label="Submit Post")


# ============================================================================
# FORM 2: User Registration Form
# ============================================================================
# Purpose: Form for new user registration
# Used in: /register route
class RegisterForm(FlaskForm):
    """
    Form for user registration
    
    Fields:
        - email: User email (required, must be valid email format)
        - password: User password (required, minimum 8 characters)
        - name: User full name (required)
    
    Validations:
        - Email must be unique (checked in route)
        - Password must be at least 8 characters
    """
    email = EmailField(
        label='Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        label='Password', 
        validators=[
            InputRequired(),
            Length(min=8, max=250, message='Password must be at least 8 characters long')
        ]
    )
    name = StringField(
        label='Name', 
        validators=[DataRequired()]
    )
    submit = SubmitField(label='SIGN ME UP!')


# ============================================================================
# FORM 3: User Login Form
# ============================================================================
# Purpose: Form for user authentication
# Used in: /login route
class LoginForm(FlaskForm):
    """
    Form for user login
    
    Fields:
        - email: User email (required, must be valid email format)
        - password: User password (required, minimum 8 characters)
    
    Note: Password is checked against hashed password in database
    """
    email = EmailField(
        label='Email', 
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        label='Password', 
        validators=[
            InputRequired(),
            Length(min=8, max=250, message='Password must be at least 8 characters long')
        ]
    )
    submit = SubmitField(label='LET ME IN!')


# ============================================================================
# FORM 4: Comment Form
# ============================================================================
# Purpose: Form for users to leave comments on blog posts
# Used in: /post/<post_id> route
class CommentForm(FlaskForm):
    """
    Form for submitting comments on blog posts
    
    Fields:
        - comment_text: Comment content with rich text editor (required)
    
    Note: User must be logged in to submit comments
    """
    comment_text = CKEditorField(
        label="Comment", 
        validators=[DataRequired()]
    )
    submit = SubmitField(label="Submit Comment")
```

---

### FASE 2: Configuración Principal y Base de Datos (main.py - Parte 1)

Ahora configuramos la aplicación Flask y los modelos de base de datos.

```python
# ============================================================================
# IMPORTS SECTION
# ============================================================================
import os
from datetime import date
from functools import wraps

from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
import hashlib

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column

from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from dotenv import load_dotenv
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm


# ============================================================================
# APPLICATION SETUP
# ============================================================================
# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Configure secret key for session management and CSRF protection
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize CKEditor for rich text editing
ckeditor = CKEditor(app)

# Initialize Bootstrap 5 for styling
Bootstrap5(app)


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
class Base(DeclarativeBase):
    """
    Base class for all database models
    Uses SQLAlchemy's declarative base
    """
    pass


# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# Initialize SQLAlchemy with custom base class
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# ============================================================================
# DATABASE MODELS
# ============================================================================

class User(db.Model, UserMixin):
    """
    User Model - Represents registered users in the blog
    
    Inherits from:
        - db.Model: SQLAlchemy database model
        - UserMixin: Flask-Login methods (is_authenticated, is_active, get_id)
    
    Relationships:
        - ONE User → MANY BlogPosts (via 'posts' attribute)
        - ONE User → MANY Comments (via 'comments' attribute)
    
    Methods:
        - avatar(size): Returns Gravatar URL for user's email
    
    Usage:
        # Create new user
        user = User(email="user@example.com", password="hashed_pw", name="John Doe")
        
        # Access user's posts
        user_posts = user.posts  # Returns list of BlogPost objects
        
        # Access user's comments
        user_comments = user.comments  # Returns list of Comment objects
    """
    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # User credentials and info
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationship: User → BlogPosts (one-to-many)
    # cascade="all, delete-orphan" means if user is deleted, all their posts are deleted
    posts: Mapped[list["BlogPost"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )

    # Relationship: User → Comments (one-to-many)
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="comment_author",
        cascade="all, delete-orphan"
    )

    def avatar(self, size=100):
        """
        Generate Gravatar avatar URL for this user
        
        Args:
            size (int): Size of avatar in pixels (default: 100)
        
        Returns:
            str: Gravatar URL for user's email
        """
        return gravatar_url(self.email, size=size)

    def __repr__(self):
        return f'<User: {self.name}>'


class BlogPost(db.Model):
    """
    BlogPost Model - Represents blog articles
    
    Relationships:
        - MANY BlogPosts → ONE User (each post has one author)
        - ONE BlogPost → MANY Comments (via 'comments' attribute)
    
    Usage:
        # Create new post
        post = BlogPost(
            title="My Post",
            author=user_object,
            subtitle="Subtitle",
            body="Content",
            img_url="https://image.url",
            date="January 1, 2024"
        )
        
        # Access post's author
        post_author = post.author  # Returns User object
        
        # Access post's comments
        post_comments = post.comments  # Returns list of Comment objects
    """
    __tablename__ = "blog_posts"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign key linking to User
    author_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("users.id"), 
        nullable=False
    )

    # Post content
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Relationship: BlogPost → User (many-to-one)
    author: Mapped["User"] = relationship(back_populates="posts")

    # Relationship: BlogPost → Comments (one-to-many)
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="parent_post",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<BlogPost: {self.title}>'


class Comment(db.Model):
    """
    Comment Model - Represents user comments on blog posts
    
    Relationships:
        - MANY Comments → ONE User (each comment has one author)
        - MANY Comments → ONE BlogPost (each comment belongs to one post)
    
    Usage:
        # Create new comment
        comment = Comment(
            text="Great post!",
            comment_author=user_object,
            parent_post=post_object
        )
        
        # Access comment's author
        comment_author = comment.comment_author  # Returns User object
        
        # Access comment's post
        comment_post = comment.parent_post  # Returns BlogPost object
    """
    __tablename__ = 'comments'

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign key 1: Links to User (comment author)
    author_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("users.id"), 
        nullable=False
    )

    # Foreign key 2: Links to BlogPost (which post is commented on)
    post_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey("blog_posts.id"), 
        nullable=False
    )

    # Relationship: Comment → User (many-to-one)
    comment_author: Mapped["User"] = relationship(back_populates="comments")

    # Relationship: Comment → BlogPost (many-to-one)
    parent_post: Mapped["BlogPost"] = relationship(back_populates="comments")

    # Comment content
    text: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        return f'<Comment by {self.comment_author.name} on {self.parent_post.title}>'


# Create all database tables
with app.app_context():
    db.create_all()
```

---

### FASE 3: Autenticación y Utilidades (main.py - Parte 2)

```python
# ============================================================================
# FLASK-LOGIN CONFIGURATION
# ============================================================================
# Create LoginManager instance for handling user sessions
login_manager = LoginManager()

# Initialize LoginManager with Flask app
login_manager.init_app(app)

# Configure login view (where to redirect if not logged in)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """
    User loader callback for Flask-Login
    
    Purpose:
        Flask-Login calls this function automatically on every request
        to load the current user from the session
    
    Args:
        user_id (str): The user's ID stored in the session cookie
    
    Returns:
        User object or None if user doesn't exist
    
    How it works:
        1. Flask-Login stores user_id in session when user logs in
        2. On each request, Flask-Login calls this function with user_id
        3. Function queries database and returns User object
        4. User object becomes available as 'current_user' in views
    """
    return db.session.get(User, int(user_id))


# ============================================================================
# GRAVATAR HELPER FUNCTION
# ============================================================================
def gravatar_url(email, size=50, default='retro', rating='g'):
    """
    Generate Gravatar URL from email address
    
    Purpose:
        Gravatar provides user avatars based on email addresses
        This function creates the URL to fetch those avatars
    
    Args:
        email (str): User's email address
        size (int): Image size in pixels (1-2048), default 50
        default (str): Default image style if no Gravatar exists
            Options: '404', 'mp', 'identicon', 'monsterid', 'wavatar',
                     'retro', 'robohash', 'blank'
        rating (str): Content rating - 'g', 'pg', 'r', 'x'
    
    Returns:
        str: Gravatar image URL
    
    How it works:
        1. Convert email to lowercase and remove whitespace
        2. Create MD5 hash of email
        3. Build Gravatar URL with hash and parameters
    
    Example:
        gravatar_url("user@example.com", size=100)
        # Returns: "https://www.gravatar.com/avatar/abc123...?s=100&d=retro&r=g"
    """
    # Create MD5 hash of lowercase, stripped email
    email_hash = hashlib.md5(email.lower().strip().encode('utf-8')).hexdigest()
    
    # Build and return Gravatar URL with parameters
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d={default}&r={rating}"


# Make gravatar_url available in all Jinja templates
app.jinja_env.globals['gravatar'] = gravatar_url


# ============================================================================
# CUSTOM DECORATORS
# ============================================================================
def admin_only(f):
    """
    Decorator to restrict routes to admin users only
    
    Purpose:
        Protects routes that should only be accessible by admin (user ID 1)
        If non-admin tries to access, returns 403 Forbidden error
    
    Usage:
        @app.route('/admin-page')
        @admin_only
        def admin_page():
            return "Admin content"
    
    How it works:
        1. Check if current user's ID is 1 (admin)
        2. If not admin, abort with 403 error
        3. If admin, execute the wrapped function
    
    Note:
        First registered user (ID=1) is automatically admin
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Check if current user is admin (ID = 1)
        if current_user.id != 1:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return wrapper
```

---

### FASE 4: Rutas de Autenticación (main.py - Parte 3)

```python
# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    User Registration Route
    
    Purpose:
        Allows new users to create an account
    
    Methods:
        GET: Display registration form
        POST: Process registration form submission
    
    Process:
        1. Display RegisterForm
        2. When form submitted:
           a. Get email, name, password from form
           b. Hash password using Werkzeug
           c. Check if email already exists
           d. If exists: flash error, redirect to login
           e. If new: create user, save to DB, log them in
        3. Redirect to homepage
    
    Security:
        - Password is hashed before storing (never store plain text!)
        - Uses pbkdf2:sha256 algorithm with 8-byte salt
        - Email uniqueness is enforced at DB level
    """
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Extract form data
        email = form.email.data
        name = form.name.data
        password = form.password.data
        
        # Hash password for secure storage
        # pbkdf2:sha256 = Password-Based Key Derivation Function 2 with SHA-256
        # salt_length=8 = adds random 8-byte salt to prevent rainbow table attacks
        password_hashed = generate_password_hash(
            password=password,
            method="pbkdf2:sha256",
            salt_length=8
        )
        
        # Check if email already exists
        user = db.session.scalar(
            db.select(User).where(User.email == email)
        )
        
        if user:
            # Email already registered
            flash(
                message="You've already signed up with that email, log in instead!", 
                category="error"
            )
            return redirect(url_for('login'))
        
        # Create new user
        new_user = User(
            email=email,
            password=password_hashed,
            name=name,
        )
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        # Log user in automatically after registration
        login_user(new_user)
        
        return redirect(url_for('get_all_posts'))
    
    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    User Login Route
    
    Purpose:
        Authenticates existing users
    
    Methods:
        GET: Display login form
        POST: Process login attempt
    
    Process:
        1. Display LoginForm
        2. When form submitted:
           a. Get email and password from form
           b. Query database for user with that email
           c. If user doesn't exist: flash error
           d. If password wrong: flash error
           e. If credentials valid: log user in, redirect to homepage
    
    Security:
        - Password is compared using check_password_hash()
        - This safely compares hashed passwords
        - Never compares plain text passwords
    """
    form = LoginForm()
    
    if form.validate_on_submit():
        # Extract form data
        provided_email = form.email.data
        provided_password = form.password.data
        
        # Query database for user
        user = db.session.scalar(
            db.select(User).where(User.email == provided_email)
        )
        
        # Check if user exists
        if not user:
            flash(
                message='That email does not exist, please try again', 
                category='error'
            )
            return redirect(url_for('login'))
        
        # Check if password is correct
        elif not check_password_hash(user.password, provided_password):
            flash(
                message='Password incorrect, please try again.', 
                category='error'
            )
            return redirect(url_for('login'))
        
        # Credentials are valid - log user in
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    """
    User Logout Route
    
    Purpose:
        Logs out the current user and clears their session
    
    Process:
        1. Call logout_user() to clear session
        2. Redirect to homepage
    
    Note:
        User can be logged out from any page
        No login required to access this route
    """
    logout_user()
    return redirect(url_for('get_all_posts'))
```

---

### FASE 5: Rutas del Blog (main.py - Parte 4)

```python
# ============================================================================
# BLOG ROUTES
# ============================================================================

@app.route('/')
def get_all_posts():
    """
    Homepage Route - Display all blog posts
    
    Purpose:
        Shows list of all published blog posts
    
    Process:
        1. Query all blog posts from database
        2. Pass posts to template
        3. Template displays posts with:
           - Title, subtitle, author, date
           - Delete button (only visible to admin)
           - Link to full post
    
    Available to: Everyone (no login required)
    """
    # Query all blog posts
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):
    """
    Individual Post Route - Display single post with comments
    
    Purpose:
        Shows full blog post content and allows users to comment
    
    Methods:
        GET: Display post and comments
        POST: Process new comment submission
    
    Args:
        post_id (int): ID of the post to display
    
    Process:
        GET:
            1. Query post by ID (or 404 if not found)
            2. Display post content
            3. Show all comments with Gravatar avatars
            4. Show comment form (if user logged in)
        
        POST (submit comment):
            1. Check if user is logged in
            2. If not: flash error, redirect to login
            3. If yes: create comment, save to DB
            4. Redirect back to post page
    
    Available to:
        - View: Everyone
        - Comment: Logged-in users only
    """
    # Get post or return 404 if not found
    requested_post = db.get_or_404(BlogPost, post_id)
    
    # Create comment form
    comment_form = CommentForm()
    
    # Process comment submission
    if comment_form.validate_on_submit():
        # Check if user is logged in
        if not current_user.is_authenticated:
            flash(
                message='You need to login or register to comment.', 
                category='error'
            )
            return redirect(url_for('login'))
        
        # Create new comment
        new_comment = Comment(
            text=comment_form.comment_text.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        
        # Save to database
        db.session.add(new_comment)
        db.session.commit()
        
        flash(message='Comment added successfully!', category='success')
        
        return redirect(url_for('show_post', post_id=post_id))
    
    return render_template(
        "post.html",
        post=requested_post,
        form=comment_form
    )


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    """
    Create New Post Route - Only admin can access
    
    Purpose:
        Allows admin to create new blog posts
    
    Methods:
        GET: Display post creation form
        POST: Process new post submission
    
    Process:
        1. Display CreatePostForm
        2. When form submitted:
           a. Get title, subtitle, body, image URL from form
           b. Create new BlogPost with current user as author
           c. Add current date automatically
           d. Save to database
           e. Redirect to homepage
    
    Available to: Admin only (user ID = 1)
    Decorator: @admin_only (returns 403 if not admin)
    """
    form = CreatePostForm()
    
    if form.validate_on_submit():
        # Create new post
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")  # Format: "January 01, 2024"
        )
        
        # Save to database
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for("get_all_posts"))
    
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    """
    Edit Post Route - Only admin can access
    
    Purpose:
        Allows admin to edit existing blog posts
    
    Methods:
        GET: Display post edit form with current values
        POST: Process post update
    
    Args:
        post_id (int): ID of the post to edit
    
    Process:
        GET:
            1. Query post by ID (or 404 if not found)
            2. Pre-fill form with current post values
            3. Display form
        
        POST:
            1. Get updated values from form
            2. Update post object
            3. Save changes to database
            4. Redirect to updated post page
    
    Available to: Admin only (user ID = 1)
    Decorator: @admin_only (returns 403 if not admin)
    """
    # Get post or return 404
    post = db.get_or_404(BlogPost, post_id)
    
    # Pre-fill form with current values
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    
    if edit_form.validate_on_submit():
        # Update post with new values
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        
        # Save changes
        db.session.commit()
        
        return redirect(url_for("show_post", post_id=post.id))
    
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    """
    Delete Post Route - Only admin can access
    
    Purpose:
        Allows admin to delete blog posts
    
    Args:
        post_id (int): ID of the post to delete
    
    Process:
        1. Query post by ID (or 404 if not found)
        2. Delete post from database
        3. All associated comments are automatically deleted (cascade)
        4. Redirect to homepage
    
    Available to: Admin only (user ID = 1)
    Decorator: @admin_only (returns 403 if not admin)
    
    Note:
        Due to cascade="all, delete-orphan" in relationships,
        deleting a post automatically deletes all its comments
    """
    # Get post or return 404
    post_to_delete = db.get_or_404(BlogPost, post_id)
    
    # Delete from database
    db.session.delete(post_to_delete)
    db.session.commit()
    
    return redirect(url_for('get_all_posts'))


# ============================================================================
# STATIC PAGES ROUTES
# ============================================================================

@app.route("/about")
def about():
    """
    About Page Route
    
    Purpose:
        Displays information about the blog/author
    
    Available to: Everyone
    """
    return render_template("about.html")


@app.route("/contact")
def contact():
    """
    Contact Page Route
    
    Purpose:
        Displays contact information or contact form
    
    Available to: Everyone
    
    Note:
        Currently just displays page
        Could be extended to handle form submissions
    """
    return render_template("contact.html")


# ============================================================================
# RUN APPLICATION
# ============================================================================
if __name__ == "__main__":
    app.run(debug=True, port=5002)
```

---

## 🎨 Archivos Frontend

### header.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <meta name="description" content="" />
    <meta name="author" content="" />
    <title>Jesus's Blog</title>
    
    {% block styles %}
    {# Load Bootstrap-Flask CSS #}
    {{ bootstrap.load_css() }}
    
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='assets/favicon.ico') }}" />
    
    {# Font Awesome icons #}
    <script src="https://use.fontawesome.com/releases/v6.3.0/js/all.js" crossorigin="anonymous"></script>
    
    {# Google fonts #}
    <link href="https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic" rel="stylesheet" type="text/css" />
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800" rel="stylesheet" type="text/css" />
    
    {# Custom CSS #}
    <link href="{{ url_for('static', filename='css/styles.css') }}" rel="stylesheet" />
    {% endblock %}
</head>
<body>
    {# Navigation Bar #}
    <nav class="navbar navbar-expand-lg navbar-light" id="mainNav">
        <div class="container px-4 px-lg-5">
            <a class="navbar-brand" href="/">Start Bootstrap</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                Menu
                <i class="fas fa-bars"></i>
            </button>
            <div class="collapse navbar-collapse" id="navbarResponsive">
                <ul class="navbar-nav ms-auto py-4 py-lg-0">
                    {# Home link #}
                    <li class="nav-item">
                        <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('get_all_posts') }}">
                            Home
                        </a>
                    </li>

                    {# Conditional navigation based on authentication #}
                    {% if not current_user.is_authenticated %}
                        {# Login link - only show to logged out users #}
                        <li class="nav-item">
                            <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('login') }}">
                                Login
                            </a>
                        </li>

                        {# Register link - only show to logged out users #}
                        <li class="nav-item">
                            <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('register') }}">
                                Register
                            </a>
                        </li>
                    {% else %}
                        {# Logout link - only show to logged in users #}
                        <li class="nav-item">
                            <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('logout') }}">
                                Log Out
                            </a>
                        </li>
                    {% endif %}

                    {# About link #}
                    <li class="nav-item">
                        <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('about') }}">
                            About
                        </a>
                    </li>

                    {# Contact link #}
                    <li class="nav-item">
                        <a class="nav-link px-lg-3 py-3 py-lg-4" href="{{ url_for('contact') }}">
                            Contact
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</body>
</html>
```

### scripts.js

```javascript
/*!
 * Navigation scroll behavior
 * Purpose: Makes navigation bar sticky on scroll
 */
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        
        if (currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove('is-visible');
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
});
```

---

## ⚙️ Funcionalidades Principales

### 1. Sistema de Autenticación

**Registro**:
- Validación de email
- Hash de contraseñas con Werkzeug
- Verificación de email único
- Login automático después del registro

**Login**:
- Verificación de credenciales
- Mensajes de error amigables
- Sesiones persistentes

### 2. Gestión de Posts

**Solo Admin puede**:
- Crear nuevos posts
- Editar posts existentes
- Eliminar posts
- Ver botones de acción en la interfaz

**Todos pueden**:
- Ver lista de posts
- Leer posts completos
- Ver comentarios

### 3. Sistema de Comentarios

**Características**:
- Usuarios autenticados pueden comentar
- Editor de texto enriquecido (CKEditor)
- Avatares Gravatar automáticos
- Relación usuario-comentario-post

### 4. Permisos y Seguridad

**Niveles de acceso**:
- **Visitante**: Ver posts y comentarios
- **Usuario registrado**: Todo lo anterior + comentar
- **Admin (ID=1)**: Todo lo anterior + CRUD de posts

---

## 🚦 Cómo Ejecutar el Proyecto

### 1. Iniciar el servidor

```bash
# Asegúrate de estar en el entorno virtual
python main.py
```

### 2. Acceder a la aplicación

Abre tu navegador en: `http://localhost:5002`

### 3. Crear cuenta de administrador

El **primer usuario** que se registre tendrá ID=1 y será el administrador automáticamente.

---

## 📚 Conceptos Clave Explicados

### ¿Qué es ORM (Object-Relational Mapping)?

SQLAlchemy es un ORM que te permite trabajar con bases de datos usando objetos Python en lugar de SQL puro.

**En lugar de escribir**:
```sql
SELECT * FROM users WHERE email = 'user@example.com';
```

**Escribes**:
```python
user = db.session.scalar(db.select(User).where(User.email == email))
```

### ¿Qué son las Relaciones?

Las relaciones conectan tablas entre sí:

**One-to-Many** (Uno a Muchos):
- Un usuario puede tener muchos posts
- `User.posts` → lista de BlogPost

**Many-to-One** (Muchos a Uno):
- Muchos posts pertenecen a un usuario
- `BlogPost.author` → objeto User

### ¿Qué es el Hash de Contraseñas?

**Nunca guardes contraseñas en texto plano**. El hash convierte la contraseña en un string irreversible:

```python
# Password: "mipassword123"
# Hashed: "pbkdf2:sha256:600000$abc...xyz"
```

Para verificar:
```python
check_password_hash(hashed_password, provided_password)  # True/False
```

### ¿Qué son los Decoradores?

Los decoradores modifican el comportamiento de funciones:

```python
@admin_only
def delete_post():
    # Solo admin puede ejecutar esto
```

### ¿Qué es Flask-Login?

Gestiona sesiones de usuarios automáticamente:
- `current_user`: Usuario actual en cualquier vista
- `@login_required`: Protege rutas
- `login_user()`: Inicia sesión
- `logout_user()`: Cierra sesión

---

## 🐛 Solución de Problemas Comunes

### Error: "SECRET_KEY not found"
```bash
# Solución: Crea archivo .env con:
SECRET_KEY=tu_clave_secreta_aqui
```

### Error: "No module named 'flask'"
```bash
# Solución: Instala dependencias
pip install -r requirements.txt
```

### Error: "Database doesn't exist"
```python
# Solución: Crea las tablas
with app.app_context():
    db.create_all()
```

### No puedo editar/eliminar posts
**Solución**: Solo el usuario con ID=1 (admin) puede hacerlo. Registra la primera cuenta.

---

## 🎯 Próximos Pasos para Mejorar

1. **Paginación**: Mostrar solo 10 posts por página
2. **Búsqueda**: Agregar barra de búsqueda de posts
3. **Categorías**: Organizar posts por categorías
4. **Likes**: Sistema de "me gusta" en posts
5. **Imágenes**: Subir imágenes en lugar de URLs
6. **Email**: Enviar email de verificación al registrarse
7. **Perfil**: Página de perfil de usuario
8. **Respuestas**: Responder a comentarios específicos

---

## 📝 Comandos Útiles

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Mac/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Generar SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Ejecutar aplicación
python main.py

# Desactivar entorno virtual
deactivate
```

---

## 🤝 Contribuir

Si quieres mejorar este proyecto:
1. Haz fork del repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@example.com

---

## 🙏 Agradecimientos

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Start Bootstrap - Clean Blog](https://startbootstrap.com/theme/clean-blog)
- [Gravatar](https://gravatar.com/)

---

## 📞 Soporte

Si tienes preguntas o problemas:
1. Revisa la sección [Solución de Problemas](#solución-de-problemas-comunes)
2. Abre un Issue en GitHub
3. Contacta al autor

---

**¡Feliz Coding! 🚀**