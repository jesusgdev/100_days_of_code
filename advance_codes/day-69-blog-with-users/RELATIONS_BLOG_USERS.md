# 📚 Guía Completa: Relaciones en SQLAlchemy para Blog con Usuarios

## 📖 Tabla de Contenidos
1. [Conceptos Fundamentales](#conceptos-fundamentales)
2. [Anatomía de una Tabla](#anatomía-de-una-tabla)
3. [Primary Keys (Llaves Primarias)](#primary-keys)
4. [Foreign Keys (Llaves Foráneas)](#foreign-keys)
5. [Relationships (Relaciones)](#relationships)
6. [Tipos de Relaciones](#tipos-de-relaciones)
7. [Parámetros Importantes](#parámetros-importantes)
8. [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🎯 Conceptos Fundamentales

### ¿Qué es una Base de Datos Relacional?

Una base de datos relacional es como un conjunto de **tablas de Excel** que están **conectadas entre sí**. Cada tabla almacena información específica y las relaciones permiten vincular datos entre diferentes tablas.

**Ejemplo del mundo real:**
- **Tabla Users**: Lista de personas registradas
- **Tabla BlogPosts**: Lista de artículos escritos
- **Relación**: Cada artículo fue escrito por UNA persona (usuario)

### Terminología Básica

| Término | Significado | Ejemplo |
|---------|-------------|---------|
| **Table (Tabla)** | Estructura que almacena datos | `users`, `blog_posts` |
| **Row (Fila)** | Un registro individual en la tabla | Un usuario específico |
| **Column (Columna)** | Un campo de datos | `email`, `name`, `password` |
| **Primary Key** | ID único que identifica cada fila | `id = 1`, `id = 2` |
| **Foreign Key** | Columna que referencia el ID de otra tabla | `author_id = 5` (referencia a `users.id = 5`) |
| **Relationship** | Conexión virtual entre tablas | `user.posts`, `post.author` |

---

## 🏗️ Anatomía de una Tabla

### Estructura Completa de una Clase Model

```python
class User(db.Model, UserMixin):
    """Docstring explicando la tabla"""
    __tablename__ = "users"  # Nombre de la tabla en la DB
    
    # Columnas reales en la base de datos
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Relaciones virtuales (NO son columnas reales)
    posts: Mapped[list["BlogPost"]] = relationship(back_populates="author")
```

### Componentes Explicados:

#### 1. **Herencia de Clases**
```python
class User(db.Model, UserMixin):
```

**`db.Model`**:
- Clase base de SQLAlchemy
- Convierte tu clase Python en una tabla de base de datos
- Proporciona métodos como `.query.all()`, `.query.get()`

**`UserMixin`** (solo para User):
- Clase de Flask-Login
- Añade métodos automáticos:
  - `is_authenticated`: ¿Está el usuario logueado?
  - `is_active`: ¿Está la cuenta activa?
  - `get_id()`: Obtiene el ID del usuario como string

#### 2. **Nombre de la Tabla**
```python
__tablename__ = "users"
```

- Define el nombre EXACTO de la tabla en la base de datos
- Debe ser único
- Por convención se usa minúsculas y plural
- Este nombre se usa en `ForeignKey("users.id")`

#### 3. **Type Hints (Anotaciones de Tipo)**
```python
id: Mapped[int]
email: Mapped[str]
posts: Mapped[list["BlogPost"]]
```

**`Mapped[tipo]`**:
- Nueva sintaxis de SQLAlchemy 2.0
- Indica qué tipo de dato contendrá la columna
- `Mapped[int]`: Números enteros
- `Mapped[str]`: Texto/cadenas
- `Mapped[list["BlogPost"]]`: Lista de objetos BlogPost

**¿Por qué "BlogPost" entre comillas?**
- Se llama "forward reference" (referencia hacia adelante)
- Permite referenciar una clase que aún no ha sido definida
- Sin comillas, Python daría error si BlogPost se define después

---

## 🔑 Primary Keys (Llaves Primarias)

### ¿Qué es una Primary Key?

Es un **identificador único** para cada registro en la tabla. Como el número de cédula de una persona: nadie más puede tener el mismo.

### Sintaxis Completa:

```python
id: Mapped[int] = mapped_column(Integer, primary_key=True)
```

### Desglose de Cada Parte:

| Parte | ¿Qué hace? |
|-------|------------|
| `id` | Nombre de la columna |
| `Mapped[int]` | Type hint: será un número entero |
| `mapped_column()` | Función que define propiedades de la columna |
| `Integer` | Tipo SQL: número entero |
| `primary_key=True` | Marca esta columna como PRIMARY KEY |

### Características Automáticas:

Cuando defines `primary_key=True`, SQLAlchemy automáticamente:
- ✅ Hace la columna **única** (no pueden haber duplicados)
- ✅ Hace la columna **no nula** (siempre tiene valor)
- ✅ Hace la columna **auto-incremental** (1, 2, 3, 4...)

### Ejemplo Visual:

```
Tabla: users
+----+------------------+----------+
| id | email            | name     |  ← "id" es la PRIMARY KEY
+----+------------------+----------+
| 1  | alice@email.com  | Alice    |
| 2  | bob@email.com    | Bob      |  ← Cada ID es único
| 3  | carol@email.com  | Carol    |
+----+------------------+----------+
```

---

## 🔗 Foreign Keys (Llaves Foráneas)

### ¿Qué es una Foreign Key?

Es una columna que **almacena el ID de otra tabla**, creando una conexión entre ellas. Es como guardar el número de teléfono de alguien para poder llamarle.

### Sintaxis Completa:

```python
author_id: Mapped[int] = mapped_column(
    Integer,
    ForeignKey("users.id"),
    nullable=False
)
```

### Desglose de Cada Parte:

| Parte | ¿Qué hace? |
|-------|------------|
| `author_id` | Nombre de la columna (debe terminar en `_id` por convención) |
| `Mapped[int]` | Type hint: número entero |
| `Integer` | Tipo SQL de la columna |
| `ForeignKey("users.id")` | Conecta esta columna con `id` de la tabla `users` |
| `nullable=False` | Esta columna es obligatoria (no puede estar vacía) |

### Formato de ForeignKey:

```python
ForeignKey("table_name.column_name")
         #  ↓           ↓
         #  Tabla       Columna
```

**Importante:**
- El nombre de la tabla debe coincidir EXACTAMENTE con `__tablename__`
- La columna referenciada casi siempre es `id` (la PRIMARY KEY)

### Ejemplo Visual:

```
Tabla: users                    Tabla: blog_posts
+----+---------+               +----+-------+-----------+
| id | name    |               | id | title | author_id |  ← FOREIGN KEY
+----+---------+               +----+-------+-----------+
| 1  | Alice   | ←─────────────| 1  | Post1 | 1         |
| 2  | Bob     | ←─────────────| 2  | Post2 | 1         |
+----+---------+    ↑          | 3  | Post3 | 2         |
                    │          +----+-------+-----------+
                    └──────── author_id referencia users.id
```

**Explicación:**
- `author_id` en `blog_posts` almacena el ID del usuario
- Post1 y Post2 tienen `author_id = 1` (fueron escritos por Alice)
- Post3 tiene `author_id = 2` (fue escrito por Bob)

### ¿Qué Previene una Foreign Key?

```python
# ❌ Esto daría ERROR:
new_post = BlogPost(author_id=999)  # El usuario 999 no existe

# ✅ Esto funciona:
new_post = BlogPost(author_id=1)    # El usuario 1 existe
```

---

## 🔄 Relationships (Relaciones)

### ¿Qué es un Relationship?

Es una **propiedad virtual** que te permite acceder a objetos relacionados SIN escribir consultas SQL manualmente. Es la "magia" de SQLAlchemy.

**Importante:** `relationship()` **NO crea una columna en la base de datos**. Solo crea una propiedad Python para facilitar el acceso a datos.

### Sintaxis Completa:

```python
posts: Mapped[list["BlogPost"]] = relationship(
    back_populates="author",
    cascade="all, delete-orphan"
)
```

### Desglose de Cada Parte:

| Parte | ¿Qué hace? |
|-------|------------|
| `posts` | Nombre de la propiedad (usa plural para listas) |
| `Mapped[list["BlogPost"]]` | Type hint: lista de objetos BlogPost |
| `relationship()` | Función que crea la conexión virtual |
| `back_populates="author"` | Conecta con la propiedad `author` en BlogPost |
| `cascade="all, delete-orphan"` | Reglas para eliminación en cascada |

### back_populates: La Conexión Bidireccional

`back_populates` crea una relación de **dos vías**:

```python
# En User:
posts: Mapped[list["BlogPost"]] = relationship(back_populates="author")
                                                              # ↓
# En BlogPost:                                               # ↓
author: Mapped["User"] = relationship(back_populates="posts")
                                                    # ↑
```

**Regla:** El valor de `back_populates` debe ser el **nombre exacto** de la propiedad en la otra clase.

### Ejemplo Visual de Uso:

```python
# Obtener un usuario
user = User.query.get(1)

# Acceder a sus posts (NO necesitas escribir SQL)
user_posts = user.posts  # ← SQLAlchemy hace la query automáticamente
# Resultado: [<BlogPost: Post1>, <BlogPost: Post2>]

# Acceder al autor de un post
post = BlogPost.query.get(1)
post_author = post.author  # ← Obtiene el objeto User completo
print(post_author.name)    # "Alice"
```

### Diferencia: Columna vs Relationship

```python
class BlogPost(db.Model):
    # COLUMNA real en la base de datos
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    # ↑ Almacena solo un NÚMERO (el ID del usuario)
    
    # RELATIONSHIP virtual (NO es columna)
    author: Mapped["User"] = relationship(back_populates="posts")
    # ↑ Retorna el OBJETO User completo
```

**Uso:**
```python
post = BlogPost.query.get(1)
print(post.author_id)  # 5 (solo el número)
print(post.author)     # <User: Alice> (objeto completo)
print(post.author.email)  # "alice@email.com"
```

---

## 📊 Tipos de Relaciones

### 1. One-to-Many (Uno a Muchos)

**Concepto:** UN registro en tabla A se relaciona con MUCHOS registros en tabla B.

**Ejemplo:** Un usuario escribe muchos posts.

```
User (ONE)  →  BlogPost (MANY)
   1        →     1, 2, 3
```

**Implementación:**

```python
# Tabla PADRE (ONE)
class User(db.Model):
    posts: Mapped[list["BlogPost"]] = relationship(back_populates="author")
    #              ↑ lista = "muchos"

# Tabla HIJA (MANY)
class BlogPost(db.Model):
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    #              ↑ objeto único = "uno"
```

**Uso:**
```python
user = User.query.get(1)
print(user.posts)  # [post1, post2, post3] ← lista

post = BlogPost.query.get(1)
print(post.author)  # user ← objeto único
```

### 2. Many-to-One (Muchos a Uno)

**Es lo mismo que One-to-Many**, pero visto desde el otro lado.

**Ejemplo:** Muchos posts pertenecen a un usuario.

```
BlogPost (MANY)  →  User (ONE)
  1, 2, 3        →     1
```

### 3. Many-to-Many (Muchos a Muchos)

**No lo usamos en este proyecto**, pero para referencia:

**Concepto:** MUCHOS registros en tabla A se relacionan con MUCHOS registros en tabla B.

**Ejemplo:** Estudiantes y Cursos
- Un estudiante toma muchos cursos
- Un curso tiene muchos estudiantes

Requiere una **tabla intermedia** (association table).

---

## ⚙️ Parámetros Importantes

### 1. nullable

**¿Qué hace?** Define si una columna puede estar vacía (NULL) o no.

```python
email: Mapped[str] = mapped_column(String(100), nullable=False)
#                                                nullable=False → obligatorio
```

| Valor | Significado |
|-------|-------------|
| `nullable=False` | Campo OBLIGATORIO (no puede estar vacío) |
| `nullable=True` | Campo OPCIONAL (puede estar vacío) |

**Ejemplo:**
```python
# ✅ Válido si nullable=True
user = User(name="Alice")  # email queda vacío

# ❌ Error si nullable=False
user = User(name="Alice")  # Falta email - ERROR!
```

### 2. unique

**¿Qué hace?** Previene valores duplicados en una columna.

```python
email: Mapped[str] = mapped_column(String(100), unique=True)
#                                                unique=True → sin duplicados
```

**Ejemplo:**
```python
# ✅ Primer usuario con este email
user1 = User(email="alice@email.com")

# ❌ Error - email duplicado
user2 = User(email="alice@email.com")  # ERROR!
```

### 3. cascade

**¿Qué hace?** Define qué ocurre con los registros relacionados cuando eliminas un padre.

```python
posts: Mapped[list["BlogPost"]] = relationship(
    back_populates="author",
    cascade="all, delete-orphan"
)
```

#### Opciones de Cascade:

| Opción | ¿Qué hace? |
|--------|------------|
| `"all"` | Propaga TODAS las operaciones (save, delete, etc.) |
| `"delete"` | Al borrar padre, borra hijos |
| `"delete-orphan"` | Borra hijos si pierden su padre |
| `"save-update"` | Al guardar padre, guarda hijos automáticamente |

**Ejemplo Práctico:**

```python
# Sin cascade
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
# Los posts del usuario quedan huérfanos (author_id apunta a un user inexistente)

# Con cascade="all, delete-orphan"
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
# ✅ Todos los posts del usuario se eliminan automáticamente
```

### 4. String vs Text

**¿Cuál usar para texto?**

| Tipo | Uso | Límite |
|------|-----|--------|
| `String(n)` | Texto corto (título, nombre, email) | Máximo n caracteres |
| `Text` | Texto largo (contenido de posts, comentarios) | Sin límite |

```python
# Para títulos, nombres
title: Mapped[str] = mapped_column(String(250))

# Para contenido largo
body: Mapped[str] = mapped_column(Text)
```

---

## 💡 Ejemplos de Uso Completos

### Ejemplo 1: Crear un Usuario

```python
from werkzeug.security import generate_password_hash

# Crear nuevo usuario
new_user = User(
    email="alice@email.com",
    password=generate_password_hash("secret123", method='pbkdf2:sha256', salt_length=8),
    name="Alice"
)

# Guardar en base de datos
db.session.add(new_user)
db.session.commit()

print(f"Usuario creado con ID: {new_user.id}")
```

### Ejemplo 2: Crear un Post

```python
from flask_login import current_user
from datetime import date

# Opción A: Pasar el objeto User completo
new_post = BlogPost(
    title="Mi Primer Post",
    subtitle="Un post increíble",
    body="Contenido del post aquí...",
    img_url="https://example.com/image.jpg",
    date=date.today().strftime("%B %d, %Y"),
    author=current_user  # ← Objeto User
)

# Opción B: Pasar solo el ID
new_post = BlogPost(
    title="Mi Primer Post",
    subtitle="Un post increíble",
    body="Contenido del post aquí...",
    img_url="https://example.com/image.jpg",
    date=date.today().strftime("%B %d, %Y"),
    author_id=current_user.id  # ← Solo el ID
)

db.session.add(new_post)
db.session.commit()
```

### Ejemplo 3: Crear un Comentario

```python
# Obtener el post
post = BlogPost.query.get(1)

# Crear comentario
new_comment = Comment(
    text="¡Excelente artículo!",
    comment_author=current_user,  # Usuario que comenta
    parent_post=post  # Post que se comenta
)

db.session.add(new_comment)
db.session.commit()
```

### Ejemplo 4: Acceder a Relaciones

```python
# Obtener usuario
user = User.query.filter_by(email="alice@email.com").first()

# Acceder a posts del usuario
print(f"Posts de {user.name}:")
for post in user.posts:
    print(f"- {post.title}")

# Acceder a comentarios del usuario
print(f"
Comentarios de {user.name}:")
for comment in user.comments:
    print(f"- {comment.text} en '{comment.parent_post.title}'")
```

### Ejemplo 5: Obtener Autor de un Post

```python
# Obtener post
post = BlogPost.query.get(1)

# Acceder al autor (no necesitas hacer otra query)
print(f"Título: {post.title}")
print(f"Autor: {post.author.name}")
print(f"Email del autor: {post.author.email}")

# Acceder a comentarios del post
print(f"
Comentarios ({len(post.comments)}):")
for comment in post.comments:
    print(f"- {comment.comment_author.name}: {comment.text}")
```

### Ejemplo 6: Eliminar con Cascade

```python
# Obtener usuario
user = User.query.get(1)

# Ver cuántos posts tiene
print(f"Posts antes de eliminar: {len(user.posts)}")

# Eliminar usuario
db.session.delete(user)
db.session.commit()

# Gracias a cascade="all, delete-orphan"
# Todos sus posts Y comentarios se eliminan automáticamente
```

### Ejemplo 7: Validar Relaciones

```python
# Intentar crear post con usuario inexistente
try:
    bad_post = BlogPost(
        title="Post",
        author_id=9999  # Este usuario no existe
    )
    db.session.add(bad_post)
    db.session.commit()
except IntegrityError:
    print("Error: El usuario no existe")
    db.session.rollback()
```

---

## 🎯 Diagrama de Relaciones Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                      MODELO DE DATOS                            │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │    User      │
    │              │
    │ id (PK)      │◄────────┐
    │ email        │         │
    │ password     │         │ ONE User
    │ name         │         │ HAS MANY Posts
    └──────────────┘         │
          │                  │
          │ user.posts       │
          │ (relationship)   │
          │                  │
          ▼                  │
    ┌──────────────┐         │
    │  BlogPost    │         │
    │              │         │
    │ id (PK)      │         │
    │ author_id(FK)├─────────┘
    │ title        │
    │ subtitle     │
    │ date         │
    │ body         │
    │ img_url      │
    └──────────────┘
          │
          │ post.comments
          │ (relationship)
          ▼
    ┌──────────────┐
    │   Comment    │
    │              │
    │ id (PK)      │
    │ author_id(FK)├────┐
    │ post_id (FK) ├────┤
    │ text         │    │
    └──────────────┘    │
                        │
         ┌──────────────┴──────────────┐
         │                             │
         │ ONE User                    │ ONE Post
         │ HAS MANY Comments           │ HAS MANY Comments
         │                             │
         └─────────────────────────────┘

LEYENDA:
PK = Primary Key (Llave Primaria)
FK = Foreign Key (Llave Foránea)
│  = Relación One-to-Many
```

---

## 🚨 Errores Comunes y Soluciones

### Error 1: `'str' object has no attribute '_sa_instance_state'`

**Causa:** Estás pasando un string en lugar de un objeto.

```python
# ❌ INCORRECTO
new_post = BlogPost(author=current_user.name)  # String

# ✅ CORRECTO
new_post = BlogPost(author=current_user)  # Objeto User
```

### Error 2: `UndefinedError: relationship is undefined`

**Causa:** El nombre en `back_populates` no coincide con el nombre de la propiedad.

```python
# En User:
posts = relationship(back_populates="writer")  # ❌ "writer"

# En BlogPost:
author = relationship(back_populates="posts")  # ❌ Busca "writer"

# ✅ CORRECTO - nombres deben coincidir:
# En User:
posts = relationship(back_populates="author")
# En BlogPost:
author = relationship(back_populates="posts")
```

### Error 3: Nombre de tabla incorrecto en ForeignKey

```python
# ❌ INCORRECTO
ForeignKey("blog_post.id")  # Singular

# ✅ CORRECTO - debe coincidir con __tablename__
ForeignKey("blog_posts.id")  # Plural
```

### Error 4: Columna duplicada

```python
# ❌ INCORRECTO - dos columnas con el mismo nombre
class Comment(db.Model):
    author_id = mapped_column(ForeignKey("users.id"))
    author_id = mapped_column(ForeignKey("posts.id"))  # ❌ Duplicado

# ✅ CORRECTO - nombres únicos
class Comment(db.Model):
    author_id = mapped_column(ForeignKey("users.id"))
    post_id = mapped_column(ForeignKey("posts.id"))
```

---

## ✅ Checklist de Verificación

Antes de ejecutar tu código, verifica:

- [ ] Cada tabla tiene `__tablename__` único
- [ ] Cada tabla tiene una PRIMARY KEY (`id`)
- [ ] Los FOREIGN KEYS referencian tablas existentes
- [ ] Los nombres en `back_populates` coinciden en ambas clases
- [ ] No hay nombres de columnas duplicados
- [ ] Las relaciones usan el tipo correcto: `Mapped["User"]` vs `Mapped[list["User"]]`
- [ ] Los campos obligatorios tienen `nullable=False`

---

## 📚 Recursos Adicionales

- [SQLAlchemy Official Documentation](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)

---

**¡Felicidades!** Ahora entiendes cómo funcionan las relaciones en SQLAlchemy. 🎉