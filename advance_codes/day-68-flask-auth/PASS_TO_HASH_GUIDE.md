# Guía Completa: `generate_password_hash` y `check_password_hash`

## 📋 Tabla de Contenidos
1. [¿Qué es el Hash de Contraseñas?](#qué-es-el-hash-de-contraseñas)
2. [Instalación](#instalación)
3. [Funciones Principales](#funciones-principales)
4. [Ejemplos Básicos](#ejemplos-básicos)
5. [Uso con Flask y Base de Datos](#uso-con-flask-y-base-de-datos)
6. [Sistema Completo de Autenticación](#sistema-completo-de-autenticación)
7. [Mejores Prácticas](#mejores-prácticas)

---

## ¿Qué es el Hash de Contraseñas?

### El Problema
**❌ NUNCA hagas esto:**
```python
# WRONG - Storing password as plain text
password = "mypassword123"
user.password = password  # Anyone with database access can see it!
```

### La Solución: Hash
Un **hash** es una transformación irreversible de texto. Es como un código secreto que solo va en una dirección.

```
Original Password: "mypassword123"
                    ↓ (hash)
Hashed Password: "$2b$12$KIXxLV8zjWFVEWc5cGXLbOzuhQxPZ7l3h.F7yXGmj5LyqZ8Nx5FuK"
```

**Características del hash:**
- ✅ Es imposible revertirlo (no puedes obtener "mypassword123" del hash)
- ✅ La misma contraseña siempre genera un hash diferente (gracias al "salt")
- ✅ Puedes verificar si una contraseña coincide con el hash
- ✅ Mantiene las contraseñas seguras en la base de datos

---

## Instalación

```bash
# Install Werkzeug (included with Flask)
pip install Flask

# Or install Werkzeug separately
pip install Werkzeug
```

---

## Funciones Principales

### 1. `generate_password_hash()`
**Qué hace:** Convierte una contraseña de texto plano en un hash seguro.

**Sintaxis:**
```python
generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
```

**Parámetros:**
- `password`: La contraseña en texto plano (string)
- `method`: Algoritmo de hash (default: 'pbkdf2:sha256')
- `salt_length`: Longitud del "salt" aleatorio (default: 16)

### 2. `check_password_hash()`
**Qué hace:** Verifica si una contraseña coincide con un hash.

**Sintaxis:**
```python
check_password_hash(pwhash, password)
```

**Parámetros:**
- `pwhash`: El hash almacenado en la base de datos
- `password`: La contraseña que el usuario ingresó

**Retorna:**
- `True`: La contraseña es correcta
- `False`: La contraseña es incorrecta

---

## Ejemplos Básicos

### Ejemplo 1: Hash Simple

```python
from werkzeug.security import generate_password_hash, check_password_hash

# User creates an account with password
original_password = "mysecretpass123"

# Generate hash to store in database
hashed_password = generate_password_hash(original_password)

print("Original:", original_password)
print("Hashed:", hashed_password)

# Output:
# Original: mysecretpass123
# Hashed: pbkdf2:sha256:600000$randomsalt$longhashstring...
```

### Ejemplo 2: Verificar Contraseña

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Step 1: User registers (store hash in database)
password = "mypassword123"
hashed = generate_password_hash(password)
print(f"Stored in DB: {hashed}")

# Step 2: User tries to login
user_input = "mypassword123"  # User enters this

# Step 3: Check if password matches
is_correct = check_password_hash(hashed, user_input)

if is_correct:
    print("✅ Login successful!")
else:
    print("❌ Wrong password!")

# Output: ✅ Login successful!
```

### Ejemplo 3: Contraseña Incorrecta

```python
from werkzeug.security import generate_password_hash, check_password_hash

# User registered with this password
correct_password = "secretpass123"
hashed = generate_password_hash(correct_password)

# User tries to login with wrong password
wrong_attempt = "wrongpassword"

# Check password
is_valid = check_password_hash(hashed, wrong_attempt)

if is_valid:
    print("✅ Access granted")
else:
    print("❌ Access denied - Wrong password!")

# Output: ❌ Access denied - Wrong password!
```

### Ejemplo 4: Mismo Password, Diferentes Hashes

```python
from werkzeug.security import generate_password_hash

password = "samepassword"

# Generate hash 3 times with same password
hash1 = generate_password_hash(password)
hash2 = generate_password_hash(password)
hash3 = generate_password_hash(password)

print("Hash 1:", hash1)
print("Hash 2:", hash2)
print("Hash 3:", hash3)

# All three hashes are DIFFERENT!
# This is because of the random "salt" added each time
print("\nAre they the same?", hash1 == hash2)  # False

# But they all verify correctly
from werkzeug.security import check_password_hash
print("Hash 1 valid?", check_password_hash(hash1, password))  # True
print("Hash 2 valid?", check_password_hash(hash2, password))  # True
print("Hash 3 valid?", check_password_hash(hash3, password))  # True
```

---

## Uso con Flask y Base de Datos

### Ejemplo 5: Modelo de Usuario con SQLAlchemy

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    """User model with hashed password"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Stores HASH, not plain password
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<User {self.email}>'

# Create database
with app.app_context():
    db.create_all()
```

### Ejemplo 6: Registrar Usuario (Guardar Hash)

```python
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user with hashed password"""
    
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')  # Plain text password from form
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered!", 400
        
        # Hash the password BEFORE storing in database
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',  # Hashing algorithm
            salt_length=8            # Length of random salt
        )
        
        # Create new user with HASHED password
        new_user = User(
            email=email,
            name=name,
            password=hashed_password  # Store hash, NOT plain password
        )
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        print(f"✅ User registered: {email}")
        print(f"Password hash: {hashed_password}")
        
        return redirect(url_for('login'))
    
    return render_template('register.html')
```

### Ejemplo 7: Login (Verificar Hash)

```python
from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login user by checking password hash"""
    
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')  # Plain text password from form
        
        # Find user in database
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists
        if not user:
            print("❌ User not found")
            return "Invalid email or password", 401
        
        # Check if password matches the stored hash
        password_correct = check_password_hash(
            user.password,  # Hash from database
            password        # Plain text password user entered
        )
        
        if password_correct:
            # Password is correct - login successful
            session['user_id'] = user.id
            print(f"✅ Login successful for {email}")
            return redirect(url_for('dashboard'))
        else:
            # Password is wrong
            print(f"❌ Wrong password for {email}")
            return "Invalid email or password", 401
    
    return render_template('login.html')
```

---

## Sistema Completo de Autenticación

### Ejemplo 8: Aplicación Completa

```python
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# ============================================
# DATABASE MODEL
# ============================================

class User(db.Model):
    """User model with secure password storage"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Stores hash
    name = db.Column(db.String(100), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# ============================================
# ROUTES
# ============================================

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""
    
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        # Validate input
        if not email or not password or not name:
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        # Hash password before storing
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Create new user
        new_user = User(
            email=email,
            name=name,
            password=hashed_password  # Store hash, not plain password
        )
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login existing user"""
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            # Login successful
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Login failed
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Protected page - only for logged in users"""
    
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', name=session['user_name'])

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
```

---

## Templates HTML

### register.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Register</title>
</head>
<body>
    <h1>Register</h1>
    
    <!-- Flash messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <p style="color: {{ 'red' if category == 'error' else 'green' }}">
                    {{ message }}
                </p>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <!-- Registration form -->
    <form method="POST">
        <input type="text" name="name" placeholder="Full Name" required><br>
        <input type="email" name="email" placeholder="Email" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Register</button>
    </form>
    
    <p>Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
</body>
</html>
```

### login.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    
    <!-- Flash messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <p style="color: {{ 'red' if category == 'error' else 'green' }}">
                    {{ message }}
                </p>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <!-- Login form -->
    <form method="POST">
        <input type="email" name="email" placeholder="Email" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
    
    <p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
</body>
</html>
```

---

## Mejores Prácticas

### 1. ✅ Siempre Hashea las Contraseñas

```python
# CORRECT
hashed = generate_password_hash(password)
user.password = hashed

# WRONG - NEVER DO THIS
user.password = password  # Storing plain text!
```

### 2. ✅ Usa un Método de Hash Seguro

```python
# Recommended (default in Flask)
hashed = generate_password_hash(password, method='pbkdf2:sha256')

# Also good
hashed = generate_password_hash(password, method='scrypt')
```

### 3. ✅ No Reveles Información en Mensajes de Error

```python
# WRONG - Reveals if email exists
if not user:
    return "Email not found"
if not check_password_hash(user.password, password):
    return "Wrong password"

# CORRECT - Generic message
if not user or not check_password_hash(user.password, password):
    return "Invalid email or password"
```

### 4. ✅ Valida la Longitud de la Contraseña

```python
@app.route('/register', methods=['POST'])
def register():
    password = request.form.get('password')
    
    # Validate password strength
    if len(password) < 8:
        return "Password must be at least 8 characters", 400
    
    # Hash and store
    hashed = generate_password_hash(password)
    # ...
```

### 5. ✅ Usa HTTPS en Producción

```python
# In production, always use HTTPS to encrypt data in transit
# The hash protects data at rest (in database)
# HTTPS protects data in transit (over network)

if not app.debug:
    # Force HTTPS in production
    from flask_talisman import Talisman
    Talisman(app)
```

---

## Comparación Visual

### Flujo de Registro:
```
User enters: "mypassword123"
      ↓
generate_password_hash("mypassword123")
      ↓
Produces: "pbkdf2:sha256:600000$salt$longhash..."
      ↓
Store in database: user.password = hash
```

### Flujo de Login:
```
User enters: "mypassword123"
      ↓
Get hash from database: user.password
      ↓
check_password_hash(user.password, "mypassword123")
      ↓
Returns: True (if correct) or False (if wrong)
      ↓
Grant or deny access
```

---

## Tabla Resumen

| Función | Propósito | Cuándo Usar |
|---------|-----------|-------------|
| `generate_password_hash()` | Convierte contraseña a hash | Al **registrar** un usuario |
| `check_password_hash()` | Verifica si contraseña es correcta | Al **hacer login** |

| Parámetro | Valor por Defecto | Descripción |
|-----------|-------------------|-------------|
| `method` | `'pbkdf2:sha256'` | Algoritmo de hash |
| `salt_length` | `16` | Longitud del salt aleatorio |

---

## Preguntas Frecuentes

**Q: ¿Puedo "desencriptar" un hash para ver la contraseña original?**  
A: No. Los hashes son unidireccionales. No puedes obtener la contraseña original del hash.

**Q: ¿Por qué el mismo password genera diferentes hashes?**  
A: Por el "salt" (sal aleatoria) que se agrega cada vez. Esto previene ataques de tablas rainbow.

**Q: ¿Necesito almacenar el "salt" por separado?**  
A: No. El salt está incluido en el hash generado.

**Q: ¿Es seguro comparar hashes con `==`?**  
A: No. Siempre usa `check_password_hash()` para prevenir timing attacks.

---

## Recursos Adicionales

- **Documentación oficial:** https://werkzeug.palletsprojects.com/en/latest/utils/#module-werkzeug.security
- **Flask Authentication:** https://flask.palletsprojects.com/en/latest/patterns/
- **OWASP Password Storage:** https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

---

**¡Nunca almacenes contraseñas en texto plano! Siempre usa `generate_password_hash()`.** 🔒