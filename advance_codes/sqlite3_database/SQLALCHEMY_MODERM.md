# Guía Completa SQLAlchemy 2.0+ (Sintaxis Moderna) con Flask

## 📚 Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Configuración Paso a Paso](#configuración-paso-a-paso)
5. [Modelos con Sintaxis Moderna](#modelos-con-sintaxis-moderna)
6. [Operaciones CRUD Completas](#operaciones-crud-completas)
7. [Consultas y Filtros](#consultas-y-filtros)
8. [Relaciones entre Tablas](#relaciones-entre-tablas)
9. [Live Templates para PyCharm](#live-templates-para-pycharm)
10. [Ejemplos Prácticos Completos](#ejemplos-prácticos-completos)

---

## Introducción

Esta guía usa **SQLAlchemy 2.0+** con su sintaxis moderna que incluye:
- ✅ `Mapped[]` para type hints
- ✅ `mapped_column()` en lugar de `Column()`
- ✅ `DeclarativeBase` como clase base
- ✅ Mejor autocompletado en IDEs
- ✅ Código más claro y mantenible

**¿Por qué esta sintaxis?**
- Más segura: Python detecta errores de tipos antes de ejecutar
- Mejor experiencia: Tu IDE te ayuda con sugerencias
- Más moderna: Es el estándar de SQLAlchemy 2.0+

---

## Instalación

```bash
# Crear ambiente virtual
python -m venv venv

# Activar ambiente virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar paquetes necesarios
pip install flask
pip install flask-sqlalchemy
pip install python-dotenv

# Crear archivo requirements.txt
pip freeze > requirements.txt
```

**Archivo `requirements.txt`:**
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
python-dotenv==1.0.0
SQLAlchemy==2.0.23
```

---

## Estructura del Proyecto

```
mi_proyecto/
│
├── app/
│   ├── __init__.py          # Inicialización de Flask y SQLAlchemy
│   ├── models.py            # Modelos (tablas)
│   ├── routes.py            # Rutas y lógica
│   └── config.py            # Configuración
│
├── instance/                # Base de datos SQLite (auto-generada)
│   └── app.db
│
├── templates/               # HTML templates (opcional)
├── static/                  # CSS, JS, imágenes (opcional)
├── .env                     # Variables de entorno
├── .gitignore              # Archivos a ignorar en git
├── requirements.txt         # Dependencias
└── run.py                   # Punto de entrada
```

---

## Configuración Paso a Paso

### 1. Archivo `.env`

```bash
# .env - Variables de entorno (NO subir a git)

# Clave secreta para sesiones (genera una aleatoria)
SECRET_KEY=tu-clave-super-secreta-cambiala

# URL de la base de datos SQLite
DATABASE_URL=sqlite:///instance/app.db

# Ambiente de desarrollo
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
```

---

### 2. Archivo `app/config.py`

```python
# app/config.py
import os
from dotenv import load_dotenv

# Cargar variables desde .env
# load_dotenv(): Lee el archivo .env y carga las variables
load_dotenv()

class Config:
    """
    Clase de configuración para Flask y SQLAlchemy
    Todas las configuraciones de la app se centralizan aquí
    """
    
    # SECRET_KEY: Clave para encriptar sesiones y cookies
    # os.environ.get(): Obtiene variable de entorno
    # Si no existe, usa el valor después de 'or'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-por-defecto-insegura'
    
    # SQLALCHEMY_DATABASE_URI: Ubicación de la base de datos
    # Format SQLite: sqlite:///ruta/al/archivo.db
    # sqlite:/// significa base de datos local (3 barras)
    # sqlite://// sería ruta absoluta (4 barras)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                                     '..', 'instance', 'app.db')
    
    # SQLALCHEMY_TRACK_MODIFICATIONS: Sistema de señales de cambios
    # False: Desactivado (ahorra memoria y recursos)
    # True: Activado (solo si necesitas rastrear cada cambio)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLALCHEMY_ECHO: Mostrar SQL en consola
    # True: Muestra cada query SQL ejecutado (útil para aprender/debug)
    # False: No muestra nada (usar en producción)
    SQLALCHEMY_ECHO = True


# Configuración para desarrollo (puedes crear más)
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


# Configuración para producción
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
```

**Explicación de `os.path`:**
```python
# os.path.dirname(__file__): Directorio del archivo actual (config.py)
# os.path.abspath(): Convierte a ruta absoluta
# os.path.join(): Une partes de una ruta de forma segura
# '..': Sube un nivel en la jerarquía de carpetas

# Ejemplo:
# Si estás en: /home/user/proyecto/app/config.py
# dirname(__file__) = /home/user/proyecto/app
# '..' sube a = /home/user/proyecto
# 'instance' = /home/user/proyecto/instance
# 'app.db' = /home/user/proyecto/instance/app.db
```

---

### 3. Archivo `app/__init__.py`

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from app.config import Config

# ============================================
# PASO 1: Crear clase base para modelos
# ============================================
class Base(DeclarativeBase):
    """
    Clase base de la que heredarán todos los modelos
    
    DeclarativeBase: Clase especial de SQLAlchemy 2.0+
    pass: No necesita código adicional, solo existir
    
    Todos tus modelos (Usuario, Post, etc.) heredarán de esta clase
    """
    pass


# ============================================
# PASO 2: Crear instancia de SQLAlchemy
# ============================================
# db: Objeto que maneja TODA la comunicación con la base de datos
# model_class=Base: Le dice a SQLAlchemy que use nuestra clase Base
db = SQLAlchemy(model_class=Base)


# ============================================
# PASO 3: Factory Function (Función Fábrica)
# ============================================
def create_app(config_class=Config):
    """
    Factory function para crear y configurar la aplicación Flask
    
    ¿Por qué una función?
    - Permite crear múltiples instancias de la app
    - Facilita testing
    - Organiza mejor el código
    
    Args:
        config_class: Clase de configuración a usar
    
    Returns:
        app: Instancia configurada de Flask
    """
    
    # Crear instancia de Flask
    # __name__: Nombre del módulo actual
    app = Flask(__name__)
    
    # Cargar configuración desde la clase Config
    # app.config: Diccionario de configuración
    # from_object(): Carga todas las variables de la clase
    app.config.from_object(config_class)
    
    # Conectar SQLAlchemy con Flask
    # Ahora db sabe qué aplicación Flask usar
    db.init_app(app)
    
    # Importar modelos DESPUÉS de crear db
    # Esto evita importaciones circulares
    from app import models
    
    # Registrar rutas (blueprints)
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Crear tablas en la base de datos
    # app.app_context(): Activa el contexto de la aplicación
    # db.create_all(): Crea las tablas si no existen
    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada")
    
    return app
```

**¿Qué es el contexto de aplicación?**
```python
# Flask usa contextos para saber qué app está activa
# Necesario cuando tienes múltiples apps o trabajas fuera de rutas

# OPCIÓN 1: Usar with (recomendado)
with app.app_context():
    # Aquí Flask sabe qué app usar
    db.create_all()

# OPCIÓN 2: Activar manualmente (rara vez necesario)
ctx = app.app_context()
ctx.push()
db.create_all()
ctx.pop()
```

---

### 4. Archivo `run.py`

```python
# run.py - Punto de entrada de la aplicación
from app import create_app

# Crear la aplicación usando la factory function
app = create_app()

# Solo ejecutar si este archivo se ejecuta directamente
# No se ejecuta si se importa desde otro archivo
if __name__ == '__main__':
    # Ejecutar servidor de desarrollo de Flask
    # debug=True: Recarga automáticamente al cambiar código
    # host='0.0.0.0': Accesible desde otras computadoras en la red
    # port=5000: Puerto donde corre la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Ejecutar la aplicación:**
```bash
# Opción 1: Directamente
python run.py

# Opción 2: Con flask command
flask run

# La aplicación estará en: http://localhost:5000
```

---

## Modelos con Sintaxis Moderna

### Archivo `app/models.py`

```python
# app/models.py
from app import db
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# ============================================
# MODELO BÁSICO: Usuario
# ============================================
class Usuario(db.Model):
    """
    Modelo Usuario - Representa la tabla 'usuario' en la base de datos
    
    SINTAXIS MODERNA:
    - Mapped[tipo]: Declara el tipo de dato en Python
    - mapped_column(): Define la columna en la base de datos
    """
    
    # __tablename__: Nombre explícito de la tabla (opcional)
    # Si no se define, SQLAlchemy usa el nombre de la clase en minúscula
    __tablename__ = 'usuario'
    
    # ============================================
    # COLUMNA: id (Clave Primaria)
    # ============================================
    # Mapped[int]: Tipo en Python (entero)
    # mapped_column(): Función que crea la columna
    # Integer: Tipo en la base de datos
    # primary_key=True: Esta es la clave primaria (identificador único)
    # autoincrement=True: Se incrementa automáticamente (1, 2, 3...)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # ============================================
    # COLUMNA: username (Nombre de usuario)
    # ============================================
    # String(80): Texto de máximo 80 caracteres
    # unique=True: No puede haber duplicados
    # nullable=False: Campo obligatorio (no puede ser NULL)
    # index=True: Crea índice para búsquedas rápidas
    username: Mapped[str] = mapped_column(
        String(80), 
        unique=True, 
        nullable=False, 
        index=True
    )
    
    # ============================================
    # COLUMNA: email
    # ============================================
    email: Mapped[str] = mapped_column(
        String(120), 
        unique=True, 
        nullable=False, 
        index=True
    )
    
    # ============================================
    # COLUMNA: password_hash (Contraseña encriptada)
    # ============================================
    # Optional[str]: Puede ser str o None
    # nullable=True: Campo opcional (puede ser NULL)
    password_hash: Mapped[Optional[str]] = mapped_column(
        String(255), 
        nullable=True
    )
    
    # ============================================
    # COLUMNA: nombre_completo
    # ============================================
    nombre_completo: Mapped[Optional[str]] = mapped_column(
        String(200), 
        nullable=True
    )
    
    # ============================================
    # COLUMNA: edad
    # ============================================
    # Integer: Número entero
    edad: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # ============================================
    # COLUMNA: activo (Estado del usuario)
    # ============================================
    # Boolean: True o False
    # default=True: Valor por defecto si no se especifica
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # ============================================
    # COLUMNA: fecha_creacion
    # ============================================
    # DateTime: Fecha y hora
    # default=datetime.utcnow: Función que se ejecuta al crear
    # IMPORTANTE: Sin paréntesis (datetime.utcnow, no datetime.utcnow())
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow
    )
    
    # ============================================
    # COLUMNA: fecha_actualizacion
    # ============================================
    # onupdate=datetime.utcnow: Se actualiza automáticamente al modificar
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    
    # ============================================
    # RELACIÓN: posts (One-to-Many)
    # ============================================
    # relationship(): Define relación con otra tabla
    # back_populates='autor': Nombre del atributo en la otra clase
    # lazy='dynamic': Devuelve query en lugar de lista (permite filtrar)
    # cascade='all, delete-orphan': Elimina posts si se elimina usuario
    posts: Mapped[list["Post"]] = relationship(
        back_populates='autor', 
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    # ============================================
    # MÉTODO: __repr__ (Representación del objeto)
    # ============================================
    def __repr__(self) -> str:
        """
        Define cómo se ve el objeto cuando lo imprimes
        
        Ejemplo:
        usuario = Usuario.query.get(1)
        print(usuario)  # Output: <Usuario: juan_perez>
        """
        return f'<Usuario: {self.username}>'
    
    # ============================================
    # MÉTODO: to_dict (Convertir a diccionario)
    # ============================================
    def to_dict(self) -> dict:
        """
        Convierte el objeto a diccionario
        Útil para enviar datos en formato JSON
        
        Returns:
            dict: Diccionario con los datos del usuario
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nombre_completo': self.nombre_completo,
            'edad': self.edad,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }


# ============================================
# MODELO: Post (Publicación)
# ============================================
class Post(db.Model):
    """
    Modelo Post - Representa una publicación o artículo
    Tiene relación Many-to-One con Usuario
    """
    __tablename__ = 'post'
    
    # Clave primaria
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Título del post
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # Contenido del post
    # Text: Texto largo sin límite específico
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Estado de publicación
    publicado: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Número de likes
    likes: Mapped[int] = mapped_column(Integer, default=0)
    
    # Fecha de creación
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow
    )
    
    # ============================================
    # FOREIGN KEY: usuario_id
    # ============================================
    # ForeignKey('usuario.id'): Referencia a la columna id de la tabla usuario
    # nullable=False: Un post DEBE pertenecer a un usuario
    usuario_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('usuario.id'), 
        nullable=False
    )
    
    # ============================================
    # RELACIÓN: autor (Many-to-One)
    # ============================================
    # Mapped["Usuario"]: Tipo de la relación (como string por forward reference)
    # back_populates='posts': Conecta con el atributo 'posts' en Usuario
    autor: Mapped["Usuario"] = relationship(back_populates='posts')
    
    def __repr__(self) -> str:
        return f'<Post: {self.titulo}>'
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'titulo': self.titulo,
            'contenido': self.contenido,
            'publicado': self.publicado,
            'likes': self.likes,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'usuario_id': self.usuario_id,
            'autor': self.autor.username if self.autor else None
        }


# ============================================
# TIPOS DE DATOS MÁS COMUNES
# ============================================
"""
NÚMEROS:
- Integer: Números enteros (-2, -1, 0, 1, 2, 100)
- Float: Números decimales (9.5, 3.14, 100.0)
- Numeric(precision, scale): Decimales con precisión exacta
  Ejemplo: Numeric(10, 2) = 12345678.90 (10 dígitos, 2 decimales)

TEXTO:
- String(n): Texto de longitud fija (máximo n caracteres)
- Text: Texto de longitud variable (sin límite específico)

FECHA Y HORA:
- Date: Solo fecha (2025-01-15)
- Time: Solo hora (14:30:00)
- DateTime: Fecha y hora completa (2025-01-15 14:30:00)

BOOLEANOS:
- Boolean: True o False

BINARIOS:
- LargeBinary: Datos binarios (imágenes, PDFs, etc.)

JSON:
- JSON: Datos en formato JSON (solo PostgreSQL y MySQL 5.7+)
"""
```

---

## Operaciones CRUD Completas

### Archivo `app/routes.py`

```python
# app/routes.py
from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import Usuario, Post
from sqlalchemy import select, and_, or_, not_, func, desc, asc

# ============================================
# CREAR BLUEPRINT
# ============================================
# Blueprint: Forma de organizar rutas en módulos
# 'main': Nombre del blueprint
# __name__: Nombre del módulo actual
bp = Blueprint('main', __name__)


# ============================================
# RUTA PRINCIPAL
# ============================================
@bp.route('/')
def index():
    """Ruta de inicio"""
    return jsonify({
        'mensaje': 'API de Usuarios y Posts',
        'endpoints': {
            'usuarios': '/usuarios',
            'posts': '/posts'
        }
    })


# ============================================
# CREATE - Crear Usuario
# ============================================
@bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    """
    Crea un nuevo usuario en la base de datos
    
    Request Body (JSON):
    {
        "username": "juan123",
        "email": "juan@example.com",
        "nombre_completo": "Juan Pérez",
        "edad": 25
    }
    
    Returns:
        JSON con los datos del usuario creado
    """
    # Obtener datos del request
    # request.get_json(): Convierte JSON a diccionario Python
    data = request.get_json()
    
    # Validar datos obligatorios
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'username y email son obligatorios'}), 400
    
    # Crear instancia del modelo Usuario
    # Los datos se pasan como argumentos con nombre (keyword arguments)
    nuevo_usuario = Usuario(
        username=data.get('username'),
        email=data.get('email'),
        nombre_completo=data.get('nombre_completo'),
        edad=data.get('edad')
    )
    
    try:
        # PASO 1: Agregar objeto a la sesión
        # La sesión es como un "carrito" de cambios pendientes
        # Todavía NO está en la base de datos
        db.session.add(nuevo_usuario)
        
        # PASO 2: Confirmar cambios
        # Aquí se ejecuta el INSERT en la base de datos
        # El usuario recibe su ID automáticamente después del commit
        db.session.commit()
        
        # Responder con éxito (código 201 = Created)
        return jsonify(nuevo_usuario.to_dict()), 201
    
    except Exception as e:
        # Si hay error, revertir cambios
        # rollback(): Cancela todos los cambios pendientes
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ============================================
# READ - Obtener Todos los Usuarios
# ============================================
@bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    """
    Obtiene lista de todos los usuarios
    
    Returns:
        JSON con lista de usuarios
    """
    # OPCIÓN 1: Sintaxis clásica (recomendada para simplicidad)
    # Usuario.query: Objeto Query para hacer consultas
    # .all(): Ejecuta y devuelve todos los resultados
    # SQL equivalente: SELECT * FROM usuario
    usuarios = Usuario.query.all()
    
    # OPCIÓN 2: Sintaxis moderna SQLAlchemy 2.0 (más explícita)
    # stmt = select(Usuario)
    # usuarios = db.session.execute(stmt).scalars().all()
    
    # Convertir cada usuario a diccionario
    # List comprehension: [acción for item in lista]
    return jsonify([usuario.to_dict() for usuario in usuarios]), 200


# ============================================
# READ - Obtener Usuario por ID
# ============================================
@bp.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    """
    Obtiene un usuario específico por su ID
    
    Args:
        id: ID del usuario (se extrae de la URL)
        <int:id> significa que debe ser un número entero
    
    Returns:
        JSON con los datos del usuario
    """
    # .get_or_404(id): Busca por clave primaria
    # Si no encuentra, devuelve error 404 automáticamente
    # SQL equivalente: SELECT * FROM usuario WHERE id = ?
    usuario = Usuario.query.get_or_404(id)
    
    return jsonify(usuario.to_dict()), 200


# ============================================
# UPDATE - Actualizar Usuario
# ============================================
@bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    """
    Actualiza los datos de un usuario existente
    
    Request Body (JSON):
    {
        "nombre_completo": "Juan Carlos Pérez",
        "edad": 26,
        "activo": true
    }
    
    Returns:
        JSON con los datos actualizados
    """
    # Buscar usuario existente
    usuario = Usuario.query.get_or_404(id)
    
    # Obtener nuevos datos
    data = request.get_json()
    
    try:
        # Actualizar solo los campos que se envían
        # .get(key, default): Obtiene valor o devuelve default si no existe
        if 'username' in data:
            usuario.username = data['username']
        if 'email' in data:
            usuario.email = data['email']
        if 'nombre_completo' in data:
            usuario.nombre_completo = data['nombre_completo']
        if 'edad' in data:
            usuario.edad = data['edad']
        if 'activo' in data:
            usuario.activo = data['activo']
        
        # No necesitas hacer add() porque el objeto ya está en la sesión
        # Solo commit() para guardar cambios
        # SQL equivalente: UPDATE usuario SET ... WHERE id = ?
        db.session.commit()
        
        return jsonify(usuario.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ============================================
# DELETE - Eliminar Usuario
# ============================================
@bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    """
    Elimina un usuario de la base de datos
    
    IMPORTANTE: Por la cascada 'delete-orphan', también elimina
    todos los posts asociados al usuario
    
    Returns:
        JSON con mensaje de confirmación
    """
    usuario = Usuario.query.get_or_404(id)
    
    try:
        # Marcar objeto para eliminación
        db.session.delete(usuario)
        
        # Ejecutar DELETE en la base de datos
        # SQL equivalente: DELETE FROM usuario WHERE id = ?
        db.session.commit()
        
        return jsonify({'mensaje': f'Usuario {usuario.username} eliminado'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ============================================
# CREATE - Crear Post
# ============================================
@bp.route('/usuarios/<int:usuario_id>/posts', methods=['POST'])
def crear_post(usuario_id):
    """
    Crea un post asociado a un usuario
    
    Args:
        usuario_id: ID del usuario que crea el post
    
    Request Body (JSON):
    {
        "titulo": "Mi primer post",
        "contenido": "Este es el contenido del post",
        "publicado": true
    }
    """
    # Verificar que el usuario existe
    usuario = Usuario.query.get_or_404(usuario_id)
    
    data = request.get_json()
    
    # Validar datos obligatorios
    if not data or not data.get('titulo') or not data.get('contenido'):
        return jsonify({'error': 'titulo y contenido son obligatorios'}), 400
    
    nuevo_post = Post(
        titulo=data.get('titulo'),
        contenido=data.get('contenido'),
        publicado=data.get('publicado', False),  # False por defecto
        usuario_id=usuario_id  # Foreign key
    )
    
    try:
        db.session.add(nuevo_post)
        db.session.commit()
        
        return jsonify(nuevo_post.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ============================================
# READ - Obtener Posts de un Usuario
# ============================================
@bp.route('/usuarios/<int:usuario_id>/posts', methods=['GET'])
def obtener_posts_usuario(usuario_id):
    """
    Obtiene todos los posts de un usuario específico
    
    Aprovecha la relación definida en el modelo
    """
    usuario = Usuario.query.get_or_404(usuario_id)
    
    # Acceder a la relación 'posts'
    # Como lazy='dynamic', devuelve un query que podemos filtrar
    posts = usuario.posts.all()
    
    return jsonify([post.to_dict() for post in posts]), 200


# ============================================
# UPDATE - Dar Like a un Post
# ============================================
@bp.route('/posts/<int:id>/like', methods=['POST'])
def dar_like(id):
    """
    Incrementa los likes de un post
    
    Ejemplo de actualización simple de un campo
    """
    post = Post.query.get_or_404(id)
    
    try:
        # Incrementar likes
        post.likes += 1
        
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Like agregado',
            'likes': post.likes
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
```

---

## Consultas y Filtros

```python
# app/routes.py - Continúa...

# ============================================
# CONSULTAS BÁSICAS
# ============================================

@bp.route('/ejemplos/consultas-basicas', methods=['GET'])
def consultas_basicas():
    """
    Ejemplos de consultas básicas más usadas
    """
    
    # 1. Obtener TODOS los registros
    # SQL: SELECT * FROM usuario
    todos = Usuario.query.all()
    
    # 2. Obtener el PRIMER registro
    # SQL: SELECT * FROM usuario LIMIT 1
    primero = Usuario.query.first()
    
    # 3. Obtener por ID (clave primaria)
    # SQL: SELECT * FROM usuario WHERE id = 1
    usuario = Usuario.query.get(1)
    
    # 4. Obtener por ID o error 404
    usuario = Usuario.query.get_or_404(1)
    
    # 5. Contar registros
    # SQL: SELECT COUNT(*) FROM usuario
    total = Usuario.query.count()
    
    # 6. Verificar si existe
    existe = Usuario.query.filter_by(username='admin').first() is not None
    
    return jsonify({
        'total_usuarios': total,
        'primer_usuario': primero.username if primero else None,
        'existe_admin': existe
    })


# ============================================
# FILTROS CON filter_by() - Igualdad Simple
# ============================================

@bp.route('/ejemplos/filter-by', methods=['GET'])
def ejemplos_filter_by():
    """
    filter_by(): Para comparaciones de igualdad simples
    Sintaxis más fácil de leer
    """
    
    # 1. Filtrar por UN campo
    # SQL: SELECT * FROM usuario WHERE username = 'admin'
    admin = Usuario.query.filter_by(username='admin').first()
    
    # 2. Filtrar por MÚLTIPLES campos (AND implícito)
    # SQL: SELECT * FROM usuario WHERE activo = 1 AND edad = 25
    usuarios = Usuario.query.filter_by(activo=True, edad=25).all()
    
    # 3. Filtrar y contar
    # SQL: SELECT COUNT(*) FROM usuario WHERE activo = 1
    usuarios_activos = Usuario.query.filter_by(activo=True).count()
    
    # 4. Filtrar y obtener el primero
    usuario = Usuario.query.filter_by(email='test@example.com').first()
    
    return jsonify({
        'admin': admin.to_dict() if admin else None,
        'usuarios_25': len(usuarios),
        'activos': usuarios_activos
    })


# ============================================
# FILTROS CON filter() - Expresiones Complejas
# ============================================

@bp.route('/ejemplos/filter', methods=['GET'])
def ejemplos_filter():
    """
    filter(): Para comparaciones complejas
    Usa operadores de SQLAlchemy
    """
    
    # 1. IGUALDAD (==)
    # SQL: SELECT * FROM usuario WHERE username = 'admin'
    usuario = Usuario.query.filter(Usuario.username == 'admin').first()
    
    # 2. DESIGUALDAD (!=)
    # SQL: SELECT * FROM usuario WHERE username != 'admin'
    no_admin = Usuario.query.filter(Usuario.username != 'admin').all()
    
    # 3. MAYOR QUE (>)
    # SQL: SELECT * FROM usuario WHERE edad > 18
    mayores = Usuario.query.filter(Usuario.edad > 18).all()
    
    # 4. MENOR QUE (<)
    # SQL: SELECT * FROM usuario WHERE edad < 30
    menores = Usuario.query.filter(Usuario.edad < 30).all()
    
    # 5. MAYOR O IGUAL (>=)
    # SQL: SELECT * FROM usuario WHERE edad >= 18
    adultos = Usuario.query.filter(Usuario.edad >= 18).all()
    
    # 6. MENOR O IGUAL (<=)
    # SQL: SELECT * FROM usuario WHERE edad <= 65
    no_seniors = Usuario.query.filter(Usuario.edad <= 65).all()
    
    return jsonify({
        'mayores_18': len(mayores),
        'menores_30': len(menores)
    })


# ============================================
# OPERADORES ESPECIALES
# ============================================

@bp.route('/ejemplos/operadores-especiales', methods=['GET'])
def operadores_especiales():
    """
    Operadores especiales más usados
    """
    
    # 1. LIKE - Búsqueda de patrones
    # % = cualquier cantidad de caracteres
    # _ = un solo carácter
    
    # Buscar usuarios cuyo email termine en @gmail.com
    # SQL: SELECT * FROM usuario WHERE email LIKE '%@gmail.com'
    gmail = Usuario.query.filter(Usuario.email.like('%@gmail.com')).all()
    
    # Buscar usuarios cuyo nombre empiece con "Juan"
    # SQL: SELECT * FROM usuario WHERE nombre_completo LIKE 'Juan%'
    juanes = Usuario.query.filter(Usuario.nombre_completo.like('Juan%')).all()
    
    # Buscar usuarios con "carlos" en cualquier parte del nombre
    # SQL: SELECT * FROM usuario WHERE nombre_completo LIKE '%carlos%'
    carlos = Usuario.query.filter(Usuario.nombre_completo.like('%carlos%')).all()
    
    # 2. ILIKE - LIKE case-insensitive (solo PostgreSQL)
    # Busca sin importar mayúsculas/minúsculas
    # usuarios = Usuario.query.filter(Usuario.username.ilike('%admin%')).all()
    
    # 3. IN - Está en una lista
    # SQL: SELECT * FROM usuario WHERE id IN (1, 2, 3)
    ids = [1, 2, 3]
    usuarios = Usuario.query.filter(Usuario.id.in_(ids)).all()
    
    # 4. NOT IN - No está en una lista
    # SQL: SELECT * FROM usuario WHERE id NOT IN (1, 2, 3)
    # Usando ~ (operador NOT)
    otros = Usuario.query.filter(~Usuario.id.in_(ids)).all()
    
    # 5. IS NULL - Campo vacío
    # SQL: SELECT * FROM usuario WHERE nombre_completo IS NULL
    sin_nombre = Usuario.query.filter(Usuario.nombre_completo == None).all()
    # O forma explícita:
    sin_nombre = Usuario.query.filter(Usuario.nombre_completo.is_(None)).all()
    
    # 6. IS NOT NULL - Campo no vacío
    # SQL: SELECT * FROM usuario WHERE nombre_completo IS NOT NULL
    con_nombre = Usuario.query.filter(Usuario.nombre_completo != None).all()
    # O forma explícita:
    con_nombre = Usuario.query.filter(Usuario.nombre_completo.isnot(None)).all()
    
    # 7. BETWEEN - Entre dos valores
    # SQL: SELECT * FROM usuario WHERE edad BETWEEN 18 AND 30
    rango = Usuario.query.filter(Usuario.edad.between(18, 30)).all()
    
    return jsonify({
        'gmail_users': len(gmail),
        'usuarios_in_ids': len(usuarios),
        'edad_18_30': len(rango)
    })


# ============================================
# OPERADORES LÓGICOS: AND, OR, NOT
# ============================================

@bp.route('/ejemplos/logicos', methods=['GET'])
def operadores_logicos():
    """
    Combinar múltiples condiciones
    """
    
    # 1. AND - Todas las condiciones deben cumplirse
    
    # Forma 1: Múltiples filter() (AND implícito)
    # SQL: SELECT * FROM usuario WHERE activo = 1 AND edad > 18
    usuarios = Usuario.query.filter(Usuario.activo == True).filter(Usuario.edad > 18).all()
    
    # Forma 2: Múltiples condiciones separadas por comas (AND implícito)
    usuarios = Usuario.query.filter(Usuario.activo == True, Usuario.edad > 18).all()
    
    # Forma 3: Usando and_() explícito (más claro para condiciones complejas)
    from sqlalchemy import and_
    usuarios = Usuario.query.filter(and_(
        Usuario.activo == True,
        Usuario.edad > 18,
        Usuario.email.like('%@gmail.com')
    )).all()
    
    # 2. OR - Al menos una condición debe cumplirse
    
    # SQL: SELECT * FROM usuario WHERE username = 'admin' OR email = 'admin@example.com'
    from sqlalchemy import or_
    admin = Usuario.query.filter(or_(
        Usuario.username == 'admin',
        Usuario.email == 'admin@example.com'
    )).first()
    
    # OR con múltiples condiciones
    # SQL: SELECT * FROM usuario WHERE edad < 18 OR edad > 65
    extremos = Usuario.query.filter(or_(
        Usuario.edad < 18,
        Usuario.edad > 65
    )).all()
    
    # 3. NOT - Negar una condición
    
    # Forma 1: Usando ~ (operador NOT de Python)
    # SQL: SELECT * FROM usuario WHERE NOT (activo = 1)
    inactivos = Usuario.query.filter(~(Usuario.activo == True)).all()
    
    # Forma 2: Usando not_() explícito
    from sqlalchemy import not_
    inactivos = Usuario.query.filter(not_(Usuario.activo == True)).all()
    
    # 4. COMBINACIONES COMPLEJAS
    
    # AND dentro de OR
    # SQL: SELECT * FROM usuario WHERE (edad > 18 AND activo = 1) OR username = 'admin'
    usuarios = Usuario.query.filter(or_(
        and_(Usuario.edad > 18, Usuario.activo == True),
        Usuario.username == 'admin'
    )).all()
    
    return jsonify({
        'adultos_activos': len(usuarios),
        'extremos_edad': len(extremos)
    })


# ============================================
# ORDENAMIENTO: order_by()
# ============================================

@bp.route('/ejemplos/ordenamiento', methods=['GET'])
def ordenamiento():
    """
    Ordenar resultados
    """
    
    # 1. Orden ASCENDENTE (A-Z, 0-9)
    # SQL: SELECT * FROM usuario ORDER BY username ASC
    por_nombre = Usuario.query.order_by(Usuario.username).all()
    # O explícito:
    por_nombre = Usuario.query.order_by(Usuario.username.asc()).all()
    
    # 2. Orden DESCENDENTE (Z-A, 9-0)
    # SQL: SELECT * FROM usuario ORDER BY fecha_creacion DESC
    mas_recientes = Usuario.query.order_by(Usuario.fecha_creacion.desc()).all()
    
    # 3. Ordenar por MÚLTIPLES columnas
    # SQL: SELECT * FROM usuario ORDER BY activo DESC, username ASC
    ordenado = Usuario.query.order_by(
        Usuario.activo.desc(),  # Primero activos
        Usuario.username.asc()   # Luego por nombre
    ).all()
    
    # 4. Ordenar con filtro
    # SQL: SELECT * FROM usuario WHERE activo = 1 ORDER BY edad DESC
    activos = Usuario.query.filter_by(activo=True).order_by(Usuario.edad.desc()).all()
    
    # 5. Ordenar posts por likes
    top_posts = Post.query.order_by(Post.likes.desc()).limit(10).all()
    
    return jsonify({
        'primer_usuario': por_nombre[0].username if por_nombre else None,
        'usuario_mas_reciente': mas_recientes[0].username if mas_recientes else None,
        'top_posts': [p.to_dict() for p in top_posts]
    })


# ============================================
# LIMITACIÓN Y PAGINACIÓN
# ============================================

@bp.route('/ejemplos/paginacion', methods=['GET'])
def paginacion():
    """
    Limitar resultados y paginar
    """
    
    # 1. LIMIT - Limitar cantidad de resultados
    # SQL: SELECT * FROM usuario LIMIT 10
    primeros_10 = Usuario.query.limit(10).all()
    
    # 2. OFFSET - Saltar registros
    # SQL: SELECT * FROM usuario OFFSET 10
    despues_10 = Usuario.query.offset(10).limit(10).all()
    
    # 3. PAGINACIÓN MANUAL
    # Página 2, 10 registros por página
    pagina = 2
    por_pagina = 10
    usuarios = Usuario.query.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
    
    # 4. PAGINACIÓN CON .paginate() (RECOMENDADO)
    # request.args.get(): Obtiene parámetros de URL (?page=2&per_page=10)
    pagina = request.args.get('page', 1, type=int)
    por_pagina = request.args.get('per_page', 10, type=int)
    
    # paginate(): Método especial de Flask-SQLAlchemy
    paginacion = Usuario.query.paginate(
        page=pagina,           # Número de página (empieza en 1)
        per_page=por_pagina,   # Registros por página
        error_out=False        # No lanzar error si página no existe
    )
    
    return jsonify({
        'usuarios': [u.to_dict() for u in paginacion.items],
        'total': paginacion.total,           # Total de registros
        'paginas': paginacion.pages,         # Total de páginas
        'pagina_actual': paginacion.page,    # Página actual
        'tiene_siguiente': paginacion.has_next,    # ¿Hay página siguiente?
        'tiene_anterior': paginacion.has_prev,     # ¿Hay página anterior?
        'pagina_siguiente': paginacion.next_num,   # Número de página siguiente
        'pagina_anterior': paginacion.prev_num     # Número de página anterior
    })


# ============================================
# FUNCIONES DE AGREGACIÓN
# ============================================

@bp.route('/ejemplos/agregacion', methods=['GET'])
def funciones_agregacion():
    """
    Funciones matemáticas sobre columnas
    """
    from sqlalchemy import func
    
    # 1. COUNT - Contar registros
    # SQL: SELECT COUNT(*) FROM usuario
    total_usuarios = db.session.query(func.count(Usuario.id)).scalar()
    # O forma simple:
    total_usuarios = Usuario.query.count()
    
    # 2. SUM - Sumar valores
    # SQL: SELECT SUM(likes) FROM post
    total_likes = db.session.query(func.sum(Post.likes)).scalar()
    
    # 3. AVG - Promedio
    # SQL: SELECT AVG(edad) FROM usuario
    edad_promedio = db.session.query(func.avg(Usuario.edad)).scalar()
    
    # 4. MAX - Valor máximo
    # SQL: SELECT MAX(likes) FROM post
    max_likes = db.session.query(func.max(Post.likes)).scalar()
    
    # 5. MIN - Valor mínimo
    # SQL: SELECT MIN(edad) FROM usuario WHERE edad IS NOT NULL
    edad_minima = db.session.query(func.min(Usuario.edad)).filter(
        Usuario.edad != None
    ).scalar()
    
    # 6. Múltiples agregaciones
    resultado = db.session.query(
        func.count(Post.id).label('total_posts'),
        func.sum(Post.likes).label('total_likes'),
        func.avg(Post.likes).label('promedio_likes')
    ).first()
    
    return jsonify({
        'total_usuarios': total_usuarios,
        'total_likes': total_likes or 0,
        'edad_promedio': float(edad_promedio) if edad_promedio else 0,
        'max_likes': max_likes or 0,
        'edad_minima': edad_minima,
        'estadisticas_posts': {
            'total': resultado.total_posts if resultado else 0,
            'likes_totales': resultado.total_likes if resultado else 0,
            'promedio': float(resultado.promedio_likes) if resultado and resultado.promedio_likes else 0
        }
    })


# ============================================
# GROUP BY y HAVING
# ============================================

@bp.route('/ejemplos/group-by', methods=['GET'])
def group_by_having():
    """
    Agrupar resultados y filtrar grupos
    """
    from sqlalchemy import func
    
    # 1. GROUP BY - Agrupar y contar
    # SQL: SELECT usuario_id, COUNT(*) as total 
    #      FROM post GROUP BY usuario_id
    posts_por_usuario = db.session.query(
        Post.usuario_id,
        func.count(Post.id).label('total_posts')
    ).group_by(Post.usuario_id).all()
    
    # 2. GROUP BY con JOIN para obtener nombres
    # SQL: SELECT usuario.username, COUNT(post.id) as total
    #      FROM usuario LEFT JOIN post ON usuario.id = post.usuario_id
    #      GROUP BY usuario.id
    estadisticas = db.session.query(
        Usuario.username,
        func.count(Post.id).label('total_posts')
    ).outerjoin(Post).group_by(Usuario.id).all()
    
    # 3. HAVING - Filtrar después de agrupar
    # Solo usuarios con más de 5 posts
    # SQL: SELECT usuario_id, COUNT(*) as total 
    #      FROM post GROUP BY usuario_id 
    #      HAVING COUNT(*) > 5
    usuarios_activos = db.session.query(
        Post.usuario_id,
        func.count(Post.id).label('total_posts')
    ).group_by(Post.usuario_id).having(func.count(Post.id) > 5).all()
    
    # 4. GROUP BY con múltiples agregaciones
    # SQL: SELECT usuario_id, COUNT(*) as total, SUM(likes) as total_likes
    #      FROM post GROUP BY usuario_id
    resumen = db.session.query(
        Post.usuario_id,
        func.count(Post.id).label('total_posts'),
        func.sum(Post.likes).label('total_likes'),
        func.avg(Post.likes).label('promedio_likes')
    ).group_by(Post.usuario_id).all()
    
    return jsonify({
        'posts_por_usuario': [
            {'usuario_id': r[0], 'total': r[1]} 
            for r in posts_por_usuario
        ],
        'estadisticas': [
            {'username': r[0], 'total_posts': r[1]} 
            for r in estadisticas
        ],
        'usuarios_muy_activos': len(usuarios_activos)
    })


# ============================================
# JOINS - Unir Tablas
# ============================================

@bp.route('/ejemplos/joins', methods=['GET'])
def ejemplos_joins():
    """
    Diferentes tipos de joins
    """
    
    # 1. INNER JOIN (solo registros que coinciden en ambas tablas)
    # SQL: SELECT usuario.*, post.* FROM usuario 
    #      INNER JOIN post ON usuario.id = post.usuario_id
    resultado = db.session.query(Usuario, Post).join(Post).all()
    
    # 2. LEFT JOIN / LEFT OUTER JOIN (todos los usuarios, con o sin posts)
    # SQL: SELECT usuario.*, post.* FROM usuario 
    #      LEFT JOIN post ON usuario.id = post.usuario_id
    resultado = db.session.query(Usuario, Post).outerjoin(Post).all()
    
    # 3. JOIN con filtros
    # Usuarios que tienen posts publicados
    # SQL: SELECT DISTINCT usuario.* FROM usuario 
    #      JOIN post ON usuario.id = post.usuario_id 
    #      WHERE post.publicado = 1
    usuarios_con_posts = db.session.query(Usuario).join(Post).filter(
        Post.publicado == True
    ).distinct().all()
    
    # 4. JOIN con agregación
    # Usuarios y su cantidad de posts
    usuarios_stats = db.session.query(
        Usuario.username,
        func.count(Post.id).label('total_posts')
    ).outerjoin(Post).group_by(Usuario.id).all()
    
    # 5. Acceder a través de la relación (más simple)
    # No necesitas JOIN explícito si tienes relationship
    usuario = Usuario.query.first()
    if usuario:
        posts = usuario.posts.all()  # Usa la relación definida
    
    return jsonify({
        'usuarios_con_posts_publicados': len(usuarios_con_posts),
        'estadisticas': [
            {'username': r[0], 'posts': r[1]} 
            for r in usuarios_stats
        ]
    })


# ============================================
# CONSULTAS RAW SQL (Cuando sea necesario)
# ============================================

@bp.route('/ejemplos/raw-sql', methods=['GET'])
def raw_sql():
    """
    Ejecutar SQL directo cuando SQLAlchemy no es suficiente
    """
    from sqlalchemy import text
    
    # 1. Ejecutar SQL directo
    # SQL personalizado con parámetros seguros (:nombre)
    resultado = db.session.execute(
        text("SELECT * FROM usuario WHERE activo = :activo"),
        {"activo": True}
    )
    usuarios = resultado.fetchall()
    
    # 2. SQL que devuelve modelos
    # from_statement(): Convierte SQL en objetos del modelo
    usuarios_obj = Usuario.query.from_statement(
        text("SELECT * FROM usuario WHERE edad > :edad")
    ).params(edad=18).all()
    
    # 3. SQL con múltiples parámetros
    resultado = db.session.execute(
        text("""
            SELECT u.username, COUNT(p.id) as total_posts
            FROM usuario u
            LEFT JOIN post p ON u.id = p.usuario_id
            WHERE u.activo = :activo
            GROUP BY u.id
            HAVING COUNT(p.id) > :min_posts
        """),
        {"activo": True, "min_posts": 2}
    )
    
    return jsonify({
        'total_raw': len(usuarios),
        'total_objetos': len(usuarios_obj)
    })


# ============================================
# BÚSQUEDA AVANZADA - Ejemplo Práctico
# ============================================

@bp.route('/buscar/usuarios', methods=['GET'])
def buscar_usuarios():
    """
    Endpoint de búsqueda flexible con múltiples filtros opcionales
    
    Query params:
    - q: Término de búsqueda general (busca en username, email, nombre)
    - activo: true/false
    - edad_min: Edad mínima
    - edad_max: Edad máxima
    - order: Campo para ordenar (username, email, fecha_creacion)
    - direccion: asc/desc
    - page: Número de página
    - per_page: Registros por página
    
    Ejemplo: /buscar/usuarios?q=juan&activo=true&edad_min=18&order=username&page=1
    """
    
    # Construir query base
    query = Usuario.query
    
    # Filtro de búsqueda general
    termino = request.args.get('q', '').strip()
    if termino:
        # Buscar en múltiples campos con OR
        query = query.filter(or_(
            Usuario.username.like(f'%{termino}%'),
            Usuario.email.like(f'%{termino}%'),
            Usuario.nombre_completo.like(f'%{termino}%')
        ))
    
    # Filtro de activo
    activo = request.args.get('activo')
    if activo is not None:
        activo_bool = activo.lower() == 'true'
        query = query.filter_by(activo=activo_bool)
    
    # Filtro de edad mínima
    edad_min = request.args.get('edad_min', type=int)
    if edad_min:
        query = query.filter(Usuario.edad >= edad_min)
    
    # Filtro de edad máxima
    edad_max = request.args.get('edad_max', type=int)
    if edad_max:
        query = query.filter(Usuario.edad <= edad_max)
    
    # Ordenamiento
    order_field = request.args.get('order', 'fecha_creacion')
    direccion = request.args.get('direccion', 'desc')
    
    # Mapeo de campos válidos para ordenar
    order_map = {
        'username': Usuario.username,
        'email': Usuario.email,
        'fecha_creacion': Usuario.fecha_creacion,
        'edad': Usuario.edad
    }
    
    if order_field in order_map:
        campo = order_map[order_field]
        if direccion == 'asc':
            query = query.order_by(campo.asc())
        else:
            query = query.order_by(campo.desc())
    
    # Paginación
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    paginacion = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return jsonify({
        'usuarios': [u.to_dict() for u in paginacion.items],
        'total': paginacion.total,
        'pagina': paginacion.page,
        'total_paginas': paginacion.pages,
        'tiene_siguiente': paginacion.has_next,
        'tiene_anterior': paginacion.has_prev
    })
```

---

## Relaciones entre Tablas

### Ejemplo Completo con Todos los Tipos de Relaciones

```python
# app/models.py - Agregar al archivo existente

from typing import List

# ============================================
# ONE-TO-MANY (Uno a Muchos)
# Ya existe: Usuario -> Posts
# ============================================

# ============================================
# MANY-TO-MANY (Muchos a Muchos)
# ============================================

# Tabla asociativa para la relación Many-to-Many
# No es un modelo completo, solo una tabla intermedia
# Se define FUERA de las clases
estudiante_clase = db.Table('estudiante_clase',
    # Columna con foreign key a estudiante
    db.Column('estudiante_id', db.Integer, db.ForeignKey('estudiante.id'), primary_key=True),
    # Columna con foreign key a clase
    db.Column('clase_id', db.Integer, db.ForeignKey('clase.id'), primary_key=True),
    # Columnas adicionales opcionales
    db.Column('fecha_inscripcion', db.DateTime, default=datetime.utcnow),
    db.Column('calificacion', db.Float, nullable=True)
)


class Estudiante(db.Model):
    """
    Modelo Estudiante - Un estudiante puede tomar muchas clases
    """
    __tablename__ = 'estudiante'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    
    # Relación Many-to-Many
    # secondary: Especifica la tabla intermedia
    # back_populates: Conecta con el atributo en Clase
    # lazy='dynamic': Permite hacer queries
    clases: Mapped[List["Clase"]] = relationship(
        secondary=estudiante_clase,
        back_populates='estudiantes',
        lazy='dynamic'
    )
    
    def __repr__(self) -> str:
        return f'<Estudiante: {self.nombre}>'


class Clase(db.Model):
    """
    Modelo Clase - Una clase puede tener muchos estudiantes
    """
    __tablename__ = 'clase'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relación inversa Many-to-Many
    estudiantes: Mapped[List["Estudiante"]] = relationship(
        secondary=estudiante_clase,
        back_populates='clases',
        lazy='dynamic'
    )
    
    def __repr__(self) -> str:
        return f'<Clase: {self.nombre}>'


# ============================================
# ONE-TO-ONE (Uno a Uno)
# ============================================

class Perfil(db.Model):
    """
    Modelo Perfil - Un usuario tiene UN perfil
    """
    __tablename__ = 'perfil'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    biografia: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    fecha_nacimiento: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Foreign Key - UNIQUE garantiza One-to-One
    # Un perfil pertenece a UN SOLO usuario
    usuario_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('usuario.id'), 
        unique=True,  # CRÍTICO para One-to-One
        nullable=False
    )
    
    # Relación inversa
    # back_populates: Conecta con 'perfil' en Usuario
    # uselist=False: NO es una lista (es un solo objeto)
    usuario: Mapped["Usuario"] = relationship(back_populates='perfil')
    
    def __repr__(self) -> str:
        return f'<Perfil del usuario {self.usuario_id}>'


# Agregar a la clase Usuario existente:
# perfil: Mapped[Optional["Perfil"]] = relationship(
#     back_populates='usuario',
#     uselist=False,  # One-to-One
#     cascade='all, delete-orphan'
# )


# ============================================
# RUTAS PARA RELACIONES
# ============================================

@bp.route('/estudiantes/<int:estudiante_id>/inscribir', methods=['POST'])
def inscribir_estudiante(estudiante_id):
    """
    Inscribir un estudiante en una clase (Many-to-Many)
    
    Request Body:
    {
        "clase_id": 1
    }
    """
    estudiante = Estudiante.query.get_or_404(estudiante_id)
    data = request.get_json()
    clase_id = data.get('clase_id')
    
    if not clase_id:
        return jsonify({'error': 'clase_id es requerido'}), 400
    
    clase = Clase.query.get_or_404(clase_id)
    
    try:
        # Agregar clase a la lista de clases del estudiante
        estudiante.clases.append(clase)
        db.session.commit()
        
        return jsonify({
            'mensaje': f'{estudiante.nombre} inscrito en {clase.nombre}',
            'total_clases': estudiante.clases.count()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@bp.route('/usuarios/<int:usuario_id>/perfil', methods=['POST'])
def crear_perfil(usuario_id):
    """
    Crear perfil para un usuario (One-to-One)
    
    Request Body:
    {
        "biografia": "Desarrollador Python",
        "avatar": "avatar.jpg"
    }
    """
    usuario = Usuario.query.get_or_404(usuario_id)
    
    # Verificar que no tenga perfil ya
    if hasattr(usuario, 'perfil') and usuario.perfil:
        return jsonify({'error': 'Usuario ya tiene perfil'}), 400
    
    data = request.get_json()
    
    nuevo_perfil = Perfil(
        biografia=data.get('biografia'),
        avatar=data.get('avatar'),
        usuario_id=usuario_id
    )
    
    try:
        db.session.add(nuevo_perfil)
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Perfil creado exitosamente',
            'perfil': {
                'biografia': nuevo_perfil.biografia,
                'avatar': nuevo_perfil.avatar
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
```

---

## Live Templates para PyCharm

### Cómo Instalar Templates en PyCharm

1. **File → Settings** (Windows/Linux) o **PyCharm → Preferences** (Mac)
2. **Editor → Live Templates**
3. Click en **+** → **Template Group** → Crear grupo "SQLAlchemy Modern"
4. Click en **+** → **Live Template** → Pegar cada template

---

### Templates Principales

#### Template: `sqlinit`
**Descripción**: Inicializar Flask + SQLAlchemy (app/__init__.py)

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from app.config import Config

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from app import models
    from app.routes import bp
    app.register_blueprint(bp)
    
    with app.app_context():
        db.create_all()
    
    return app
```

---

#### Template: `sqlmodel`
**Descripción**: Crear modelo completo con sintaxis moderna

**Abbreviation**: `sqlmodel`

```python
class $MODEL_NAME$(db.Model):
    """
    $DESCRIPTION$
    """
    __tablename__ = '$TABLE_NAME
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    $CURSOR$
    
    def __repr__(self) -> str:
        return f'<$MODEL_NAME$: {self.id}>'
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }
```

**Variables**:
- `MODEL_NAME`: Nombre de la clase
- `DESCRIPTION`: Descripción del modelo
- `TABLE_NAME`: Nombre de la tabla

---

#### Template: `sqlcol`
**Descripción**: Agregar columna con sintaxis moderna

**Abbreviation**: `sqlcol`

```python
$NAME$: Mapped[$TYPE$] = mapped_column($DB_TYPE$($SIZE$), $OPTIONS$)
```

**Variables**:
- `NAME`: Nombre de la columna
- `TYPE`: Tipo Python (str, int, bool, float, Optional[str])
- `DB_TYPE`: Tipo DB (String, Integer, Boolean, Float, Text)
- `SIZE`: Tamaño (para String)
- `OPTIONS`: nullable=False, unique=True, default=valor

**Ejemplos de uso**:
```python
# Presionar sqlcol + Tab
username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
edad: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
precio: Mapped[float] = mapped_column(Float, nullable=False)
```

---

#### Template: `sqlfk`
**Descripción**: Foreign Key

**Abbreviation**: `sqlfk`

```python
$NAME$_id: Mapped[int] = mapped_column(Integer, ForeignKey('$TABLE$.$FK_COLUMN), nullable=False)
```

---

#### Template: `sqlrel1m`
**Descripción**: Relación One-to-Many

**Abbreviation**: `sqlrel1m`

```python
$NAME$: Mapped[List["$MODEL$"]] = relationship(
    back_populates='$BACK_POP,
    lazy='dynamic',
    cascade='all, delete-orphan'
)
```

---

#### Template: `sqlrelm1`
**Descripción**: Relación Many-to-One

**Abbreviation**: `sqlrelm1`

```python
$NAME$: Mapped["$MODEL$"] = relationship(back_populates='$BACK_POP)
```

---

#### Template: `sqlrelmm`
**Descripción**: Relación Many-to-Many (tabla asociativa)

**Abbreviation**: `sqlrelmm`

```python
$TABLE_NAME$ = db.Table('$TABLE_NAME,
    db.Column('$TABLE1$_id', db.Integer, db.ForeignKey('$TABLE1$.id'), primary_key=True),
    db.Column('$TABLE2$_id', db.Integer, db.ForeignKey('$TABLE2$.id'), primary_key=True)
)
```

---

### Templates para Rutas CRUD

#### Template: `flaskget`
**Descripción**: Ruta GET para listar todos

**Abbreviation**: `flaskget`

```python
@bp.route('/$ROUTE, methods=['GET'])
def obtener_$PLURAL$():
    """
    Obtiene todos los registros de $MODEL$
    """
    $VARIABLE$ = $MODEL$.query.all()
    return jsonify([$ITEM$.to_dict() for $ITEM$ in $VARIABLE$]), 200
```

---

#### Template: `flaskgetid`
**Descripción**: Ruta GET para obtener por ID

**Abbreviation**: `flaskgetid`

```python
@bp.route('/$ROUTE$/<int:id>', methods=['GET'])
def obtener_$SINGULAR$(id):
    """
    Obtiene un registro específico de $MODEL$
    """
    $VARIABLE$ = $MODEL$.query.get_or_404(id)
    return jsonify($VARIABLE$.to_dict()), 200
```

---

#### Template: `flaskpost`
**Descripción**: Ruta POST para crear

**Abbreviation**: `flaskpost`

```python
@bp.route('/$ROUTE, methods=['POST'])
def crear_$SINGULAR$():
    """
    Crea un nuevo registro de $MODEL$
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos no proporcionados'}), 400
    
    nuevo_$VARIABLE$ = $MODEL$(
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
**Descripción**: Ruta PUT para actualizar

**Abbreviation**: `flaskput`

```python
@bp.route('/$ROUTE$/<int:id>', methods=['PUT'])
def actualizar_$SINGULAR$(id):
    """
    Actualiza un registro de $MODEL$
    """
    $VARIABLE$ = $MODEL$.query.get_or_404(id)
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
**Descripción**: Ruta DELETE para eliminar

**Abbreviation**: `flaskdel`

```python
@bp.route('/$ROUTE$/<int:id>', methods=['DELETE'])
def eliminar_$SINGULAR$(id):
    """
    Elimina un registro de $MODEL$
    """
    $VARIABLE$ = $MODEL$.query.get_or_404(id)
    
    try:
        db.session.delete($VARIABLE$)
        db.session.commit()
        return jsonify({'mensaje': 'Eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
```

---

### Templates para Consultas

#### Template: `sqlfilter`
**Descripción**: Query con filtro

**Abbreviation**: `sqlfilter`

```python
$VARIABLE$ = $MODEL$.query.filter($MODEL$.$FIELD$ == $VALUE$).all()
```

---

#### Template: `sqlfilterby`
**Descripción**: Query con filter_by

**Abbreviation**: `sqlfilterby`

```python
$VARIABLE$ = $MODEL$.query.filter_by($FIELD$=$VALUE$).all()
```

---

#### Template: `sqlorder`
**Descripción**: Query con ordenamiento

**Abbreviation**: `sqlorder`

```python
$VARIABLE$ = $MODEL$.query.order_by($MODEL$.$FIELD$.desc()).all()
```

---

#### Template: `sqlpag`
**Descripción**: Query con paginación

**Abbreviation**: `sqlpag`

```python
page = request.args.get('page', 1, type=int)
per_page = request.args.get('per_page', 10, type=int)

paginacion = $MODEL$.query.paginate(
    page=page,
    per_page=per_page,
    error_out=False
)

$VARIABLE$ = paginacion.items
```

---

#### Template: `sqljoin`
**Descripción**: Query con JOIN

**Abbreviation**: `sqljoin`

```python
$VARIABLE$ = db.session.query($MODEL1$, $MODEL2$).join($MODEL2$).filter($CONDITION$).all()
```

---

#### Template: `sqlcount`
**Descripción**: Contar registros con agregación

**Abbreviation**: `sqlcount`

```python
from sqlalchemy import func

total = db.session.query(func.count($MODEL$.id)).scalar()
```

---

#### Template: `sqlgroupby`
**Descripción**: Query con GROUP BY

**Abbreviation**: `sqlgroupby`

```python
from sqlalchemy import func

resultado = db.session.query(
    $MODEL$.$FIELD$,
    func.count($MODEL$.id).label('total')
).group_by($MODEL$.$FIELD$).all()
```

---

## Ejemplos Prácticos Completos

### Ejemplo 1: Sistema de Blog

```python
# app/models.py

class Categoria(db.Model):
    """Categorías para los posts"""
    __tablename__ = 'categoria'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Relación con Posts
    posts: Mapped[List["PostBlog"]] = relationship(
        back_populates='categoria',
        lazy='dynamic'
    )
    
    def __repr__(self) -> str:
        return f'<Categoria: {self.nombre}>'


class PostBlog(db.Model):
    """Post de blog con categoría"""
    __tablename__ = 'post_blog'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    publicado: Mapped[bool] = mapped_column(Boolean, default=False)
    visitas: Mapped[int] = mapped_column(Integer, default=0)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_publicacion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Foreign Keys
    autor_id: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.id'), nullable=False)
    categoria_id: Mapped[int] = mapped_column(Integer, ForeignKey('categoria.id'), nullable=False)
    
    # Relaciones
    autor: Mapped["Usuario"] = relationship()
    categoria: Mapped["Categoria"] = relationship(back_populates='posts')
    
    def __repr__(self) -> str:
        return f'<PostBlog: {self.titulo}>'


# Rutas para el blog
@bp.route('/blog/posts', methods=['GET'])
def listar_posts_blog():
    """
    Lista posts con filtros avanzados
    
    Query params:
    - categoria: ID de categoría
    - publicado: true/false
    - buscar: Término de búsqueda
    - ordenar: titulo, fecha, visitas
    """
    query = PostBlog.query
    
    # Filtrar por categoría
    categoria_id = request.args.get('categoria', type=int)
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    
    # Filtrar por publicado
    publicado = request.args.get('publicado')
    if publicado is not None:
        query = query.filter_by(publicado=publicado.lower() == 'true')
    
    # Búsqueda
    buscar = request.args.get('buscar', '').strip()
    if buscar:
        query = query.filter(or_(
            PostBlog.titulo.like(f'%{buscar}%'),
            PostBlog.contenido.like(f'%{buscar}%')
        ))
    
    # Ordenar
    ordenar = request.args.get('ordenar', 'fecha')
    if ordenar == 'visitas':
        query = query.order_by(PostBlog.visitas.desc())
    elif ordenar == 'titulo':
        query = query.order_by(PostBlog.titulo.asc())
    else:
        query = query.order_by(PostBlog.fecha_creacion.desc())
    
    # Paginar
    page = request.args.get('page', 1, type=int)
    paginacion = query.paginate(page=page, per_page=10, error_out=False)
    
    return jsonify({
        'posts': [{
            'id': p.id,
            'titulo': p.titulo,
            'slug': p.slug,
            'autor': p.autor.username,
            'categoria': p.categoria.nombre,
            'visitas': p.visitas,
            'publicado': p.publicado,
            'fecha': p.fecha_creacion.isoformat()
        } for p in paginacion.items],
        'total': paginacion.total,
        'pagina': paginacion.page,
        'total_paginas': paginacion.pages
    })


@bp.route('/blog/estadisticas', methods=['GET'])
def estadisticas_blog():
    """Estadísticas del blog"""
    from sqlalchemy import func
    
    # Total de posts por categoría
    posts_por_categoria = db.session.query(
        Categoria.nombre,
        func.count(PostBlog.id).label('total')
    ).outerjoin(PostBlog).group_by(Categoria.id).all()
    
    # Posts más visitados
    top_posts = PostBlog.query.order_by(
        PostBlog.visitas.desc()
    ).limit(5).all()
    
    # Total de visitas
    total_visitas = db.session.query(
        func.sum(PostBlog.visitas)
    ).scalar() or 0
    
    return jsonify({
        'posts_por_categoria': [
            {'categoria': r[0], 'total': r[1]} 
            for r in posts_por_categoria
        ],
        'top_posts': [{
            'titulo': p.titulo,
            'visitas': p.visitas
        } for p in top_posts],
        'total_visitas': total_visitas
    })
```

---

### Ejemplo 2: Sistema de Tienda

```python
# app/models.py

class Producto(db.Model):
    """Producto en tienda"""
    __tablename__ = 'producto'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f'<Producto: {self.nombre}>'
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'activo': self.activo,
            'disponible': self.stock > 0
        }


# Rutas para productos
@bp.route('/productos', methods=['GET'])
def listar_productos():
    """
    Listar productos con filtros
    
    Query params:
    - disponible: true/false
    - precio_min: Precio mínimo
    - precio_max: Precio máximo
    - buscar: Término de búsqueda
    """
    query = Producto.query.filter_by(activo=True)
    
    # Filtrar disponibles
    disponible = request.args.get('disponible')
    if disponible and disponible.lower() == 'true':
        query = query.filter(Producto.stock > 0)
    
    # Rango de precios
    precio_min = request.args.get('precio_min', type=float)
    precio_max = request.args.get('precio_max', type=float)
    
    if precio_min:
        query = query.filter(Producto.precio >= precio_min)
    if precio_max:
        query = query.filter(Producto.precio <= precio_max)
    
    # Búsqueda
    buscar = request.args.get('buscar', '').strip()
    if buscar:
        query = query.filter(Producto.nombre.like(f'%{buscar}%'))
    
    # Ordenar por precio
    orden = request.args.get('orden', 'asc')
    if orden == 'desc':
        query = query.order_by(Producto.precio.desc())
    else:
        query = query.order_by(Producto.precio.asc())
    
    productos = query.all()
    
    return jsonify([p.to_dict() for p in productos])


@bp.route('/productos/<int:id>/actualizar-stock', methods=['PATCH'])
def actualizar_stock(id):
    """
    Actualizar stock de un producto
    
    Request Body:
    {
        "cantidad": 10,  # Puede ser positivo (agregar) o negativo (restar)
    }
    """
    producto = Producto.query.get_or_404(id)
    data = request.get_json()
    
    cantidad = data.get('cantidad', 0)
    
    try:
        nuevo_stock = producto.stock + cantidad
        
        if nuevo_stock < 0:
            return jsonify({'error': 'Stock no puede ser negativo'}), 400
        
        producto.stock = nuevo_stock
        db.session.commit()
        
        return jsonify({
            'mensaje': 'Stock actualizado',
            'producto': producto.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
```

---

## 🎯 Mejores Prácticas

### 1. Siempre Usa Try-Except para Operaciones de BD

```python
try:
    db.session.add(objeto)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    # Loggear el error
    print(f"Error: {e}")
    raise
```

---

### 2. Validar Datos Antes de Guardar

```python
def crear_usuario():
    data = request.get_json()
    
    # Validar campos requeridos
    if not data.get('username') or not data.get('email'):
        return jsonify({'error': 'Campos requeridos faltantes'}), 400
    
    # Validar formato email
    import re
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+, data['email']):
        return jsonify({'error': 'Email inválido'}), 400
    
    # Verificar duplicados
    if Usuario.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username ya existe'}), 409
    
    # Crear usuario...
```

---

### 3. Usar Índices para Búsquedas Frecuentes

```python
# Agregar index=True a columnas que se buscan frecuentemente
email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
```

---

### 4. Cerrar Sesión Correctamente

```python
# Flask-SQLAlchemy maneja esto automáticamente,
# pero si usas sesiones manuales:

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
```

---

### 5. Usar Métodos de Clase para Operaciones Comunes

```python
class Usuario(db.Model):
    # ... columnas ...
    
    @classmethod
    def buscar_por_email(cls, email: str):
        """Buscar usuario por email