# 🚀 Guía Completa: REST API con Flask y Postman

## 📋 Tabla de Contenidos
1. [Introducción a REST API](#introducción-a-rest-api)
2. [Configuración Inicial](#configuración-inicial)
3. [Métodos HTTP Explicados](#métodos-http-explicados)
4. [Ejemplo Completo: API de Películas](#ejemplo-completo-api-de-películas)
5. [Probando con Postman](#probando-con-postman)
6. [Snippets Útiles](#snippets-útiles)
7. [Manejo de Errores](#manejo-de-errores)

---

## 🎯 Introducción a REST API

### ¿Qué es una REST API?
Una REST API es una forma de comunicación entre aplicaciones usando HTTP. En lugar de renderizar HTML, enviamos y recibimos **JSON** (datos).

### Diferencias Clave:
- **Web App Tradicional**: Servidor → HTML → Navegador
- **REST API**: Servidor → JSON → Cliente (puede ser móvil, web, etc.)

---

## ⚙️ Configuración Inicial

### 1. Instalación de Paquetes
```bash
pip install flask flask-sqlalchemy python-dotenv
```

### 2. Estructura del Proyecto
```
mi_proyecto/
│
├── app.py              # Tu aplicación principal
├── .env                # Variables de entorno
├── instance/
│   └── database.db     # Base de datos SQLite
└── README.md           # Esta guía
```

### 3. Archivo `.env`
```env
SECRET_KEY=tu-clave-secreta-aqui-123456
DATABASE_URL=sqlite:///database.db
```

---

## 📚 Métodos HTTP Explicados

### GET - Obtener Datos
**Propósito**: Leer información sin modificar nada.
- No lleva datos en el body
- Usa parámetros en la URL: `/movies?year=2024`

### POST - Crear Datos
**Propósito**: Crear un nuevo recurso.
- Lleva datos en el body (JSON)
- Retorna el recurso creado

### PUT - Actualizar Completo
**Propósito**: Reemplazar un recurso completo.
- Debes enviar TODOS los campos
- Reemplaza el registro entero

### PATCH - Actualizar Parcial
**Propósito**: Actualizar solo algunos campos.
- Solo envías los campos que quieres cambiar
- Más flexible que PUT

### DELETE - Eliminar Datos
**Propósito**: Eliminar un recurso.
- Solo necesita el ID en la URL
- No lleva body

---

## 💻 Ejemplo Completo: API de Películas

### Código Completo `app.py`

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize database
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# ==================== MODEL ====================
class Movie(db.Model):
    """Movie model representing the movies table"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    review: Mapped[str] = mapped_column(String(500), nullable=True)
    
    def to_dict(self):
        """Convert movie object to dictionary for JSON response"""
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'rating': self.rating,
            'review': self.review
        }


# Create tables
with app.app_context():
    db.create_all()


# ==================== ROUTES ====================

# 1️⃣ GET ALL - Get all movies
@app.route('/api/movies', methods=['GET'])
def get_all_movies():
    """
    Get all movies from database
    URL: http://localhost:5000/api/movies
    Method: GET
    """
    # Query all movies using SQLAlchemy 2.0 syntax
    result = db.session.execute(db.select(Movie).order_by(Movie.rating.desc()))
    all_movies = result.scalars().all()
    
    # Convert movies to dictionary format
    movies_list = [movie.to_dict() for movie in all_movies]
    
    return jsonify({
        'success': True,
        'count': len(movies_list),
        'movies': movies_list
    }), 200


# 2️⃣ GET ONE - Get a specific movie by ID
@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """
    Get a single movie by ID
    URL: http://localhost:5000/api/movies/1
    Method: GET
    """
    # Find movie by ID using SQLAlchemy 2.0 syntax
    result = db.session.execute(db.select(Movie).where(Movie.id == movie_id))
    movie = result.scalar()
    
    # Check if movie exists
    if not movie:
        return jsonify({
            'success': False,
            'error': 'Movie not found'
        }), 404
    
    return jsonify({
        'success': True,
        'movie': movie.to_dict()
    }), 200


# 3️⃣ POST - Create a new movie
@app.route('/api/movies', methods=['POST'])
def create_movie():
    """
    Create a new movie
    URL: http://localhost:5000/api/movies
    Method: POST
    Body (JSON):
    {
        "title": "Inception",
        "year": 2010,
        "rating": 8.8,
        "review": "Amazing movie!"
    }
    """
    # Get JSON data from request
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    required_fields = ['title', 'year', 'rating']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Missing required field: {field}'
            }), 400
    
    # Create new movie instance
    new_movie = Movie(
        title=data['title'],
        year=data['year'],
        rating=data['rating'],
        review=data.get('review', '')  # Optional field
    )
    
    # Add to database
    db.session.add(new_movie)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Movie created successfully',
        'movie': new_movie.to_dict()
    }), 201


# 4️⃣ PUT - Update entire movie (all fields required)
@app.route('/api/movies/<int:movie_id>', methods=['PUT'])
def update_movie_put(movie_id):
    """
    Update entire movie (replace all fields)
    URL: http://localhost:5000/api/movies/1
    Method: PUT
    Body (JSON):
    {
        "title": "Inception Updated",
        "year": 2010,
        "rating": 9.0,
        "review": "Masterpiece!"
    }
    """
    # Find movie by ID
    result = db.session.execute(db.select(Movie).where(Movie.id == movie_id))
    movie = result.scalar()
    
    if not movie:
        return jsonify({
            'success': False,
            'error': 'Movie not found'
        }), 404
    
    # Get JSON data
    data = request.get_json()
    
    # Validate all required fields are present
    required_fields = ['title', 'year', 'rating']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Missing required field: {field}. PUT requires all fields.'
            }), 400
    
    # Update all fields
    movie.title = data['title']
    movie.year = data['year']
    movie.rating = data['rating']
    movie.review = data.get('review', '')
    
    # Commit changes
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Movie updated successfully',
        'movie': movie.to_dict()
    }), 200


# 5️⃣ PATCH - Update partial movie (only send fields to change)
@app.route('/api/movies/<int:movie_id>', methods=['PATCH'])
def update_movie_patch(movie_id):
    """
    Update specific fields of a movie
    URL: http://localhost:5000/api/movies/1
    Method: PATCH
    Body (JSON) - Example updating only rating:
    {
        "rating": 9.5
    }
    """
    # Find movie by ID
    result = db.session.execute(db.select(Movie).where(Movie.id == movie_id))
    movie = result.scalar()
    
    if not movie:
        return jsonify({
            'success': False,
            'error': 'Movie not found'
        }), 404
    
    # Get JSON data
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Update only the fields that are present in the request
    if 'title' in data:
        movie.title = data['title']
    if 'year' in data:
        movie.year = data['year']
    if 'rating' in data:
        movie.rating = data['rating']
    if 'review' in data:
        movie.review = data['review']
    
    # Commit changes
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Movie updated successfully',
        'movie': movie.to_dict()
    }), 200


# 6️⃣ DELETE - Delete a movie
@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    """
    Delete a movie by ID
    URL: http://localhost:5000/api/movies/1
    Method: DELETE
    """
    # Find movie by ID
    result = db.session.execute(db.select(Movie).where(Movie.id == movie_id))
    movie = result.scalar()
    
    if not movie:
        return jsonify({
            'success': False,
            'error': 'Movie not found'
        }), 404
    
    # Delete movie
    db.session.delete(movie)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Movie "{movie.title}" deleted successfully'
    }), 200


# 7️⃣ SEARCH - Search movies by title
@app.route('/api/movies/search', methods=['GET'])
def search_movies():
    """
    Search movies by title
    URL: http://localhost:5000/api/movies/search?title=inception
    Method: GET
    """
    # Get search term from query parameters
    search_term = request.args.get('title', '')
    
    if not search_term:
        return jsonify({
            'success': False,
            'error': 'Please provide a search term using ?title=your_search'
        }), 400
    
    # Search using LIKE operator (case-insensitive)
    result = db.session.execute(
        db.select(Movie).where(Movie.title.ilike(f'%{search_term}%'))
    )
    movies = result.scalars().all()
    
    return jsonify({
        'success': True,
        'count': len(movies),
        'movies': [movie.to_dict() for movie in movies]
    }), 200


# Root endpoint - API info
@app.route('/')
def home():
    """API information endpoint"""
    return jsonify({
        'message': 'Welcome to Movies API',
        'version': '1.0',
        'endpoints': {
            'GET /api/movies': 'Get all movies',
            'GET /api/movies/<id>': 'Get specific movie',
            'POST /api/movies': 'Create new movie',
            'PUT /api/movies/<id>': 'Update entire movie',
            'PATCH /api/movies/<id>': 'Update movie fields',
            'DELETE /api/movies/<id>': 'Delete movie',
            'GET /api/movies/search?title=': 'Search movies'
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
```

---

## 🧪 Probando con Postman

### Configuración Inicial de Postman

1. **Descargar Postman**: [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
2. **Crear una colección**: Haz clic en "New" → "Collection" → Nómbrala "Movies API"

### Pruebas Paso a Paso

#### 1️⃣ GET ALL - Obtener Todas las Películas

```
Método: GET
URL: http://localhost:5000/api/movies
Headers: (ninguno necesario)
Body: (ninguno)
```

**Respuesta Esperada:**
```json
{
    "success": true,
    "count": 2,
    "movies": [
        {
            "id": 1,
            "title": "Inception",
            "year": 2010,
            "rating": 8.8,
            "review": "Amazing!"
        }
    ]
}
```

---

#### 2️⃣ GET ONE - Obtener Una Película

```
Método: GET
URL: http://localhost:5000/api/movies/1
Headers: (ninguno necesario)
Body: (ninguno)
```

**Respuesta Esperada:**
```json
{
    "success": true,
    "movie": {
        "id": 1,
        "title": "Inception",
        "year": 2010,
        "rating": 8.8,
        "review": "Amazing!"
    }
}
```

---

#### 3️⃣ POST - Crear Nueva Película

```
Método: POST
URL: http://localhost:5000/api/movies
Headers: Content-Type: application/json
Body (raw JSON):
```

```json
{
    "title": "The Matrix",
    "year": 1999,
    "rating": 8.7,
    "review": "Mind-blowing!"
}
```

**Respuesta Esperada:**
```json
{
    "success": true,
    "message": "Movie created successfully",
    "movie": {
        "id": 2,
        "title": "The Matrix",
        "year": 1999,
        "rating": 8.7,
        "review": "Mind-blowing!"
    }
}
```

**Pasos en Postman:**
1. Selecciona método **POST**
2. En la pestaña **Body** → selecciona **raw** → selecciona **JSON**
3. Pega el JSON del ejemplo
4. Click en **Send**

---

#### 4️⃣ PUT - Actualizar Película Completa

```
Método: PUT
URL: http://localhost:5000/api/movies/1
Headers: Content-Type: application/json
Body (raw JSON):
```

```json
{
    "title": "Inception - Director's Cut",
    "year": 2010,
    "rating": 9.0,
    "review": "Masterpiece of cinema!"
}
```

**⚠️ Nota**: PUT requiere TODOS los campos. Si olvidas uno, debes enviarlo igual.

---

#### 5️⃣ PATCH - Actualizar Solo Rating

```
Método: PATCH
URL: http://localhost:5000/api/movies/1
Headers: Content-Type: application/json
Body (raw JSON):
```

```json
{
    "rating": 9.5
}
```

**✅ Ventaja**: Solo envías lo que quieres cambiar. El resto permanece igual.

---

#### 6️⃣ DELETE - Eliminar Película

```
Método: DELETE
URL: http://localhost:5000/api/movies/1
Headers: (ninguno necesario)
Body: (ninguno)
```

**Respuesta Esperada:**
```json
{
    "success": true,
    "message": "Movie 'Inception' deleted successfully"
}
```

---

#### 7️⃣ SEARCH - Buscar Películas

```
Método: GET
URL: http://localhost:5000/api/movies/search?title=matrix
Headers: (ninguno necesario)
Body: (ninguno)
```

**Nota**: Los parámetros van en la URL después de `?`

---

## 📦 Snippets Útiles

### 1. Modelo Básico con to_dict()

```python
class Product(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }
```

---

### 2. Obtener Todos los Registros

```python
@app.route('/api/products', methods=['GET'])
def get_all_products():
    # Get all records ordered by name
    result = db.session.execute(db.select(Product).order_by(Product.name))
    products = result.scalars().all()
    
    return jsonify({
        'success': True,
        'products': [product.to_dict() for product in products]
    }), 200
```

---

### 3. Obtener Un Registro por ID

```python
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    # Find by ID
    result = db.session.execute(db.select(Product).where(Product.id == product_id))
    product = result.scalar()
    
    if not product:
        return jsonify({'success': False, 'error': 'Not found'}), 404
    
    return jsonify({'success': True, 'product': product.to_dict()}), 200
```

---

### 4. Crear Nuevo Registro

```python
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    # Validate data
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'success': False, 'error': 'Invalid data'}), 400
    
    # Create new instance
    new_product = Product(
        name=data['name'],
        price=data['price'],
        stock=data.get('stock', 0)
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'product': new_product.to_dict()
    }), 201
```

---

### 5. Actualizar Registro (PATCH)

```python
@app.route('/api/products/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    # Find product
    result = db.session.execute(db.select(Product).where(Product.id == product_id))
    product = result.scalar()
    
    if not product:
        return jsonify({'success': False, 'error': 'Not found'}), 404
    
    # Get data
    data = request.get_json()
    
    # Update only provided fields
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']
    
    db.session.commit()
    
    return jsonify({'success': True, 'product': product.to_dict()}), 200
```

---

### 6. Eliminar Registro

```python
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    # Find product
    result = db.session.execute(db.select(Product).where(Product.id == product_id))
    product = result.scalar()
    
    if not product:
        return jsonify({'success': False, 'error': 'Not found'}), 404
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Deleted successfully'}), 200
```

---

### 7. Buscar con Filtros

```python
@app.route('/api/products/search', methods=['GET'])
def search_products():
    # Get query parameters
    name = request.args.get('name', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    # Start with base query
    query = db.select(Product)
    
    # Add filters
    if name:
        query = query.where(Product.name.ilike(f'%{name}%'))
    if min_price:
        query = query.where(Product.price >= min_price)
    if max_price:
        query = query.where(Product.price <= max_price)
    
    # Execute query
    result = db.session.execute(query)
    products = result.scalars().all()
    
    return jsonify({
        'success': True,
        'products': [product.to_dict() for product in products]
    }), 200
```

---

### 8. Validación de Datos

```python
def validate_movie_data(data, required_fields):
    """
    Validate incoming JSON data
    Returns: (is_valid, error_message)
    """
    if not data:
        return False, 'No data provided'
    
    for field in required_fields:
        if field not in data:
            return False, f'Missing required field: {field}'
    
    return True, None

# Use in route
@app.route('/api/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    
    is_valid, error = validate_movie_data(data, ['title', 'year', 'rating'])
    if not is_valid:
        return jsonify({'success': False, 'error': error}), 400
    
    # Continue with creation...
```

---

### 9. Paginación

```python
@app.route('/api/products', methods=['GET'])
def get_products_paginated():
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Calculate offset
    offset = (page - 1) * per_page
    
    # Query with limit and offset
    result = db.session.execute(
        db.select(Product)
        .limit(per_page)
        .offset(offset)
    )
    products = result.scalars().all()
    
    # Get total count
    total_result = db.session.execute(db.select(db.func.count(Product.id)))
    total = total_result.scalar()
    
    return jsonify({
        'success': True,
        'page': page,
        'per_page': per_page,
        'total': total,
        'products': [product.to_dict() for product in products]
    }), 200
```

---

### 10. Error Handler Global

```python
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500
```

---

## ⚠️ Manejo de Errores

### Códigos de Estado HTTP Comunes

| Código | Significado | Cuándo Usar |
|--------|-------------|-------------|
| 200 | OK | Operación exitosa (GET, PUT, PATCH) |
| 201 | Created | Recurso creado exitosamente (POST) |
| 400 | Bad Request | Datos inválidos o incompletos |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error del servidor |

### Template de Manejo de Errores

```python
@app.route('/api/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    try:
        result = db.session.execute(db.select(Movie).where(Movie.id == movie_id))
        movie = result.scalar()
        
        if not movie:
            return jsonify({
                'success': False,
                'error': 'Movie not found'
            }), 404
        
        return jsonify({
            'success': True,
            'movie': movie.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'An error occurred',
            'details': str(e)
        }), 500
```

---

## 🎯 Consejos Finales

### 1. Siempre Retorna JSON
```python
# ✅ Correcto
return jsonify({'success': True}), 200

# ❌ Incorrecto
return "Success", 200
```

### 2. Usa Códigos de Estado Apropiados
```python
# ✅ Correcto - 201 para creación
return jsonify({'movie': new_movie.to_dict()}), 201

# ❌ Incorrecto - 200 no es para creación
return jsonify({'movie': new_movie.to_dict()}), 200
```

### 3. Siempre Valida los Datos
```python
# ✅ Siempre verifica que data existe
data = request.get_json()
if not data:
    return jsonify({'error': 'No data provided'}), 400
```

### 4. Usa to_dict() para Serializar
```python
# ✅ Correcto
return jsonify({'movie': movie.to_dict()})

# ❌ No puedes retornar el objeto directamente
return jsonify({'movie': movie})  # Esto da error
```

### 5. Commit Después de Cambios
```python
# ✅ Siempre haz commit después de modificar
db.session.add(new_movie)
db.session.commit()

# ✅ Usa rollback si hay error
except Exception as e:
    db.session.rollback()
```

---

## 📚 Recursos Adicionales

- **Flask Docs**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **SQLAlchemy 2.0 Docs**: [https://docs.sqlalchemy.org/en/20/](https://docs.sqlalchemy.org/en/20/)
- **Postman Learning**: [https://learning.postman.com/](https://learning.postman.com/)
- **REST API Tutorial**: [https://restfulapi.net/](https://restfulapi.net/)

---

## ✅ Checklist para Crear una API

- [ ] Crear modelo con `to_dict()`
- [ ] Implementar GET all (lista completa)
- [ ] Implementar GET one (por ID)
- [ ] Implementar POST (crear)
- [ ] Implementar PATCH (actualizar parcial)
- [ ] Implementar DELETE (eliminar)
- [ ] Añadir validación de datos
- [ ] Manejar errores 404
- [ ] Retornar códigos de estado correctos
- [ ] Probar todos los endpoints en Postman
- [ ] Documentar la API

---

**¡Felicitaciones!** 🎉 Ahora tienes una guía completa para crear y probar REST APIs con Flask.