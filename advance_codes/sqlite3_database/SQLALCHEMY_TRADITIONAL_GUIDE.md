# Guía Completa de SQLAlchemy con Flask

## 📚 Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Configuración Inicial](#configuración-inicial)
5. [Modelos (Models)](#modelos-models)
6. [Operaciones CRUD](#operaciones-crud)
7. [Relaciones entre Tablas](#relaciones-entre-tablas)
8. [Consultas Avanzadas](#consultas-avanzadas)
9. [Migraciones con Flask-Migrate](#migraciones-con-flask-migrate)
10. [Live Templates para PyCharm](#live-templates-para-pycharm)

---

## Introducción

**SQLAlchemy** es un ORM (Object-Relational Mapping) que te permite trabajar con bases de datos usando objetos de Python en lugar de escribir SQL directamente.

**Conceptos clave:**
- **ORM**: Convierte clases de Python en tablas de base de datos
- **Session**: Maneja las transacciones con la base de datos
- **Model**: Una clase que representa una tabla
- **Query**: Permite buscar datos en la base de datos

---

## Instalación

```bash
# Instalar dependencias necesarias
pip install flask
pip install flask-sqlalchemy
pip install flask-migrate
pip install python-dotenv

# Para PostgreSQL
pip install psycopg2-binary

# Para MySQL
pip install pymysql
```

---

## Estructura del Proyecto

```
mi_proyecto/
│
├── app/
│   ├── __init__.py          # Inicialización de Flask y extensiones
│   ├── models.py            # Modelos de base de datos
│   ├── routes.py            # Rutas de la aplicación
│   └── config.py            # Configuración
│
├── migrations/              # Carpeta de migraciones (auto-generada)
├── instance/                # Base de datos SQLite (auto-generada)
├── .env                     # Variables de entorno
├── requirements.txt         # Dependencias
└── run.py                   # Punto de entrada de la aplicación
```

---

## Configuración Inicial

### 1. Archivo `config.py`

```python
# app/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """
    Clase de configuración base para la aplicación Flask
    """
    # SECRET_KEY: Clave secreta para sesiones y formularios
    # Se obtiene de las variables de entorno o usa un valor por defecto
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-super-secreta-cambiar-en-produccion'
    
    # SQLALCHEMY_DATABASE_URI: URL de conexión a la base de datos
    # Format: dialect+driver://username:password@host:port/database
    # SQLite (desarrollo): sqlite:///ruta/al/archivo.db
    # PostgreSQL: postgresql://usuario:password@localhost/nombre_db
    # MySQL: mysql+pymysql://usuario:password@localhost/nombre_db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance', 'app.db')
    
    # SQLALCHEMY_TRACK_MODIFICATIONS: Desactivar para ahorrar recursos
    # Este sistema de señales consume mucha memoria
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLALCHEMY_ECHO: Mostrar SQL en consola (útil para debugging)
    SQLALCHEMY_ECHO = True  # Cambiar a False en producción
```

### 2. Archivo `.env`

```bash
# .env
SECRET_KEY=tu-clave-secreta-muy-segura
DATABASE_URL=sqlite:///instance/app.db
FLASK_APP=run.py
FLASK_ENV=development
```

### 3. Archivo `app/__init__.py`

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

# Inicializar extensiones
# db: Objeto de SQLAlchemy que maneja todas las operaciones de base de datos
db = SQLAlchemy()

# migrate: Objeto que maneja las migraciones de base de datos
migrate = Migrate()

def create_app(config_class=Config):
    """
    Factory function para crear la aplicación Flask
    
    Args:
        config_class: Clase de configuración a usar
    
    Returns:
        app: Instancia de la aplicación Flask configurada
    """
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Cargar configuración desde la clase Config
    app.config.from_object(config_class)
    
    # Inicializar extensiones con la app
    # db.init_app: Conecta SQLAlchemy con la aplicación Flask
    db.init_app(app)
    
    # migrate: Inicializa Flask-Migrate para manejar migraciones
    migrate.init_app(app, db)
    
    # Importar modelos después de inicializar db
    # Esto evita importaciones circulares
    from app import models
    
    # Registrar blueprints (rutas)
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Crear tablas si no existen (solo para desarrollo simple)
    with app.app_context():
        db.create_all()
    
    return app
```

### 4. Archivo `run.py`

```python
# run.py
from app import create_app, db

# Crear la aplicación usando la factory function
app = create_app()

if __name__ == '__main__':
    # Ejecutar servidor de desarrollo
    app.run(debug=True)
```

---

## Modelos (Models)

### Archivo `app/models.py`

```python
# app/models.py
from app import db
from datetime import datetime

class Usuario(db.Model):
    """
    Modelo Usuario: representa la tabla 'usuarios' en la base de datos
    
    Cada atributo de clase se convierte en una columna de la tabla
    """
    # __tablename__: Nombre explícito de la tabla (opcional)
    # Si no se especifica, SQLAlchemy usa el nombre de la clase en minúsculas
    __tablename__ = 'usuarios'
    
    # Columna id: Primary Key (clave primaria)
    # db.Integer: Tipo de dato entero
    # primary_key=True: Marca esta columna como clave primaria
    # autoincrement=True: El valor se incrementa automáticamente
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Columna username: Nombre de usuario único
    # db.String(80): Cadena de texto de máximo 80 caracteres
    # unique=True: No permite valores duplicados
    # nullable=False: No permite valores NULL (obligatorio)
    # index=True: Crea un índice para búsquedas más rápidas
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    
    # Columna email: Correo electrónico único
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    
    # Columna password_hash: Contraseña hasheada
    # nullable=True: Permite valores NULL (opcional)
    password_hash = db.Column(db.String(255), nullable=True)
    
    # Columna nombre_completo: Nombre completo del usuario
    nombre_completo = db.Column(db.String(200))
    
    # Columna activo: Estado del usuario
    # db.Boolean: Tipo de dato booleano (True/False)
    # default=True: Valor por defecto si no se especifica
    activo = db.Column(db.Boolean, default=True)
    
    # Columna fecha_creacion: Fecha de creación del registro
    # db.DateTime: Tipo de dato fecha y hora
    # default=datetime.utcnow: Función que se ejecuta al crear el registro
    # Nota: Se pasa la función, no el resultado (sin paréntesis)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Columna fecha_actualizacion: Fecha de última actualización
    # onupdate=datetime.utcnow: Se actualiza automáticamente en cada modificación
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación con otra tabla (se explica más adelante)
    # posts: Lista de posts asociados a este usuario
    # backref='autor': Crea un atributo 'autor' en el modelo Post
    # lazy='dynamic': Carga los datos solo cuando se accede a ellos
    posts = db.relationship('Post', backref='autor', lazy='dynamic')
    
    def __repr__(self):
        """
        Representación del objeto para debugging
        Se usa cuando imprimes el objeto: print(usuario)
        """
        return f'<Usuario {self.username}>'
    
    def to_dict(self):
        """
        Convierte el objeto a diccionario (útil para JSON)
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nombre_completo': self.nombre_completo,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }


class Post(db.Model):
    """
    Modelo Post: representa una publicación o artículo
    """
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Columna titulo: Título del post
    titulo = db.Column(db.String(200), nullable=False)
    
    # Columna contenido: Contenido del post
    # db.Text: Texto de longitud variable (sin límite específico)
    contenido = db.Column(db.Text, nullable=False)
    
    # Columna publicado: Estado de publicación
    publicado = db.Column(db.Boolean, default=False)
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Key: Llave foránea que relaciona con la tabla usuarios
    # db.ForeignKey('usuarios.id'): Hace referencia a la columna id de la tabla usuarios
    # nullable=False: Un post debe pertenecer a un usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    def __repr__(self):
        return f'<Post {self.titulo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'contenido': self.contenido,
            'publicado': self.publicado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'usuario_id': self.usuario_id,
            'autor': self.autor.username if self.autor else None
        }
```

### Tipos de Datos Comunes

```python
# Tipos de columnas más usados en SQLAlchemy

# Números
db.Integer          # Números enteros
db.BigInteger       # Enteros grandes
db.SmallInteger     # Enteros pequeños
db.Float            # Números decimales
db.Numeric(10, 2)   # Números decimales con precisión (10 dígitos, 2 decimales)

# Texto
db.String(n)        # Cadena de longitud fija (máximo n caracteres)
db.Text             # Texto de longitud variable
db.Unicode(n)       # Cadena Unicode de longitud fija
db.UnicodeText      # Texto Unicode de longitud variable

# Fechas y Tiempo
db.Date             # Solo fecha (año, mes, día)
db.Time             # Solo hora (hora, minuto, segundo)
db.DateTime         # Fecha y hora completa
db.Timestamp        # Marca de tiempo

# Booleanos
db.Boolean          # True o False

# Binarios
db.LargeBinary      # Datos binarios (imágenes, archivos)
db.PickleType       # Almacena objetos Python serializados

# JSON
db.JSON             # Almacena datos JSON (PostgreSQL, MySQL 5.7+)
```

---

## Operaciones CRUD

### Archivo `app/routes.py`

```python
# app/routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.models import Usuario, Post

# Crear Blueprint: permite organizar rutas en módulos
bp = Blueprint('main', __name__)


# ============================================
# CREATE - Crear nuevos registros
# ============================================

@bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    """
    Crea un nuevo usuario en la base de datos
    
    Recibe JSON: {"username": "...", "email": "...", "nombre_completo": "..."}
    """
    # request.get_json(): Obtiene los datos JSON del request
    data = request.get_json()
    
    # Crear instancia del modelo Usuario
    # Se pasan los datos como argumentos con nombre
    nuevo_usuario = Usuario(
        username=data.get('username'),
        email=data.get('email'),
        nombre_completo=data.get('nombre_completo')
    )
    
    try:
        # db.session.add(): Agrega el objeto a la sesión
        # La sesión es como un "carrito" de cambios pendientes
        db.session.add(nuevo_usuario)
        
        # db.session.commit(): Confirma los cambios en la base de datos
        # Aquí es cuando realmente se ejecuta el INSERT
        db.session.commit()
        
        return jsonify(nuevo_usuario.to_dict()), 201
    
    except Exception as e:
        # db.session.rollback(): Revierte los cambios si hay error
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ============================================
# READ - Leer registros
# ============================================

@bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    """
    Obtiene todos los usuarios de la base de datos
    """
    # Usuario.query: Objeto Query para hacer consultas
    # .all(): Ejecuta la consulta y devuelve todos los resultados
    # Equivalente SQL: SELECT * FROM usuarios
    usuarios = Usuario.query.all()
    
    # Convertir cada usuario a diccionario
    return jsonify([usuario.to_dict() for usuario in usuarios]), 200


@bp.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    """
    Obtiene un usuario específico por su ID
    
    Args:
        id: ID del usuario (se extrae de la URL)
    """
    # .get_or_404(): Busca por primary key (id)
    # Si no encuentra el registro, devuelve error 404 automáticamente
    # Equivalente SQL: SELECT * FROM usuarios WHERE id = ?
    usuario = Usuario.query.get_or_404(id)
    
    return jsonify(usuario.to_dict()), 200


@bp.route('/usuarios/buscar', methods=['GET'])
def buscar_usuario():
    """
    Busca un usuario por username o email
    
    Query params: ?username=... o ?email=...
    """
    # request.args.get(): Obtiene parámetros de la URL
    username = request.args.get('username')
    email = request.args.get('email')
    
    if username:
        # .filter_by(): Filtra usando argumentos con nombre (igualdad simple)
        # Equivalente SQL: SELECT * FROM usuarios WHERE username = ?
        usuario = Usuario.query.filter_by(username=username).first()
    elif email:
        # .filter(): Filtra usando expresiones más complejas
        # Usuario.email == email: Expresión de igualdad
        usuario = Usuario.query.filter(Usuario.email == email).first()
    else:
        return jsonify({'error': 'Especifica username o email'}), 400
    
    if usuario:
        return jsonify(usuario.to_dict()), 200
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404


# ============================================
# UPDATE - Actualizar registros
# ============================================

@bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    """
    Actualiza los datos de un usuario existente
    """
    # Buscar el usuario existente
    usuario = Usuario.query.get_or_404(id)
    
    # Obtener nuevos datos
    data = request.get_json()
    
    try:
        # Actualizar atributos del objeto
        # Solo actualiza los campos que se envían
        if 'username' in data:
            usuario.username = data['username']
        if 'email' in data:
            usuario.email = data['email']
        if 'nombre_completo' in data:
            usuario.nombre_completo = data['nombre_completo']
        if 'activo' in data:
            usuario.activo = data['activo']
        
        # No es necesario hacer add() porque el objeto ya está en la sesión
        # Solo hacemos commit() para guardar los cambios
        # Equivalente SQL: UPDATE usuarios SET ... WHERE id = ?
        db.session.commit()
        
        return jsonify(usuario.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ============================================
# DELETE - Eliminar registros
# ============================================

@bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    """
    Elimina un usuario de la base de datos
    """
    usuario = Usuario.query.get_or_404(id)
    
    try:
        # db.session.delete(): Marca el objeto para eliminación
        db.session.delete(usuario)
        
        # commit(): Ejecuta el DELETE en la base de datos
        # Equivalente SQL: DELETE FROM usuarios WHERE id = ?
        db.session.commit()
        
        return jsonify({'mensaje': 'Usuario eliminado exitosamente'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ============================================
# Crear Post asociado a un Usuario
# ============================================

@bp.route('/usuarios/<int:usuario_id>/posts', methods=['POST'])
def crear_post(usuario_id):
    """
    Crea un post asociado a un usuario
    """
    # Verificar que el usuario existe
    usuario = Usuario.query.get_or_404(usuario_id)
    
    data = request.get_json()
    
    nuevo_post = Post(
        titulo=data.get('titulo'),
        contenido=data.get('contenido'),
        publicado=data.get('publicado', False),
        usuario_id=usuario_id  # Foreign key
    )
    
    try:
        db.session.add(nuevo_post)
        db.session.commit()
        
        return jsonify(nuevo_post.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@bp.route('/usuarios/<int:usuario_id>/posts', methods=['GET'])
def obtener_posts_usuario(usuario_id):
    """
    Obtiene todos los posts de un usuario
    """
    usuario = Usuario.query.get_or_404(usuario_id)
    
    # Acceder a la relación 'posts' definida en el modelo
    # usuario.posts devuelve un query porque lazy='dynamic'
    posts = usuario.posts.all()
    
    return jsonify([post.to_dict() for post in posts]), 200
```

---

## Relaciones entre Tablas

### Tipos de Relaciones

```python
# app/models.py - Ejemplos de relaciones

# ============================================
# 1. One-to-Many (Uno a Muchos)
# ============================================
# Un usuario tiene muchos posts
# Un post pertenece a un usuario

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    
    # Lado "uno": define la relación
    # 'Post': Nombre del modelo relacionado (como string)
    # backref='autor': Crea atributo 'autor' en Post para acceso inverso
    # lazy='dynamic': Devuelve un query en lugar de cargar todos los datos
    posts = db.relationship('Post', backref='autor', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200))
    
    # Lado "muchos": define la foreign key
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    # No necesita relationship porque backref lo crea automáticamente


# Uso:
# usuario = Usuario.query.get(1)
# posts = usuario.posts.all()  # Obtener todos los posts del usuario
# 
# post = Post.query.get(1)
# autor = post.autor  # Obtener el usuario que creó el post


# ============================================
# 2. Many-to-Many (Muchos a Muchos)
# ============================================
# Un estudiante tiene muchas clases
# Una clase tiene muchos estudiantes
# Se requiere una tabla intermedia (association table)

# Tabla intermedia (no es un modelo completo, solo una tabla)
inscripciones = db.Table('inscripciones',
    # Primera foreign key
    db.Column('estudiante_id', db.Integer, db.ForeignKey('estudiantes.id'), primary_key=True),
    # Segunda foreign key
    db.Column('clase_id', db.Integer, db.ForeignKey('clases.id'), primary_key=True),
    # Columnas adicionales opcionales
    db.Column('fecha_inscripcion', db.DateTime, default=datetime.utcnow)
)


class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    
    # secondary: Especifica la tabla intermedia
    # backref='estudiantes': Crea atributo en Clase
    # lazy='dynamic': Devuelve un query
    clases = db.relationship('Clase', 
                            secondary=inscripciones, 
                            backref='estudiantes', 
                            lazy='dynamic')


class Clase(db.Model):
    __tablename__ = 'clases'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    
    # No necesita relationship porque backref lo crea


# Uso:
# estudiante = Estudiante.query.get(1)
# estudiante.clases.all()  # Todas las clases del estudiante
# 
# clase = Clase.query.get(1)
# clase.estudiantes.all()  # Todos los estudiantes de la clase
# 
# # Agregar relación
# estudiante.clases.append(clase)
# db.session.commit()


# ============================================
# 3. One-to-One (Uno a Uno)
# ============================================
# Un usuario tiene un perfil
# Un perfil pertenece a un usuario

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    
    # uselist=False: Hace que la relación sea uno-a-uno en lugar de uno-a-muchos
    perfil = db.relationship('Perfil', backref='usuario', uselist=False, lazy=True)


class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    biografia = db.Column(db.Text)
    avatar = db.Column(db.String(200))
    
    # unique=True: Garantiza que cada perfil esté asociado a un solo usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True)


# Uso:
# usuario = Usuario.query.get(1)
# biografia = usuario.perfil.biografia  # Acceso directo (no es una lista)
```

### Opciones de `lazy` Loading

```python
# lazy='select' (default): Carga los datos cuando se accede por primera vez
# lazy='joined': Carga los datos con JOIN automático
# lazy='subquery': Carga los datos con subquery
# lazy='dynamic': Devuelve un query object (útil para filtrar)
# lazy='raise': Lanza error si se intenta acceder (previene N+1 queries)

# Ejemplo de uso con lazy='dynamic'
class Usuario(db.Model):
    posts = db.relationship('Post', backref='autor', lazy='dynamic')

# Permite filtrar y paginar
usuario = Usuario.query.get(1)
posts_publicados = usuario.posts.filter_by(publicado=True).limit(10).all()
```

---

## Consultas Avanzadas

```python
# app/routes.py - Ejemplos de consultas avanzadas

from sqlalchemy import and_, or_, not_, func, desc, asc

# ============================================
# Filtros básicos
# ============================================

# filter_by: Igualdad simple (más fácil de leer)
Usuario.query.filter_by(activo=True, nombre_completo='Juan Pérez').all()

# filter: Expresiones complejas
Usuario.query.filter(Usuario.activo == True).all()


# ============================================
# Operadores de comparación
# ============================================

# Igualdad
Usuario.query.filter(Usuario.username == 'admin').first()

# Desigualdad
Usuario.query.filter(Usuario.username != 'admin').all()

# Mayor que / Menor que
Post.query.filter(Post.id > 10).all()
Post.query.filter(Post.id < 100).all()

# Mayor o igual / Menor o igual
Post.query.filter(Post.id >= 10).all()

# IN (está en una lista)
Usuario.query.filter(Usuario.id.in_([1, 2, 3, 4])).all()

# NOT IN
Usuario.query.filter(~Usuario.id.in_([1, 2, 3])).all()

# LIKE (patrón de texto)
# %: cualquier secuencia de caracteres
Usuario.query.filter(Usuario.email.like('%@gmail.com')).all()

# ILIKE (LIKE case-insensitive, solo PostgreSQL)
Usuario.query.filter(Usuario.username.ilike('%admin%')).all()

# IS NULL
Usuario.query.filter(Usuario.nombre_completo == None).all()
Usuario.query.filter(Usuario.nombre_completo.is_(None)).all()

# IS NOT NULL
Usuario.query.filter(Usuario.nombre_completo != None).all()
Usuario.query.filter(Usuario.nombre_completo.isnot(None)).all()


# ============================================
# Operadores lógicos
# ============================================

# AND: todas las condiciones deben cumplirse
from sqlalchemy import and_
Usuario.query.filter(and_(
    Usuario.activo == True,
    Usuario.email.like('%@gmail.com')
)).all()

# Forma simplificada (and_ implícito)
Usuario.query.filter(
    Usuario.activo == True,
    Usuario.email.like('%@gmail.com')
).all()

# OR: al menos una condición debe cumplirse
from sqlalchemy import or_
Usuario.query.filter(or_(
    Usuario.username == 'admin',
    Usuario.email == 'admin@example.com'
)).all()

# NOT: niega una condición
from sqlalchemy import not_
Usuario.query.filter(not_(Usuario.activo == True)).all()
Usuario.query.filter(~(Usuario.activo == True)).all()  # Forma corta


# ============================================
# Ordenamiento
# ============================================

# ORDER BY ASC (ascendente)
Usuario.query.order_by(Usuario.username).all()
Usuario.query.order_by(Usuario.username.asc()).all()

# ORDER BY DESC (descendente)
Usuario.query.order_by(Usuario.fecha_creacion.desc()).all()

# Ordenar por múltiples columnas
Usuario.query.order_by(Usuario.activo.desc(), Usuario.username.asc()).all()


# ============================================
# Limitación y paginación
# ============================================

# LIMIT: limitar número de resultados
Usuario.query.limit(10).all()

# OFFSET: saltar registros
Usuario.query.offset(10).limit(10).all()

# Paginación (método recomendado)
# page: número de página (empieza en 1)
# per_page: registros por página
# error_out: lanzar error si la página no existe
paginacion = Usuario.query.paginate(page=1, per_page=20, error_out=False)
usuarios = paginacion.items  # Lista de usuarios
total_paginas = paginacion.pages  # Total de páginas
pagina_actual = paginacion.page  # Página actual
tiene_siguiente = paginacion.has_next  # Booleano
tiene_anterior = paginacion.has_prev  # Booleano


# ============================================
# Funciones de agregación
# ============================================

from sqlalchemy import func

# COUNT: contar registros
total_usuarios = db.session.query(func.count(Usuario.id)).scalar()
# O forma simplificada:
total_usuarios = Usuario.query.count()

# SUM: sumar valores
total_likes = db.session.query(func.sum(Post.likes)).scalar()

# AVG: promedio
promedio_likes = db.session.query(func.avg(Post.likes)).scalar()

# MAX: valor máximo
max_id = db.session.query(func.max(Usuario.id)).scalar()

# MIN: valor mínimo
min_fecha = db.session.query(func.min(Post.fecha_creacion)).scalar()


# ============================================
# GROUP BY y HAVING
# ============================================

# Contar posts por usuario
resultado = db.session.query(
    Usuario.username,
    func.count(Post.id).label('total_posts')
).join(Post).group_by(Usuario.id).all()

# HAVING: filtrar después de agrupar
# Usuarios con más de 5 posts
resultado = db.session.query(
    Usuario.username,
    func.count(Post.id).label('total_posts')
).join(Post).group_by(Usuario.id).having(func.count(Post.id) > 5).all()


# ============================================
# JOINS (unir tablas)
# ============================================

# INNER JOIN (solo registros que coinciden en ambas tablas)
resultado = db.session.query(Usuario, Post).join(Post).all()

# LEFT JOIN (todos los usuarios, aunque no tengan posts)
resultado = db.session.query(Usuario, Post).outerjoin(Post).all()

# Acceder a los datos del join
for usuario, post in resultado:
    print(f"Usuario: {usuario.username}, Post: {post.titulo if post else 'Sin posts'}")

# Join con filtro
usuarios_con_posts = db.session.query(Usuario).join(Post).filter(
    Post.publicado == True
).distinct().all()


# ============================================
# Subconsultas
# ============================================

# Encontrar usuarios que han publicado más de 3 posts
subquery = db.session.query(
    Post.usuario_id,
    func.count(Post.id).label('total')
).group_by(Post.usuario_id).having(func.count(Post.id) > 3).subquery()

usuarios_activos = db.session.query(Usuario).join(
    subquery, Usuario.id == subquery.c.usuario_id
).all()


# ============================================
# EXISTS
# ============================================

# Usuarios que tienen al menos un post publicado
from sqlalchemy import exists
stmt = exists().where(
    and_(Post.usuario_id == Usuario.id, Post.publicado == True)
)
usuarios = Usuario.query.filter(stmt).all()


# ============================================
# Consultas raw SQL (cuando sea necesario)
# ============================================

# Ejecutar SQL directamente
resultado = db.session.execute(
    "SELECT * FROM usuarios WHERE activo = :activo",
    {"activo": True}
)
usuarios = resultado.fetchall()

# Consulta raw que devuelve modelos
usuarios = Usuario.query.from_statement(
    db.text("SELECT * FROM usuarios WHERE activo = :activo")
).params(activo=True).all()


# ============================================
# Métodos útiles de Query
# ============================================

# .first(): Primer resultado o None
usuario = Usuario.query.filter_by(username='admin').first()

# .first_or_404(): Primer resultado o error 404
usuario = Usuario.query.filter_by(username='admin').first_or_404()

# .get(id): Buscar por primary key
usuario = Usuario.query.get(1)

# .get_or_404(id): Buscar por primary key o 404
usuario = Usuario.query.get_or_404(1)

# .all(): Todos los resultados
usuarios = Usuario.query.all()

# .one(): Exactamente un resultado (error si hay 0 o más de 1)
try:
    usuario = Usuario.query.filter_by(email='test@example.com').one()
except:
    # NoResultFound o MultipleResultsFound
    pass

# .one_or_none(): Un resultado o None (error si hay más de 1)
usuario = Usuario.query.filter_by(email='test@example.com').one_or_none()

# .count(): Contar resultados
total = Usuario.query.filter_by(activo=True).count()

# .scalar(): Primer elemento de la primera fila
username = db.session.query(Usuario.username).filter_by(id=1).scalar()

# .distinct(): Resultados únicos
emails = db.session.query(Usuario.email).distinct().all()
```

---

## Migraciones con Flask-Migrate

Las migraciones permiten modificar la estructura de la base de datos de forma incremental y controlada.

### Configuración Inicial

```bash
# 1. Inicializar Flask-Migrate (solo una vez por proyecto)
flask db init

# Esto crea la carpeta migrations/ con archivos de configuración
```

### Crear y Aplicar Migraciones

```bash
# 2. Crear una migración después de modificar los modelos
flask db migrate -m "Descripción del cambio"

# Ejemplos:
flask db migrate -m "Agregar tabla usuarios"
flask db migrate -m "Agregar columna telefono a usuarios"
flask db migrate -m "Crear relación entre usuarios y posts"

# Esto genera un archivo en migrations/versions/ con los cambios detectados


# 3. Revisar el archivo de migración generado
# Abre el archivo en migrations/versions/xxxx_descripcion.py
# Verifica que los cambios sean correctos


# 4. Aplicar la migración a la base de datos
flask db upgrade

# Este comando ejecuta todos los cambios pendientes


# 5. Revertir la última migración (si es necesario)
flask db downgrade

# O revertir a una versión específica
flask db downgrade <revision_id>


# Ver historial de migraciones
flask db history

# Ver migración actual
flask db current

# Ver todas las migraciones disponibles
flask db show
```

### Ejemplo de Archivo de Migración

```python
# migrations/versions/abc123_agregar_tabla_usuarios.py
"""Agregar tabla usuarios

Revision ID: abc123
Revises: 
Create Date: 2025-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abc123'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Función que se ejecuta al aplicar la migración (flask db upgrade)
    """
    # Crear tabla usuarios
    op.create_table('usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('activo', sa.Boolean(), nullable=True),
        sa.Column('fecha_creacion', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    # Crear índices
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    op.create_index(op.f('ix_usuarios_username'), 'usuarios', ['username'], unique=True)


def downgrade():
    """
    Función que se ejecuta al revertir la migración (flask db downgrade)
    """
    # Eliminar índices
    op.drop_index(op.f('ix_usuarios_username'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    # Eliminar tabla
    op.drop_table('usuarios')
```

### Operaciones Comunes en Migraciones

```python
# Agregar columna
op.add_column('usuarios', sa.Column('telefono', sa.String(20), nullable=True))

# Eliminar columna
op.drop_column('usuarios', 'telefono')

# Modificar columna
op.alter_column('usuarios', 'username',
    existing_type=sa.String(80),
    type_=sa.String(100),
    nullable=False
)

# Crear índice
op.create_index('idx_usuario_email', 'usuarios', ['email'])

# Eliminar índice
op.drop_index('idx_usuario_email', table_name='usuarios')

# Crear constraint
op.create_unique_constraint('uq_usuario_email', 'usuarios', ['email'])

# Eliminar constraint
op.drop_constraint('uq_usuario_email', 'usuarios', type_='unique')

# Renombrar tabla
op.rename_table('usuarios', 'users')

# Ejecutar SQL custom
op.execute('UPDATE usuarios SET activo = TRUE WHERE activo IS NULL')
```

---

## Live Templates para PyCharm

### Configurar Live Templates en PyCharm

1. Ve a **File → Settings → Editor → Live Templates**
2. Haz clic en el **+** para agregar un nuevo template
3. Selecciona **Template Group** y crea un grupo llamado "SQLAlchemy"
4. Dentro del grupo, agrega templates individuales

### Templates para Modelos

#### Template: `sqlmodel`
**Descripción**: Crear modelo SQLAlchemy completo

```python
class $MODEL_NAME$(db.Model):
    """
    $DESCRIPTION$
    """
    __tablename__ = '$TABLE_NAME
    
    id = db.Column(db.Integer, primary_key=True)
    $CURSOR$
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<$MODEL_NAME$ {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
```

**Variables**:
- `MODEL_NAME`: nombre de la clase
- `DESCRIPTION`: descripción del modelo
- `TABLE_NAME`: nombre de la tabla

---

#### Template: `sqlcol`
**Descripción**: Agregar columna SQLAlchemy

```python
$COLUMN_NAME$ = db.Column(db.$TYPE$($SIZE$), $OPTIONS$END$)
```

**Variables**:
- `COLUMN_NAME`: nombre de la columna
- `TYPE`: String, Integer, Boolean, etc.
- `SIZE`: tamaño (para String)
- `OPTIONS`: nullable=False, unique=True, etc.

---

#### Template: `sqlfk`
**Descripción**: Agregar foreign key

```python
$COLUMN_NAME$_id = db.Column(db.Integer, db.ForeignKey('$TABLE_NAME$.id'), nullable=False)
```

---

#### Template: `sqlrel`
**Descripción**: Definir relación

```python
$RELATION_NAME$ = db.relationship('$MODEL_NAME, backref='$BACKREF_NAME, lazy='dynamic')
```

---

### Templates para Rutas

#### Template: `flaskget`
**Descripción**: Ruta GET para obtener todos los registros

```python
@bp.route('/$ROUTE, methods=['GET'])
def obtener_$PLURAL$():
    """
    Obtiene todos los registros de $MODEL_NAME$
    """
    $VARIABLE$ = $MODEL_NAME$.query.all()
    return jsonify([$ITEM$.to_dict() for $ITEM$ in $VARIABLE$]), 200
```

---

#### Template: `flaskgetid`
**Descripción**: Ruta GET para obtener un registro por ID

```python
@bp.route('/$ROUTE$/<int:id>', methods=['GET'])
def obtener_$SINGULAR$(id):
    """
    Obtiene un registro específico de $MODEL_NAME$
    """
    $VARIABLE$ = $MODEL_NAME$.query.get_or_404(id)
    return jsonify($VARIABLE$.to_dict()), 200
```

---

#### Template: `flaskpost`
**Descripción**: Ruta POST para crear registro

```python
@bp.route('/$ROUTE, methods=['POST'])
def crear_$SINGULAR$():
    """
    Crea un nuevo registro de $MODEL_NAME$
    """
    data = request.get_json()
    
    nuevo_$VARIABLE$ = $MODEL_NAME$(
        $CURSOR$
    )
    
    try:
        db.session.add(nuevo_$VARIABLE$)
        db.session.commit()
        return jsonify(nuevo_$VARIABLE$.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
```

---

#### Template: `flaskput`
**Descripción**: Ruta PUT para actualizar registro

```python
@bp.route('/$ROUTE$/<int:id>', methods=['PUT'])
def actualizar_$SINGULAR$(id):
    """
    Actualiza un registro de $MODEL_NAME$
    """
    $VARIABLE$ = $MODEL_NAME$.query.get_or_404(id)
    data = request.get_json()
    
    try:
        $CURSOR$
        db.session.commit()
        return jsonify($VARIABLE$.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
```

---

#### Template: `flaskdel`
**Descripción**: Ruta DELETE para eliminar registro

```python
@bp.route('/$ROUTE$/<int:id>', methods=['DELETE'])
def eliminar_$SINGULAR$(id):
    """
    Elimina un registro de $MODEL_NAME$
    """
    $VARIABLE$ = $MODEL_NAME$.query.get_or_404(id)
    
    try:
        db.session.delete($VARIABLE$)
        db.session.commit()
        return jsonify({'mensaje': 'Registro eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
```

---

### Templates para Consultas

#### Template: `sqlquery`
**Descripción**: Query básico

```python
$VARIABLE$ = $MODEL$.query.filter_by($FIELD$=$VALUE$).$METHOD$()
```

**Opciones de METHOD**: `all()`, `first()`, `first_or_404()`, `count()`

---

#### Template: `sqlfilter`
**Descripción**: Query con filter

```python
$VARIABLE$ = $MODEL$.query.filter($MODEL$.$FIELD$ == $VALUE$).all()
```

---

#### Template: `sqljoin`
**Descripción**: Query con join

```python
$VARIABLE$ = db.session.query($MODEL1$, $MODEL2$).join($MODEL2$).filter($CONDITION$).all()
```

---

#### Template: `sqlpag`
**Descripción**: Paginación

```python
paginacion = $MODEL$.query.paginate(
    page=$PAGE$,
    per_page=$PER_PAGE$,
    error_out=False
)
$VARIABLE$ = paginacion.items
```

---

### Templates de Configuración

#### Template: `flaskapp`
**Descripción**: Estructura básica de app/__init__.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app import models
    from app.routes import bp
    app.register_blueprint(bp)
    
    with app.app_context():
        db.create_all()
    
    return app
```

---

#### Template: `flaskconfig`
**Descripción**: Archivo de configuración

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '$SECRET
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = $ECHO$
```

---

## 🎯 Mejores Prácticas

### 1. Manejo de Sesiones

```python
# ✅ CORRECTO: Usar try-except-finally
try:
    db.session.add(nuevo_usuario)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    raise e
finally:
    db.session.close()  # Solo si usas sesiones manuales

# ✅ CORRECTO: Usar context manager (Flask-SQLAlchemy lo maneja)
with db.session.begin():
    db.session.add(nuevo_usuario)
```

### 2. Evitar N+1 Queries

```python
# ❌ MALO: Causa N+1 queries
usuarios = Usuario.query.all()
for usuario in usuarios:
    print(usuario.posts.all())  # Query por cada usuario

# ✅ BUENO: Usar joinedload
from sqlalchemy.orm import joinedload

usuarios = Usuario.query.options(joinedload(Usuario.posts)).all()
for usuario in usuarios:
    print(usuario.posts)  # Sin queries adicionales
```

### 3. Validaciones

```python
class Usuario(db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    @validates('email')
    def validate_email(self, key, email):
        """Validar formato de email"""
        if '@' not in email:
            raise ValueError("Email inválido")
        return email.lower()
```

### 4. Métodos Útiles en Modelos

```python
class Usuario(db.Model):
    # ... columnas ...
    
    @classmethod
    def buscar_por_email(cls, email):
        """Método de clase para buscar usuario"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def crear(cls, **kwargs):
        """Método de clase para crear usuario"""
        usuario = cls(**kwargs)
        db.session.add(usuario)
        db.session.commit()
        return usuario
    
    def actualizar(self, **kwargs):
        """Método de instancia para actualizar"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
    
    def eliminar(self):
        """Método de instancia para eliminar"""
        db.session.delete(self)
        db.session.commit()
```

---

## 📝 Comandos Útiles

```bash
# Crear ambiente virtual
python -m venv venv

# Activar ambiente virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo requirements.txt
pip freeze > requirements.txt

# Ejecutar aplicación
flask run
# o
python run.py

# Abrir shell interactivo con contexto de Flask
flask shell

# Dentro del shell:
>>> from app import db
>>> from app.models import Usuario
>>> usuarios = Usuario.query.all()

# Crear base de datos desde cero
flask db init
flask db migrate -m "Inicial"
flask db upgrade

# Variables de entorno
export FLASK_APP=run.py
export FLASK_ENV=development
```

---

## 🔍 Debugging

```python
# Activar modo debug
app.config['DEBUG'] = True

# Ver SQL en consola
app.config['SQLALCHEMY_ECHO'] = True

# Inspeccionar query antes de ejecutar
query = Usuario.query.filter_by(activo=True)
print(str(query))  # Muestra el SQL que se ejecutará

# Usar el debugger
import pdb; pdb.set_trace()
```

---

## 📚 Recursos Adicionales

- [Documentación oficial de SQLAlchemy](https://docs.sqlalchemy.org/)
- [Documentación de Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)

---

## 💡 Troubleshooting Común

### Error: "No application found"
```python
# Asegúrate de tener FLASK_APP configurado
export FLASK_APP=run.py
```

### Error: "Table already exists"
```python
# Eliminar la base de datos y recrear
rm instance/app.db
flask db upgrade
```

### Error: "Foreign key constraint failed"
```python
# Verificar que el registro relacionado existe
usuario = Usuario.query.get(usuario_id)
if not usuario:
    return {"error": "Usuario no encontrado"}, 404
```

### Error: "Detached instance"
```python
# Volver a adjuntar el objeto a la sesión
db.session.add(usuario)
db.session.commit()
```

---

¡Listo! Esta guía cubre los conceptos fundamentales de SQLAlchemy con Flask. Practica creando tus propios modelos y experimenta con las consultas para dominar el ORM.