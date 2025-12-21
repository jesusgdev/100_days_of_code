# Guía Completa: Flask-Login

## 📋 Tabla de Contenidos
1. [¿Qué es Flask-Login?](#qué-es-flask-login)
2. [Instalación](#instalación)
3. [Conceptos Fundamentales](#conceptos-fundamentales)
4. [Configuración Básica](#configuración-básica)
5. [Modelo de Usuario](#modelo-de-usuario)
6. [Funciones Principales](#funciones-principales)
7. [Decoradores](#decoradores)
8. [Sistema Completo de Autenticación](#sistema-completo-de-autenticación)
9. [Características Avanzadas](#características-avanzadas)
10. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## ¿Qué es Flask-Login?

**Flask-Login** es una extensión de Flask que maneja las sesiones de usuario de manera sencilla y segura.

### ¿Qué problemas resuelve?

Sin Flask-Login tendrías que:
- ❌ Manejar sesiones manualmente con `session['user_id']`
- ❌ Escribir código repetitivo para verificar si el usuario está logueado
- ❌ Crear decoradores personalizados para proteger rutas
- ❌ Gestionar "remember me" manualmente

Con Flask-Login:
- ✅ Maneja sesiones automáticamente
- ✅ Proporciona decorador `@login_required` listo para usar
- ✅ Incluye funcionalidad "remember me"
- ✅ Gestiona usuarios activos/anónimos
- ✅ Proporciona funciones útiles como `current_user`

---

## Instalación

```bash
# Install Flask-Login
pip install flask-login

# Usually you also need these
pip install Flask
pip install Flask-SQLAlchemy
pip install Werkzeug
```

---

## Conceptos Fundamentales

### 1. LoginManager
Es el **cerebro** de Flask-Login. Coordina todo el sistema de autenticación.

```python
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
```

### 2. UserMixin
Una **clase auxiliar** que agrega propiedades y métodos necesarios a tu modelo de Usuario.

```python
from flask_login import UserMixin

class User(UserMixin, db.Model):
    # Your user model
    pass
```

### 3. current_user
Una **variable global** que contiene el usuario actualmente logueado.

```python
from flask_login import current_user

# Access current user anywhere
print(current_user.name)
print(current_user.email)
```

### 4. @login_required
Un **decorador** que protege rutas para que solo usuarios logueados puedan acceder.

```python
from flask_login import login_required

@app.route('/dashboard')
@login_required  # Only logged-in users can access
def dashboard():
    return "Welcome to dashboard!"
```

---

## Configuración Básica

### Paso 1: Importar y Configurar

```python
from flask import Flask
from flask_login import LoginManager

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for sessions

# Create LoginManager instance
login_manager = LoginManager()

# Initialize LoginManager with app
login_manager.init_app(app)

# Configure login view (where to redirect if not logged in)
login_manager.login_view = 'login'  # Name of your login route

# Optional: Custom message when login required
login_manager.login_message = 'Please log in to access this page.'
```

**Explicación línea por línea:**

1. `LoginManager()` - Crea una instancia del gestor de login
2. `init_app(app)` - Conecta el LoginManager con tu aplicación Flask
3. `login_view = 'login'` - Define a qué ruta redirigir si el usuario no está logueado
4. `login_message` - Mensaje que se muestra cuando se requiere login

### Paso 2: User Loader Function

Esta función **es obligatoria**. Flask-Login la usa para cargar un usuario desde la base de datos.

```python
@login_manager.user_loader
def load_user(user_id):
    """
    This function is called by Flask-Login to load a user from database
    
    Parameters:
        user_id (str): The user's ID stored in the session
    
    Returns:
        User object or None if user doesn't exist
    
    Flask-Login calls this function automatically on every request
    to check if the user is logged in
    """
    # Query user from database by ID
    return User.query.get(int(user_id))
```

**¿Cuándo se llama esta función?**
- En CADA request (petición) al servidor
- Flask-Login la usa para cargar el usuario actual
- Si retorna `None`, el usuario no está logueado

---

## Modelo de Usuario

Tu modelo de Usuario **debe** heredar de `UserMixin` o implementar estos métodos:

### Opción 1: Usar UserMixin (Recomendado - Más Fácil)

```python
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    User model with Flask-Login integration
    
    UserMixin provides these methods automatically:
    - is_authenticated: Returns True if user is logged in
    - is_active: Returns True if user account is active
    - is_anonymous: Returns False (True only for anonymous users)
    - get_id(): Returns the user ID as a string
    """
    
    # Database columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<User {self.email}>'
```

**¿Qué proporciona UserMixin?**

| Propiedad/Método | Qué hace | Retorna |
|------------------|----------|---------|
| `is_authenticated` | ¿Está el usuario autenticado? | `True` o `False` |
| `is_active` | ¿Está la cuenta activa? | `True` o `False` |
| `is_anonymous` | ¿Es un usuario anónimo? | `False` (usuarios reales) |
| `get_id()` | Obtiene el ID del usuario | String con el ID |

### Opción 2: Implementar Métodos Manualmente

```python
class User(db.Model):
    """User model with manual Flask-Login implementation"""
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)  # For is_active
    
    # Required by Flask-Login
    @property
    def is_authenticated(self):
        """Return True if user is authenticated (logged in)"""
        return True
    
    @property
    def is_active(self):
        """Return True if user account is active"""
        return self.active
    
    @property
    def is_anonymous(self):
        """Return False for real users, True for anonymous"""
        return False
    
    def get_id(self):
        """Return user ID as unicode string"""
        return str(self.id)
```

---

## Funciones Principales

### 1. `login_user()`

**Qué hace:** Inicia sesión para un usuario.

```python
from flask_login import login_user

# Basic usage
login_user(user)

# With "remember me" functionality
login_user(user, remember=True)

# With duration (how long to remember)
from datetime import timedelta
login_user(user, remember=True, duration=timedelta(days=7))
```

**Parámetros:**
- `user`: Objeto usuario a loguear
- `remember` (opcional): Si `True`, la sesión persiste después de cerrar navegador
- `duration` (opcional): Cuánto tiempo recordar al usuario
- `force` (opcional): Si `True`, ignora verificaciones de `is_active`
- `fresh` (opcional): Marca la sesión como "fresca" (para operaciones sensibles)

**Ejemplo completo:**

```python
from flask import request
from flask_login import login_user
from werkzeug.security import check_password_hash

@app.route('/login', methods=['POST'])
def login():
    """Login route with login_user() example"""
    
    # Get form data
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')  # Checkbox value
    
    # Find user in database
    user = User.query.filter_by(email=email).first()
    
    # Verify user exists and password is correct
    if user and check_password_hash(user.password, password):
        # Login the user
        login_user(user, remember=remember)  # This starts the session
        return redirect(url_for('dashboard'))
    else:
        return "Invalid credentials", 401
```

**¿Qué hace `login_user()` internamente?**
1. Guarda el ID del usuario en la sesión
2. Establece una cookie en el navegador
3. Marca al usuario como autenticado
4. Hace que `current_user` apunte a este usuario

### 2. `logout_user()`

**Qué hace:** Cierra la sesión del usuario actual.

```python
from flask_login import logout_user

@app.route('/logout')
def logout():
    """Logout current user"""
    logout_user()  # Removes user from session
    return redirect(url_for('home'))
```

**¿Qué hace `logout_user()` internamente?**
1. Elimina el ID del usuario de la sesión
2. Borra las cookies de "remember me"
3. Convierte `current_user` en usuario anónimo

### 3. `current_user`

**Qué es:** Una variable proxy que apunta al usuario actualmente logueado.

```python
from flask_login import current_user

# Check if user is logged in
if current_user.is_authenticated:
    print(f"User {current_user.name} is logged in")
else:
    print("No user logged in")

# Access user properties
email = current_user.email
name = current_user.name
user_id = current_user.id

# Use in templates
@app.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)
```

**Importante:**
- `current_user` está disponible en **todas las rutas**
- `current_user` está disponible en **todos los templates**
- Si no hay usuario logueado, `current_user.is_authenticated` es `False`

### 4. `login_required`

**Qué hace:** Decorador que protege rutas, requiriendo que el usuario esté logueado.

```python
from flask_login import login_required

@app.route('/dashboard')
@login_required  # User MUST be logged in to access
def dashboard():
    """Protected route - only for authenticated users"""
    return f"Welcome {current_user.name}!"

@app.route('/admin')
@login_required
def admin():
    """Another protected route"""
    # Only logged-in users can see this
    return "Admin panel"
```

**¿Qué pasa si el usuario NO está logueado?**
1. Flask-Login redirige a la ruta definida en `login_manager.login_view`
2. Muestra el mensaje definido en `login_manager.login_message`
3. Guarda la URL original para redirigir después del login

### 5. `fresh_login_required`

**Qué hace:** Similar a `login_required`, pero requiere un login "fresco" (reciente).

```python
from flask_login import fresh_login_required

@app.route('/change-password')
@fresh_login_required  # Requires recent login
def change_password():
    """Sensitive operation requiring fresh login"""
    return render_template('change_password.html')
```

**Uso típico:**
- Cambiar contraseña
- Modificar información sensible
- Transacciones financieras
- Eliminar cuenta

---

## Decoradores

### Comparación de Decoradores

| Decorador | Requiere | Uso |
|-----------|----------|-----|
| `@login_required` | Usuario logueado | Páginas protegidas normales |
| `@fresh_login_required` | Login reciente | Operaciones sensibles |
| Sin decorador | Nada | Páginas públicas |

### Ejemplo de uso combinado:

```python
from flask_login import login_required, fresh_login_required

# Public page - anyone can access
@app.route('/')
def home():
    return "Welcome to our site!"

# Protected page - must be logged in
@app.route('/dashboard')
@login_required
def dashboard():
    return "Your dashboard"

# Sensitive page - must have fresh login
@app.route('/delete-account')
@fresh_login_required
def delete_account():
    return "Delete account confirmation"
```

---

## Sistema Completo de Autenticación

### Aplicación Completa con Flask-Login

```python
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================
# APP CONFIGURATION
# ============================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize database
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect here if not logged in
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'  # Flash message category

# ============================================
# USER MODEL
# ============================================

class User(UserMixin, db.Model):
    """
    User model with Flask-Login integration
    
    UserMixin provides:
    - is_authenticated property
    - is_active property
    - is_anonymous property
    - get_id() method
    """
    
    # Database columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<User {self.email}>'

# Create database tables
with app.app_context():
    db.create_all()

# ============================================
# FLASK-LOGIN CONFIGURATION
# ============================================

@login_manager.user_loader
def load_user(user_id):
    """
    User loader callback for Flask-Login
    
    This function is called on EVERY request to load the current user
    from the user ID stored in the session
    
    Parameters:
        user_id (str): User ID from the session
    
    Returns:
        User object or None
    """
    # Query user by ID
    return User.query.get(int(user_id))

# ============================================
# ROUTES
# ============================================

@app.route('/')
def home():
    """Home page - accessible to everyone"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register new user
    
    GET: Show registration form
    POST: Process registration and create user
    """
    
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        # Validate input
        if not email or not password or not name:
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        # Hash password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Create new user
        new_user = User(
            email=email,
            name=name,
            password=hashed_password
        )
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login existing user
    
    GET: Show login form
    POST: Authenticate user and start session
    """
    
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
        
        # Login user with Flask-Login
        # This creates a session and sets current_user
        login_user(user, remember=remember)
        
        flash(f'Welcome back, {user.name}!', 'success')
        
        # Redirect to 'next' page if exists, otherwise dashboard
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required  # Only logged-in users can access
def dashboard():
    """
    User dashboard - protected route
    
    @login_required ensures only authenticated users can access
    If user is not logged in, redirects to login page
    """
    return render_template('dashboard.html', name=current_user.name)

@app.route('/profile')
@login_required
def profile():
    """User profile page - protected route"""
    return render_template('profile.html', user=current_user)

@app.route('/logout')
@login_required  # Optional: ensure user is logged in before logging out
def logout():
    """
    Logout current user
    
    logout_user() removes user from session and clears cookies
    """
    logout_user()  # This is the Flask-Login logout function
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

# ============================================
# CUSTOM ERROR HANDLERS
# ============================================

@login_manager.unauthorized_handler
def unauthorized():
    """
    Custom handler for unauthorized access
    
    Called when user tries to access @login_required route without logging in
    """
    flash('Please log in to access this page.', 'warning')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Templates HTML

### base.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask Login App{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Navigation bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('home') }}">Flask Auth</a>
            <div class="navbar-nav ms-auto">
                {% if current_user.is_authenticated %}
                    <!-- Show these links only if user is logged in -->
                    <a class="nav-link" href="{{ url_for('dashboard') }}">Dashboard</a>
                    <a class="nav-link" href="{{ url_for('profile') }}">Profile</a>
                    <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                    <span class="navbar-text ms-3">Hello, {{ current_user.name }}</span>
                {% else %}
                    <!-- Show these links only if user is NOT logged in -->
                    <a class="nav-link" href="{{ url_for('login') }}">Login</a>
                    <a class="nav-link" href="{{ url_for('register') }}">Register</a>
                {% endif %}
            </div>
        </div>
    </nav>
    
    <!-- Flash messages -->
    <div class="container mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>
    
    <!-- Page content -->
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### login.html
```html
{% extends "base.html" %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Login</h3>
            </div>
            <div class="card-body">
                <!-- Login form -->
                <form method="POST">
                    <!-- Email field -->
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                    
                    <!-- Password field -->
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    
                    <!-- Remember me checkbox -->
                    <div class="mb-3 form-check">
                        <input type="checkbox" class="form-check-input" id="remember" name="remember">
                        <label class="form-check-label" for="remember">Remember Me</label>
                    </div>
                    
                    <!-- Submit button -->
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
                
                <div class="mt-3 text-center">
                    <p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### register.html
```html
{% extends "base.html" %}

{% block title %}Register{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3>Register</h3>
            </div>
            <div class="card-body">
                <!-- Registration form -->
                <form method="POST">
                    <!-- Name field -->
                    <div class="mb-3">
                        <label for="name" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="name" name="name" required>
                    </div>
                    
                    <!-- Email field -->
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                    
                    <!-- Password field -->
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required minlength="8">
                        <small class="form-text text-muted">Password must be at least 8 characters</small>
                    </div>
                    
                    <!-- Submit button -->
                    <button type="submit" class="btn btn-primary w-100">Register</button>
                </form>
                
                <div class="mt-3 text-center">
                    <p>Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### dashboard.html
```html
{% extends "base.html" %}

{% block title %}Dashboard{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1>Welcome to Your Dashboard, {{ name }}!</h1>
        <p class="lead">This is a protected page. Only logged-in users can see this.</p>
        
        <div class="card mt-4">
            <div class="card-header">
                <h4>Your Information</h4>
            </div>
            <div class="card-body">
                <p><strong>Name:</strong> {{ current_user.name }}</p>
                <p><strong>Email:</strong> {{ current_user.email }}</p>
                <p><strong>User ID:</strong> {{ current_user.id }}</p>
                <p><strong>Authenticated:</strong> {{ current_user.is_authenticated }}</p>
                <p><strong>Active:</strong> {{ current_user.is_active }}</p>
            </div>
        </div>
        
        <div class="mt-4">
            <a href="{{ url_for('profile') }}" class="btn btn-primary">View Profile</a>
            <a href="{{ url_for('logout') }}" class="btn btn-danger">Logout</a>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Características Avanzadas

### 1. Remember Me Functionality

```python
from datetime import timedelta

# Configure remember cookie duration
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)  # Remember for 7 days
app.config['REMEMBER_COOKIE_SECURE'] = True  # Only send over HTTPS
app.config['REMEMBER_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access

@app.route('/login', methods=['POST'])
def login():
    """Login with remember me"""
    # ... authentication code ...
    
    # Check if user checked "remember me"
    remember = request.form.get('remember')
    
    # Login with remember option
    login_user(user, remember=remember)
    
    return redirect(url_for('dashboard'))
```

### 2. Session Protection

```python
# Configure session protection
login_manager.session_protection = 'strong'  # Options: None, 'basic', 'strong'

# 'strong': Tracks IP and user agent, logs out on change
# 'basic': Only tracks user agent
# None: No protection
```

### 3. Custom User Loader Error Handler

```python
@login_manager.user_loader
def load_user(user_id):
    """Load user with error handling"""
    try:
        return User.query.get(int(user_id))
    except:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    """Handle unauthorized access attempts"""
    flash('Please log in to access this page.', 'warning')
    return redirect(url_for('login'))
```

### 4. Fresh Login for Sensitive Operations

```python
from flask_login import fresh_login_required, login_fresh

@app.route('/change-password', methods=['GET', 'POST'])
@fresh_login_required  # Requires recent login
def change_password():
    """Change password - requires fresh login"""
    return render_template('change_password.html')

@app.route('/confirm-login', methods=['POST'])
def confirm_login():
    """Re-authenticate user for sensitive operations"""
    password = request.form.get('password')
    
    if check_password_hash(current_user.password, password):
        # Mark session as fresh
        login_user(current_user, fresh=True)
        return redirect(url_for('change_password'))
    else:
        flash('Invalid password', 'error')
        return redirect(url_for('confirm_login'))

# Check if login is fresh
if login_fresh():
    # Allow sensitive operation
    pass
else:
    # Require re-authentication
    return redirect(url_for('confirm_login'))
```

### 5. Custom Unauthorized Redirect

```python
from flask import request
from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    """Check if URL is safe for redirect"""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@app.route('/login', methods=['POST'])
def login():
    """Login with safe next redirect"""
    # ... authentication code ...
    
    login_user(user)
    
    # Get next page from query string
    next_page = request.args.get('next')
    
    # Validate redirect URL for security
    if not next_page or not is_safe_url(next_page):
        next_page = url_for('dashboard')
    
    return redirect(next_page)
```

### 6. Role-Based Access Control

```python
from functools import wraps
from flask import abort

# Add role to User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user', 'admin', etc.

# Custom decorator for role-based access
def role_required(role):
    """
    Decorator to require specific role
    
    Usage:
        @app.route('/admin')
        @role_required('admin')
        def admin_panel():
            return "Admin only"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is logged in
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            
            # Check if user has required role
            if current_user.role != role:
                abort(403)  # Forbidden
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usage example
@app.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    """Admin-only route"""
    return "Welcome to admin panel"
```

---

## Ejemplos Prácticos

### Ejemplo 1: Verificar si Usuario está Logueado en Template

```html
<!-- In any template -->
{% if current_user.is_authenticated %}
    <!-- User is logged in -->
    <p>Welcome, {{ current_user.name }}!</p>
    <a href="{{ url_for('logout') }}">Logout</a>
{% else %}
    <!-- User is NOT logged in -->
    <a href="{{ url_for('login') }}">Login</a>
    <a href="{{ url_for('register') }}">Register</a>
{% endif %}
```

### Ejemplo 2: Proteger Múltiples Rutas

```python
# Protect multiple routes with @login_required

@app.route('/dashboard')
@login_required
def dashboard():
    return "Dashboard"

@app.route('/profile')
@login_required
def profile():
    return f"Profile of {current_user.name}"

@app.route('/settings')
@login_required
def settings():
    return "Settings"

@app.route('/messages')
@login_required
def messages():
    return "Messages"
```

### Ejemplo 3: Conditional Content Based on Authentication

```python
@app.route('/home')
def home():
    """Show different content based on login status"""
    if current_user.is_authenticated:
        # User is logged in
        posts = Post.query.filter_by(author_id=current_user.id).all()
        return render_template('home_logged_in.html', posts=posts)
    else:
        # User is not logged in
        return render_template('home_public.html')
```

### Ejemplo 4: Ajax Login Request

```python
from flask import jsonify

@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for AJAX login"""
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401
```

### Ejemplo 5: Logout All Sessions

```python
# Add session token to User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    session_token = db.Column(db.String(100))  # Track current session
    
    def get_id(self):
        """Return user ID with session token"""
        return f"{self.id}:{self.session_token}"

@login_manager.user_loader
def load_user(user_id):
    """Load user and verify session token"""
    try:
        user_id, session_token = user_id.split(':')
        user = User.query.get(int(user_id))
        
        if user and user.session_token == session_token:
            return user
    except:
        pass
    
    return None

@app.route('/logout-all-devices')
@login_required
def logout_all_devices():
    """Logout from all devices by changing session token"""
    import secrets
    
    # Generate new session token
    current_user.session_token = secrets.token_hex(16)
    db.session.commit()
    
    # Logout current session
    logout_user()
    
    flash('Logged out from all devices', 'info')
    return redirect(url_for('login'))
```

---

## Resumen de Componentes

### Tabla de Funciones Principales

| Función | Qué hace | Cuándo usar |
|---------|----------|-------------|
| `LoginManager()` | Crea gestor de login | Configuración inicial |
| `login_manager.init_app(app)` | Inicializa con Flask | Configuración inicial |
| `@login_manager.user_loader` | Define cómo cargar usuarios | Configuración obligatoria |
| `login_user(user)` | Inicia sesión | Al autenticar usuario |
| `logout_user()` | Cierra sesión | Al cerrar sesión |
| `current_user` | Usuario actual | Acceder a usuario en cualquier parte |
| `@login_required` | Protege ruta | Rutas privadas |
| `@fresh_login_required` | Requiere login reciente | Operaciones sensibles |

### Propiedades de UserMixin

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `is_authenticated` | bool | `True` si usuario está logueado |
| `is_active` | bool | `True` si cuenta está activa |
| `is_anonymous` | bool | `False` para usuarios reales |
| `get_id()` | method | Retorna ID del usuario como string |

### Configuraciones Importantes

| Configuración | Valor | Descripción |
|---------------|-------|-------------|
| `login_view` | 'login' | Ruta de login |
| `login_message` | string | Mensaje al requerir login |
| `session_protection` | 'strong' | Nivel de protección de sesión |
| `REMEMBER_COOKIE_DURATION` | timedelta | Duración de "remember me" |

---

## Checklist de Implementación

Para implementar Flask-Login correctamente, asegúrate de:

- ✅ Instalar Flask-Login: `pip install flask-login`
- ✅ Crear instancia de `LoginManager`
- ✅ Configurar `SECRET_KEY` en app.config
- ✅ Definir `login_view`
- ✅ Crear modelo User con `UserMixin`
- ✅ Implementar función `@login_manager.user_loader`
- ✅ Usar `login_user()` en ruta de login
- ✅ Usar `logout_user()` en ruta de logout
- ✅ Proteger rutas con `@login_required`
- ✅ Usar `current_user` para acceder al usuario
- ✅ Verificar `current_user.is_authenticated` en templates

---

## Errores Comunes y Soluciones

### Error 1: "Please configure 'SECRET_KEY'"
```python
# WRONG
app = Flask(__name__)

# CORRECT
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

### Error 2: Usuario no se carga en cada request
```python
# WRONG - Missing user_loader
login_manager = LoginManager()
login_manager.init_app(app)

# CORRECT - Add user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### Error 3: @login_required no funciona
```python
# WRONG - No login_view configured
login_manager = LoginManager()

# CORRECT - Configure login_view
login_manager = LoginManager()
login_manager.login_view = 'login'
```

### Error 4: Usuario no tiene métodos requeridos
```python
# WRONG - User without required methods
class User(db.Model):
    pass

# CORRECT - Use UserMixin
from flask_login import UserMixin
class User(UserMixin, db.Model):
    pass
```

---

## Recursos Adicionales

- **Documentación oficial:** https://flask-login.readthedocs.io/
- **Flask Authentication Tutorial:** https://flask.palletsprojects.com/en/latest/patterns/
- **OWASP Authentication:** https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

---

**¡Flask-Login hace la autenticación simple y segura!** 🔐