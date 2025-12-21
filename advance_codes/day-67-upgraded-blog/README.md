# Guía Completa de WTForms con Flask-WTF

## 📋 Tabla de Contenidos
1. [Instalación](#instalación)
2. [Configuración Básica](#configuración-básica)
3. [Tipos de Campos (Fields)](#tipos-de-campos-fields)
4. [Validadores (Validators)](#validadores-validators)
5. [Ejemplo Completo: Formulario de Blog Post](#ejemplo-completo-formulario-de-blog-post)
6. [Renderizado en Templates](#renderizado-en-templates)
7. [Manejo de Datos](#manejo-de-datos)

---

## Instalación

```bash
pip install Flask-WTF
pip install WTForms
pip install Flask-CKEditor  # Para editor de texto enriquecido
pip install email-validator  # Para validación de emails
```

---

## Configuración Básica

```python
from flask import Flask
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'  # Required for CSRF protection
```

---

## Tipos de Campos (Fields)

### 1. Campos de Texto

| Campo | Descripción | Uso |
|-------|-------------|-----|
| `StringField` | Campo de texto simple (input text) | Nombres, títulos, URLs |
| `TextAreaField` | Campo de texto multilínea (textarea) | Descripciones, comentarios |
| `PasswordField` | Campo de contraseña (oculta texto) | Passwords |
| `EmailField` | Campo específico para emails | Correos electrónicos |
| `TelField` | Campo para números telefónicos | Teléfonos |
| `SearchField` | Campo de búsqueda | Buscadores |
| `URLField` | Campo específico para URLs | Enlaces web |

**Ejemplo:**
```python
from wtforms import StringField, TextAreaField, PasswordField, EmailField

class MyForm(FlaskForm):
    title = StringField('Title')
    description = TextAreaField('Description')
    password = PasswordField('Password')
    email = EmailField('Email')
    website = URLField('Website URL')
```

### 2. Campos Numéricos

| Campo | Descripción | Tipo de Dato |
|-------|-------------|--------------|
| `IntegerField` | Números enteros | int |
| `FloatField` | Números decimales | float |
| `DecimalField` | Números decimales precisos | Decimal |

**Ejemplo:**
```python
from wtforms import IntegerField, FloatField, DecimalField

class ProductForm(FlaskForm):
    quantity = IntegerField('Quantity')
    price = FloatField('Price')
    precise_price = DecimalField('Precise Price', places=2)
```

### 3. Campos de Selección

| Campo | Descripción | Uso |
|-------|-------------|-----|
| `SelectField` | Lista desplegable (dropdown) | Opciones predefinidas |
| `RadioField` | Botones de radio (selección única) | Opciones visibles |
| `SelectMultipleField` | Selección múltiple | Varias opciones |

**Ejemplo:**
```python
from wtforms import SelectField, RadioField, SelectMultipleField

class PreferencesForm(FlaskForm):
    # Dropdown list
    country = SelectField('Country', choices=[
        ('us', 'United States'),
        ('uk', 'United Kingdom'),
        ('ca', 'Canada')
    ])
    
    # Radio buttons
    gender = RadioField('Gender', choices=[
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ])
    
    # Multiple selection
    interests = SelectMultipleField('Interests', choices=[
        ('tech', 'Technology'),
        ('sports', 'Sports'),
        ('music', 'Music')
    ])
```

### 4. Campos Booleanos

| Campo | Descripción | Uso |
|-------|-------------|-----|
| `BooleanField` | Checkbox simple | Términos y condiciones, opciones |

**Ejemplo:**
```python
from wtforms import BooleanField

class RegisterForm(FlaskForm):
    accept_terms = BooleanField('I accept the terms and conditions')
    newsletter = BooleanField('Subscribe to newsletter')
```

### 5. Campos de Fecha y Hora

| Campo | Descripción | Formato |
|-------|-------------|---------|
| `DateField` | Campo de fecha | datetime.date |
| `DateTimeField` | Fecha y hora | datetime.datetime |
| `TimeField` | Solo hora | datetime.time |

**Ejemplo:**
```python
from wtforms import DateField, DateTimeField, TimeField

class EventForm(FlaskForm):
    event_date = DateField('Event Date', format='%Y-%m-%d')
    event_datetime = DateTimeField('Event Date & Time', format='%Y-%m-%d %H:%M:%S')
    event_time = TimeField('Event Time')
```

### 6. Campos de Archivos

| Campo | Descripción | Uso |
|-------|-------------|-----|
| `FileField` | Subir un archivo | Imágenes, documentos |
| `MultipleFileField` | Subir múltiples archivos | Galería de imágenes |

**Ejemplo:**
```python
from wtforms import FileField, MultipleFileField
from flask_wtf.file import FileAllowed

class UploadForm(FlaskForm):
    photo = FileField('Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    documents = MultipleFileField('Documents')
```

### 7. Campos Especiales

| Campo | Descripción | Uso |
|-------|-------------|-----|
| `HiddenField` | Campo oculto | Datos que no se muestran al usuario |
| `SubmitField` | Botón de envío | Submit button |
| `CKEditorField` | Editor WYSIWYG | Contenido HTML enriquecido |

**Ejemplo:**
```python
from wtforms import HiddenField, SubmitField
from flask_ckeditor import CKEditorField

class BlogPostForm(FlaskForm):
    user_id = HiddenField('User ID')
    content = CKEditorField('Content')
    submit = SubmitField('Publish Post')
```

---

## Validadores (Validators)

### 1. Validadores Básicos

| Validador | Descripción | Ejemplo |
|-----------|-------------|---------|
| `DataRequired()` | Campo obligatorio | `validators=[DataRequired()]` |
| `Optional()` | Campo opcional (permite vacío) | `validators=[Optional()]` |
| `InputRequired()` | Requiere input (permite cadena vacía) | `validators=[InputRequired()]` |

**Ejemplo:**
```python
from wtforms.validators import DataRequired, Optional, InputRequired

class MyForm(FlaskForm):
    # Field cannot be empty
    name = StringField('Name', validators=[DataRequired(message='Name is required')])
    
    # Field is optional
    nickname = StringField('Nickname', validators=[Optional()])
    
    # Field must receive input (even if empty string)
    comment = StringField('Comment', validators=[InputRequired()])
```

### 2. Validadores de Longitud

| Validador | Descripción | Parámetros |
|-----------|-------------|------------|
| `Length(min, max)` | Longitud de caracteres | min, max, message |

**Ejemplo:**
```python
from wtforms.validators import Length

class UserForm(FlaskForm):
    # Minimum 3 characters
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, message='Username must be at least 3 characters')
    ])
    
    # Between 8 and 20 characters
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=20, message='Password must be between 8 and 20 characters')
    ])
    
    # Maximum 200 characters
    bio = TextAreaField('Bio', validators=[
        Length(max=200, message='Bio cannot exceed 200 characters')
    ])
```

### 3. Validadores de Números

| Validador | Descripción | Parámetros |
|-----------|-------------|------------|
| `NumberRange(min, max)` | Rango de números | min, max, message |

**Ejemplo:**
```python
from wtforms.validators import NumberRange

class ProductForm(FlaskForm):
    # Must be between 1 and 100
    quantity = IntegerField('Quantity', validators=[
        DataRequired(),
        NumberRange(min=1, max=100, message='Quantity must be between 1 and 100')
    ])
    
    # Must be greater than 0
    price = FloatField('Price', validators=[
        DataRequired(),
        NumberRange(min=0.01, message='Price must be greater than 0')
    ])
    
    # Age must be between 18 and 120
    age = IntegerField('Age', validators=[
        NumberRange(min=18, max=120, message='Age must be between 18 and 120')
    ])
```

### 4. Validadores de Formato

| Validador | Descripción | Uso |
|-----------|-------------|-----|
| `Email()` | Valida formato de email | Correos electrónicos |
| `URL()` | Valida formato de URL | Enlaces web |
| `Regexp(regex)` | Expresión regular personalizada | Patrones específicos |
| `MacAddress()` | Valida dirección MAC | Direcciones MAC |
| `UUID()` | Valida formato UUID | Identificadores únicos |

**Ejemplo:**
```python
from wtforms.validators import Email, URL, Regexp

class ContactForm(FlaskForm):
    # Validate email format
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    
    # Validate URL format
    website = URLField('Website', validators=[
        DataRequired(),
        URL(message='Invalid URL')
    ])
    
    # Validate phone number format (US)
    phone = StringField('Phone', validators=[
        Regexp(r'^\d{3}-\d{3}-\d{4}$', message='Phone must be in format: 123-456-7890')
    ])
    
    # Validate username (only letters, numbers, underscore)
    username = StringField('Username', validators=[
        Regexp(r'^[a-zA-Z0-9_]+$', message='Username can only contain letters, numbers and underscore')
    ])
```

### 5. Validadores de Comparación

| Validador | Descripción | Uso |
|-----------|-------------|-----|
| `EqualTo(fieldname)` | Debe ser igual a otro campo | Confirmación de contraseña |

**Ejemplo:**
```python
from wtforms.validators import EqualTo

class RegisterForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8)
    ])
    
    # Must match password field
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
```

### 6. Validadores de Selección

| Validador | Descripción | Uso |
|-----------|-------------|-----|
| `AnyOf(values)` | Debe ser uno de los valores | Opciones válidas |
| `NoneOf(values)` | No puede ser ninguno de los valores | Valores prohibidos |

**Ejemplo:**
```python
from wtforms.validators import AnyOf, NoneOf

class PreferencesForm(FlaskForm):
    # Must be one of these values
    theme = SelectField('Theme', validators=[
        AnyOf(['light', 'dark', 'auto'], message='Invalid theme selected')
    ])
    
    # Cannot be any of these values
    username = StringField('Username', validators=[
        NoneOf(['admin', 'root', 'system'], message='This username is reserved')
    ])
```

### 7. Validadores de Archivos

| Validador | Descripción | Parámetros |
|-----------|-------------|------------|
| `FileRequired()` | Archivo obligatorio | message |
| `FileAllowed(extensions)` | Extensiones permitidas | upload_set, message |
| `FileSize(max_size)` | Tamaño máximo de archivo | max_size, message |

**Ejemplo:**
```python
from flask_wtf.file import FileRequired, FileAllowed, FileSize

class UploadForm(FlaskForm):
    # File is required
    document = FileField('Document', validators=[
        FileRequired(message='Please select a file')
    ])
    
    # Only specific extensions allowed
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png', 'gif'], message='Only images are allowed (jpg, png, gif)')
    ])
    
    # Maximum file size: 2MB
    avatar = FileField('Avatar', validators=[
        FileSize(max_size=2097152, message='File size cannot exceed 2MB')
    ])
```

### 8. Validador Personalizado

```python
from wtforms.validators import ValidationError

def validate_username_custom(form, field):
    """Custom validator to check if username is available"""
    forbidden_usernames = ['admin', 'root', 'superuser']
    if field.data.lower() in forbidden_usernames:
        raise ValidationError('This username is not available')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        validate_username_custom  # Custom validator
    ])
```

---

## Ejemplo Completo: Formulario de Blog Post

### Paso 1: Crear el Formulario

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL, Length
from flask_ckeditor import CKEditorField

class CreatePostForm(FlaskForm):
    """Form for creating a new blog post"""
    
    # Post title (required, max 250 characters)
    title = StringField(
        'Blog Post Title',
        validators=[
            DataRequired(message='Title is required'),
            Length(max=250, message='Title cannot exceed 250 characters')
        ]
    )
    
    # Post subtitle (required, max 250 characters)
    subtitle = StringField(
        'Subtitle',
        validators=[
            DataRequired(message='Subtitle is required'),
            Length(max=250, message='Subtitle cannot exceed 250 characters')
        ]
    )
    
    # Author name (required)
    author = StringField(
        'Your Name',
        validators=[
            DataRequired(message='Author name is required'),
            Length(min=2, max=100, message='Author name must be between 2 and 100 characters')
        ]
    )
    
    # Image URL (required, must be valid URL)
    img_url = StringField(
        'Blog Image URL',
        validators=[
            DataRequired(message='Image URL is required'),
            URL(message='Please enter a valid URL')
        ]
    )
    
    # Blog content with rich text editor (required)
    body = CKEditorField(
        'Blog Content',
        validators=[
            DataRequired(message='Blog content is required')
        ]
    )
    
    # Submit button
    submit = SubmitField('Submit Post')
```

### Paso 2: Configurar la Aplicación Flask

```python
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_ckeditor import CKEditor
from datetime import date

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Initialize CKEditor
ckeditor = CKEditor(app)

# Initialize Bootstrap
Bootstrap5(app)

# Create database
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Configure table
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()
```

### Paso 3: Crear la Ruta

```python
@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    """Route to create a new blog post"""
    form = CreatePostForm()
    
    # Validate form on submission
    if form.validate_on_submit():
        # Create new post instance
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=form.author.data,
            date=date.today().strftime("%B %d, %Y")
        )
        
        # Add to database
        db.session.add(new_post)
        db.session.commit()
        
        # Redirect to home page
        return redirect(url_for('get_all_posts'))
    
    # Render template with form
    return render_template('make-post.html', form=form)
```

---

## Renderizado en Templates

### Método 1: Bootstrap-Flask (Recomendado)

```html
{% extends 'bootstrap/base.html' %}
{% from 'bootstrap5/form.html' import render_form %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
            <h1>New Post</h1>
            
            <!-- Render entire form automatically -->
            {{ render_form(form, novalidate=True, button_map={"submit": "primary"}) }}
        </div>
    </div>
</div>
{% endblock %}
```

### Método 2: CKEditor Manual

```html
{% extends 'bootstrap/base.html' %}
{% from 'bootstrap5/form.html' import render_field %}

{% block styles %}
{{ super() }}
{{ ckeditor.load() }}
{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
            <h1>New Post</h1>
            
            <form method="POST" action="" novalidate>
                {{ form.hidden_tag() }}  <!-- CSRF protection -->
                
                <!-- Title field -->
                {{ render_field(form.title, class="form-control") }}
                
                <!-- Subtitle field -->
                {{ render_field(form.subtitle, class="form-control") }}
                
                <!-- Author field -->
                {{ render_field(form.author, class="form-control") }}
                
                <!-- Image URL field -->
                {{ render_field(form.img_url, class="form-control") }}
                
                <!-- Body field with CKEditor -->
                {{ render_field(form.body, class="form-control") }}
                
                <!-- Submit button -->
                {{ render_field(form.submit, class="btn btn-primary btn-block") }}
            </form>
        </div>
    </div>
</div>

{% block scripts %}
{{ super() }}
{{ ckeditor.load() }}
{{ ckeditor.config(name='body') }}
{% endblock %}
{% endblock %}
```

### Método 3: Renderizado Manual Completo

```html
<form method="POST" action="{{ url_for('add_new_post') }}" novalidate>
    {{ form.hidden_tag() }}
    
    <div class="form-group">
        {{ form.title.label(class="form-label") }}
        {{ form.title(class="form-control", placeholder="Enter post title") }}
        
        <!-- Show validation errors -->
        {% if form.title.errors %}
            <div class="invalid-feedback d-block">
                {% for error in form.title.errors %}
                    <span>{{ error }}</span>
                {% endfor %}
            </div>
        {% endif %}
    </div>
    
    <div class="form-group">
        {{ form.subtitle.label(class="form-label") }}
        {{ form.subtitle(class="form-control") }}
        {% if form.subtitle.errors %}
            <div class="invalid-feedback d-block">
                {% for error in form.subtitle.errors %}
                    <span>{{ error }}</span>
                {% endfor %}
            </div>
        {% endif %}
    </div>
    
    <!-- Repeat for other fields... -->
    
    <div class="form-group">
        {{ form.submit(class="btn btn-primary") }}
    </div>
</form>
```

---

## Manejo de Datos

### Acceder a los Datos del Formulario

```python
@app.route('/new-post', methods=['GET', 'POST'])
def add_new_post():
    form = CreatePostForm()
    
    if form.validate_on_submit():
        # Access form data
        title = form.title.data
        subtitle = form.subtitle.data
        author = form.author.data
        img_url = form.img_url.data
        body = form.body.data
        
        print(f"Title: {title}")
        print(f"Author: {author}")
        
        # Process data...
        return redirect(url_for('success'))
    
    return render_template('make-post.html', form=form)
```

### Pre-llenar Formulario con Datos Existentes

```python
@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    
    # Pre-fill form with existing data
    form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        author=post.author,
        img_url=post.img_url,
        body=post.body
    )
    
    if form.validate_on_submit():
        # Update post with new data
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.author = form.author.data
        post.img_url = form.img_url.data
        post.body = form.body.data
        
        db.session.commit()
        return redirect(url_for('show_post', post_id=post.id))
    
    return render_template('make-post.html', form=form, is_edit=True)
```

### Validación Manual

```python
@app.route('/manual-validation', methods=['POST'])
def manual_validation():
    form = CreatePostForm()
    
    # Manual validation
    if not form.validate():
        # Get all errors
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
        
        return render_template('make-post.html', form=form)
    
    # Process valid data
    return redirect(url_for('success'))
```

---

## Tips y Mejores Prácticas

### 1. Siempre usar CSRF Protection
```python
app.config['SECRET_KEY'] = 'tu-clave-secreta-muy-segura'
```

### 2. Mensajes de Error Personalizados
```python
title = StringField('Title', validators=[
    DataRequired(message='Por favor ingresa un título'),
    Length(max=250, message='El título no puede exceder 250 caracteres')
])
```

### 3. Validadores Múltiples
```python
username = StringField('Username', validators=[
    DataRequired(),
    Length(min=3, max=20),
    Regexp(r'^[a-zA-Z0-9_]+$')
])
```

### 4. Campos Opcionales con Validación Condicional
```python
website = URLField('Website', validators=[
    Optional(),  # Field is optional
    URL()  # But if provided, must be valid URL
])
```

### 5. Deshabilitar Validación HTML5
```html
<form method="POST" novalidate>
    <!-- novalidate prevents browser validation, uses WTForms validation only -->
</form>
```

---

## Recursos Adicionales

- **Documentación Oficial de WTForms:** https://wtforms.readthedocs.io/
- **Flask-WTF Documentation:** https://flask-wtf.readthedocs.io/
- **Flask-CKEditor:** https://flask-ckeditor.readthedocs.io/
- **Bootstrap-Flask:** https://bootstrap-flask.readthedocs.io/

---

## Resumen Rápido

| Necesidad | Campo | Validador |
|-----------|-------|-----------|
| Texto corto obligatorio | `StringField` | `DataRequired()` |
| Texto largo | `TextAreaField` | `DataRequired()` |
| Email válido | `EmailField` | `Email()` |
| URL válida | `URLField` | `URL()` |
| Número entero | `IntegerField` | `NumberRange()` |
| Contraseña | `PasswordField` | `Length(min=8)` |
| Editor rico | `CKEditorField` | `DataRequired()` |
| Checkbox | `BooleanField` | - |
| Lista desplegable | `SelectField` | `DataRequired()` |
| Subir archivo | `FileField` | `FileAllowed()` |

---

**¡Guarda este README para referencia futura!** 🚀