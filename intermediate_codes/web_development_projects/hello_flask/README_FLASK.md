# Guía Completa de Flask para Principiantes

## 📚 Tabla de Contenidos
1. [¿Qué es Flask?](#qué-es-flask)
2. [Instalación](#instalación)
3. [Hola Mundo](#hola-mundo)
4. [Rutas y Decoradores](#rutas-y-decoradores)
5. [Variables en URLs](#variables-en-urls)
6. [Métodos HTTP](#métodos-http)
7. [Templates HTML](#templates-html)
8. [Formularios](#formularios)
9. [Archivos Estáticos](#archivos-estáticos)
10. [Request y Response](#request-y-response)
11. [Sesiones](#sesiones)
12. [Manejo de Errores](#manejo-de-errores)
13. [Estructura de Proyecto](#estructura-de-proyecto)

---

## ¿Qué es Flask?

**Flask** es un microframework web de Python que permite crear aplicaciones web de forma sencilla y rápida.

**Características:**
- ✅ Ligero y minimalista
- ✅ Fácil de aprender
- ✅ Flexible y extensible
- ✅ Perfecto para principiantes y proyectos pequeños

---

## Instalación

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

# Instalar Flask
pip install Flask
```

---

## Hola Mundo

### Ejemplo 1: Aplicación básica

```python
# app.py
from flask import Flask

# Crear una instancia de Flask
# __name__ le dice a Flask dónde encontrar recursos
app = Flask(__name__)

# Decorador @app.route define una ruta (URL)
# Cuando alguien visita "/" ejecuta la función de abajo
@app.route('/')
def home():
    return "¡Hola Mundo desde Flask!"

# Ejecutar la aplicación solo si este archivo se ejecuta directamente
if __name__ == '__main__':
    # debug=True recarga automáticamente cuando guardas cambios
    app.run(debug=True)
```

**Explicación línea por línea:**
1. `from flask import Flask` - Importa la clase Flask
2. `app = Flask(__name__)` - Crea una instancia de la aplicación Flask
3. `@app.route('/')` - Decorador que dice "cuando visiten la raíz del sitio..."
4. `def home():` - Función que maneja la petición
5. `return "¡Hola Mundo!"` - Lo que se muestra en el navegador
6. `app.run(debug=True)` - Inicia el servidor

**Para ejecutar:**
```bash
python app.py
```

Visita: `http://127.0.0.1:5000/`

---

## Rutas y Decoradores

En Flask, los decoradores `@app.route()` conectan URLs con funciones de Python.

### Ejemplo 2: Múltiples rutas

```python
from flask import Flask

app = Flask(__name__)

# Ruta principal
@app.route('/')
def index():
    return "Página de inicio"

# Ruta /about
@app.route('/about')
def about():
    return "Página Acerca de"

# Ruta /contact
@app.route('/contact')
def contact():
    return "Página de Contacto"

# Una función puede tener múltiples rutas
@app.route('/hello')
@app.route('/hola')
def greet():
    return "¡Saludos!"

if __name__ == '__main__':
    app.run(debug=True)
```

**URLs disponibles:**
- `http://127.0.0.1:5000/` → "Página de inicio"
- `http://127.0.0.1:5000/about` → "Página Acerca de"
- `http://127.0.0.1:5000/contact` → "Página de Contacto"
- `http://127.0.0.1:5000/hello` → "¡Saludos!"
- `http://127.0.0.1:5000/hola` → "¡Saludos!"

---

## Variables en URLs

Puedes capturar partes de la URL como variables.

### Ejemplo 3: URLs dinámicas

```python
from flask import Flask

app = Flask(__name__)

# Capturar una variable string en la URL
# <nombre> se convierte en un parámetro de la función
@app.route('/usuario/<nombre>')
def mostrar_usuario(nombre):
    return f"Perfil de usuario: {nombre}"

# Especificar el tipo de variable
# <int:id> solo acepta números enteros
@app.route('/post/<int:post_id>')
def mostrar_post(post_id):
    return f"Mostrando post #{post_id}"

# Múltiples variables
@app.route('/usuario/<nombre>/post/<int:post_id>')
def usuario_post(nombre, post_id):
    return f"Post #{post_id} del usuario {nombre}"

# Variable float
@app.route('/precio/<float:valor>')
def mostrar_precio(valor):
    return f"El precio es: ${valor:.2f}"

if __name__ == '__main__':
    app.run(debug=True)
```

**Tipos de convertidores disponibles:**
- `<string:variable>` - Texto (por defecto)
- `<int:variable>` - Números enteros
- `<float:variable>` - Números decimales
- `<path:variable>` - Como string pero acepta barras /
- `<uuid:variable>` - UUID

**Ejemplos de URLs:**
- `/usuario/Juan` → "Perfil de usuario: Juan"
- `/post/42` → "Mostrando post #42"
- `/usuario/Ana/post/5` → "Post #5 del usuario Ana"
- `/precio/19.99` → "El precio es: $19.99"

---

## Métodos HTTP

Las rutas pueden responder a diferentes métodos HTTP (GET, POST, etc.)

### Ejemplo 4: GET y POST

```python
from flask import Flask, request

app = Flask(__name__)

# Por defecto, las rutas solo aceptan GET
@app.route('/formulario')
def mostrar_formulario():
    return '''
        <form method="POST" action="/procesar">
            <input type="text" name="nombre" placeholder="Tu nombre">
            <button type="submit">Enviar</button>
        </form>
    '''

# methods=['GET', 'POST'] permite ambos métodos
@app.route('/procesar', methods=['GET', 'POST'])
def procesar():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        return f"¡Hola {nombre}! (enviado por POST)"
    else:
        return "Esta página espera un POST"

# Solo POST
@app.route('/api/crear', methods=['POST'])
def crear():
    return "Recurso creado"

if __name__ == '__main__':
    app.run(debug=True)
```

**Explicación:**
1. `methods=['GET', 'POST']` - Lista de métodos HTTP permitidos
2. `request.method` - Verifica qué método se usó
3. `request.form.get('nombre')` - Obtiene datos del formulario POST

---

## Templates HTML

Flask usa **Jinja2** para renderizar plantillas HTML dinámicas.

### Ejemplo 5: Estructura de carpetas

```
mi_proyecto/
│
├── app.py
└── templates/
    └── index.html
```

**app.py:**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # render_template busca archivos en la carpeta 'templates'
    nombre = "Juan"
    edad = 25
    # Pasar variables al template
    return render_template('index.html', nombre=nombre, edad=edad)

if __name__ == '__main__':
    app.run(debug=True)
```

**templates/index.html:**
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi Página Flask</title>
</head>
<body>
    <h1>¡Hola {{ nombre }}!</h1>
    <p>Tienes {{ edad }} años.</p>
</body>
</html>
```

**Explicación:**
- `render_template('index.html')` - Renderiza el archivo HTML
- `{{ nombre }}` - Sintaxis Jinja2 para insertar variables
- Las variables se pasan como parámetros a `render_template()`

### Ejemplo 6: Condicionales y Loops en Templates

**app.py:**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/usuarios')
def usuarios():
    lista_usuarios = [
        {"nombre": "Ana", "edad": 28, "activo": True},
        {"nombre": "Luis", "edad": 35, "activo": False},
        {"nombre": "María", "edad": 22, "activo": True}
    ]
    return render_template('usuarios.html', usuarios=lista_usuarios)

if __name__ == '__main__':
    app.run(debug=True)
```

**templates/usuarios.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Lista de Usuarios</title>
</head>
<body>
    <h1>Usuarios Registrados</h1>
    
    <!-- Loop en Jinja2 -->
    {% for usuario in usuarios %}
        <div>
            <h2>{{ usuario.nombre }}</h2>
            <p>Edad: {{ usuario.edad }}</p>
            
            <!-- Condicional en Jinja2 -->
            {% if usuario.activo %}
                <span style="color: green;">✓ Activo</span>
            {% else %}
                <span style="color: red;">✗ Inactivo</span>
            {% endif %}
        </div>
        <hr>
    {% endfor %}
</body>
</html>
```

**Sintaxis Jinja2:**
- `{% for item in lista %}` - Loop
- `{% if condicion %}` - Condicional
- `{{ variable }}` - Imprimir variable

---

## Formularios

### Ejemplo 7: Formulario completo

**Estructura:**
```
mi_proyecto/
│
├── app.py
└── templates/
    ├── formulario.html
    └── resultado.html
```

**app.py:**
```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mostrar formulario
@app.route('/registro')
def registro():
    return render_template('formulario.html')

# Procesar formulario
@app.route('/procesar-registro', methods=['POST'])
def procesar_registro():
    # Obtener datos del formulario
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    edad = request.form.get('edad')
    pais = request.form.get('pais')
    
    # Pasar datos al template de resultado
    return render_template('resultado.html', 
                          nombre=nombre, 
                          email=email, 
                          edad=edad, 
                          pais=pais)

if __name__ == '__main__':
    app.run(debug=True)
```

**templates/formulario.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Formulario de Registro</title>
</head>
<body>
    <h1>Registro de Usuario</h1>
    
    <!-- action: URL donde se envía el formulario -->
    <!-- method: POST para enviar datos -->
    <form action="/procesar-registro" method="POST">
        <label>Nombre:</label>
        <input type="text" name="nombre" required>
        <br><br>
        
        <label>Email:</label>
        <input type="email" name="email" required>
        <br><br>
        
        <label>Edad:</label>
        <input type="number" name="edad" min="1" max="120">
        <br><br>
        
        <label>País:</label>
        <select name="pais">
            <option value="Mexico">México</option>
            <option value="España">España</option>
            <option value="Argentina">Argentina</option>
        </select>
        <br><br>
        
        <button type="submit">Registrar</button>
    </form>
</body>
</html>
```

**templates/resultado.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Registro Exitoso</title>
</head>
<body>
    <h1>✓ Registro Exitoso</h1>
    
    <p><strong>Nombre:</strong> {{ nombre }}</p>
    <p><strong>Email:</strong> {{ email }}</p>
    <p><strong>Edad:</strong> {{ edad }}</p>
    <p><strong>País:</strong> {{ pais }}</p>
    
    <a href="/registro">Volver al formulario</a>
</body>
</html>
```

**Explicación:**
1. `action="/procesar-registro"` - URL donde se envía el formulario
2. `method="POST"` - Método HTTP para envío de datos
3. `name="nombre"` - Nombre del campo (usado en `request.form.get()`)
4. `request.form.get('nombre')` - Obtiene el valor del campo

---

## Archivos Estáticos

CSS, JavaScript e imágenes se colocan en la carpeta `static/`.

### Ejemplo 8: CSS y archivos estáticos

**Estructura:**
```
mi_proyecto/
│
├── app.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│       └── logo.png
└── templates/
    └── index.html
```

**app.py:**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

**static/css/style.css:**
```css
body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    padding: 20px;
}

h1 {
    color: #333;
    text-align: center;
}
```

**templates/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Mi Sitio</title>
    
    <!-- url_for('static', filename='...') genera la URL correcta -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Bienvenido a mi sitio</h1>
    
    <!-- Mostrar una imagen desde static/ -->
    <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
</body>
</html>
```

**Explicación:**
- Carpeta `static/` - Flask busca archivos estáticos aquí automáticamente
- `url_for('static', filename='...')` - Genera la URL correcta al archivo
- Nunca uses rutas hardcodeadas como `/static/css/style.css`

---

## Request y Response

### Ejemplo 9: Trabajando con request

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/info')
def info():
    # Información sobre la petición
    info_peticion = {
        "metodo": request.method,           # GET, POST, etc.
        "url": request.url,                 # URL completa
        "path": request.path,               # Solo el path
        "user_agent": str(request.user_agent),  # Navegador
        "ip": request.remote_addr           # IP del cliente
    }
    return jsonify(info_peticion)

# Query parameters: /buscar?q=python&pagina=1
@app.route('/buscar')
def buscar():
    # request.args obtiene parámetros de la URL
    query = request.args.get('q', 'nada')  # Default: 'nada'
    pagina = request.args.get('pagina', 1, type=int)
    return f"Buscando: {query}, Página: {pagina}"

# Recibir JSON
@app.route('/api/crear', methods=['POST'])
def crear():
    # request.json obtiene datos JSON del body
    datos = request.json
    nombre = datos.get('nombre')
    edad = datos.get('edad')
    return jsonify({"mensaje": f"Usuario {nombre} creado", "edad": edad})

if __name__ == '__main__':
    app.run(debug=True)
```

**Propiedades útiles de request:**
- `request.method` - Método HTTP (GET, POST, etc.)
- `request.args` - Parámetros de URL (?key=value)
- `request.form` - Datos de formularios POST
- `request.json` - Datos JSON del body
- `request.files` - Archivos subidos
- `request.cookies` - Cookies
- `request.headers` - Headers HTTP

---

## Sesiones

Las sesiones permiten almacenar datos entre peticiones para un usuario específico.

### Ejemplo 10: Login simple con sesiones

```python
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

# SECRET_KEY es necesaria para firmar las sesiones
# En producción, usa una clave secreta fuerte y manténla en secreto
app.secret_key = 'mi_clave_super_secreta_12345'

# Página de inicio
@app.route('/')
def index():
    # Verificar si el usuario está logueado
    if 'username' in session:
        username = session['username']
        return f"¡Hola {username}! <a href='/logout'>Cerrar sesión</a>"
    return "No has iniciado sesión. <a href='/login'>Iniciar sesión</a>"

# Mostrar formulario de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Guardar datos en la sesión
        username = request.form.get('username')
        session['username'] = username  # Guardar en sesión
        return redirect(url_for('index'))
    
    return '''
        <form method="POST">
            <input type="text" name="username" placeholder="Usuario">
            <button type="submit">Entrar</button>
        </form>
    '''

# Cerrar sesión
@app.route('/logout')
def logout():
    # Eliminar el username de la sesión
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

**Explicación:**
1. `app.secret_key` - Clave para firmar/encriptar sesiones (obligatoria)
2. `session['username'] = valor` - Guardar dato en la sesión
3. `'username' in session` - Verificar si existe un dato
4. `session.pop('username', None)` - Eliminar dato de la sesión
5. `redirect(url_for('index'))` - Redirigir a otra ruta

---

## Manejo de Errores

### Ejemplo 11: Páginas de error personalizadas

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Página de inicio"

@app.route('/causar-error')
def causar_error():
    # Esto causará un error 500
    resultado = 1 / 0
    return str(resultado)

# Manejador de error 404 (página no encontrada)
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

# Manejador de error 500 (error del servidor)
@app.errorhandler(500)
def error_servidor(error):
    return render_template('500.html'), 500

# Manejador genérico de excepciones
@app.errorhandler(Exception)
def manejar_excepcion(error):
    # Log del error (en producción usa logging)
    print(f"Error: {error}")
    return "Ha ocurrido un error", 500

if __name__ == '__main__':
    app.run(debug=True)
```

**templates/404.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>404 - Página No Encontrada</title>
</head>
<body>
    <h1>404 - Página No Encontrada</h1>
    <p>La página que buscas no existe.</p>
    <a href="/">Volver al inicio</a>
</body>
</html>
```

**Códigos de estado HTTP comunes:**
- `200` - OK (éxito)
- `404` - Not Found (no encontrado)
- `500` - Internal Server Error (error del servidor)
- `302` - Redirect (redirección)
- `403` - Forbidden (prohibido)

---

## Estructura de Proyecto

Para proyectos más grandes, organiza tu código en módulos.

### Ejemplo 12: Proyecto estructurado

```
mi_proyecto/
│
├── app.py                 # Punto de entrada
├── config.py              # Configuración
├── requirements.txt       # Dependencias
│
├── app/
│   ├── __init__.py       # Inicializa la app
│   ├── routes.py         # Rutas
│   └── models.py         # Modelos de datos
│
├── templates/
│   ├── base.html         # Template base
│   ├── index.html
│   └── about.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

**app.py:**
```python
from app import create_app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

**app/__init__.py:**
```python
from flask import Flask

def create_app():
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = 'mi_clave_secreta'
    
    # Registrar rutas
    from app import routes
    routes.init_app(app)
    
    return app
```

**app/routes.py:**
```python
from flask import render_template

def init_app(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')
```

**config.py:**
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-por-defecto'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
```

---

## 🎯 Comandos Útiles

### Ejecutar la aplicación

```bash
# Desarrollo
python app.py

# Especificar host y puerto
flask run --host=0.0.0.0 --port=8080

# Modo debug (recarga automática)
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
flask run
```

### Variables de entorno

```bash
# Linux/Mac
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

# Windows
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

---

## 📝 Plantilla Básica

```python
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ruta', methods=['GET', 'POST'])
def mi_ruta():
    if request.method == 'POST':
        dato = request.form.get('campo')
        # Procesar datos
        return redirect(url_for('index'))
    return render_template('formulario.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 🚀 Tips y Mejores Prácticas

1. **Siempre usa `debug=True` en desarrollo** - Recarga automática y errores detallados
2. **Usa `url_for()`** en lugar de URLs hardcodeadas
3. **Valida siempre los datos del usuario** - Nunca confíes en el input
4. **Usa templates** - No mezcles HTML con Python
5. **Organiza tu código** - Separa rutas, modelos y lógica
6. **Usa entornos virtuales** - Aísla las dependencias del proyecto
7. **No subas tu SECRET_KEY a Git** - Usa variables de entorno
8. **Usa HTTPS en producción** - Nunca HTTP para datos sensibles

---

## 🔧 Extensiones Populares

```bash
# Flask-SQLAlchemy (base de datos)
pip install flask-sqlalchemy

# Flask-Login (autenticación)
pip install flask-login

# Flask-WTF (formularios)
pip install flask-wtf

# Flask-Mail (envío de emails)
pip install flask-mail
```

---

## 📚 Recursos Adicionales

- [Documentación Oficial de Flask](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Flask Patterns](https://flask.palletsprojects.com/en/2.3.x/patterns/)

---

## 🎓 Próximos Pasos

1. ✅ Aprende Flask básico (esta guía)
2. ⬜ Conecta una base de datos (SQLAlchemy)
3. ⬜ Implementa autenticación (Flask-Login)
4. ⬜ Crea una API REST
5. ⬜ Despliega tu aplicación (Heroku, PythonAnywhere, etc.)

---

## 💡 Ejercicio Final: Blog Simple

Crea un blog con:
- Página de inicio que muestre posts
- Formulario para crear posts
- Vista individual de cada post
- Sesiones para autenticación básica

¡Usa todo lo que aprendiste en esta guía!