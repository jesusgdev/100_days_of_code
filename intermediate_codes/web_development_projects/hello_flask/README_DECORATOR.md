# Guía Completa de Decoradores en Python

## 📚 Tabla de Contenidos
1. [¿Qué es un Decorador?](#qué-es-un-decorador)
2. [Funciones como Objetos](#funciones-como-objetos)
3. [Funciones Internas](#funciones-internas)
4. [Mi Primer Decorador](#mi-primer-decorador)
5. [Decoradores con Argumentos](#decoradores-con-argumentos)
6. [Preservar Metadata](#preservar-metadata)
7. [Decoradores con Parámetros](#decoradores-con-parámetros)
8. [Ejemplos Prácticos](#ejemplos-prácticos)
9. [Decoradores de Clase](#decoradores-de-clase)

---

## ¿Qué es un Decorador?

Un **decorador** es una función que toma otra función como argumento, le agrega funcionalidad extra, y retorna una nueva función sin modificar la función original.

**Analogía:** Es como envolver un regalo. La función original es el regalo, y el decorador es el papel de envolver que le agrega presentación sin cambiar el regalo en sí.

---

## Funciones como Objetos

En Python, las funciones son **objetos de primera clase**, lo que significa que pueden:
- Asignarse a variables
- Pasarse como argumentos
- Retornarse desde otras funciones

### Ejemplo 1: Funciones asignadas a variables

```python
def saludar(nombre):
    return f"Hola, {nombre}!"

# Asignar la función a una variable
mi_saludo = saludar

# Llamar la función desde la variable
print(mi_saludo("Juan"))  # Output: Hola, Juan!
```

**Explicación línea por línea:**
1. `def saludar(nombre):` - Definimos una función normal
2. `mi_saludo = saludar` - Asignamos la función a una variable (sin paréntesis)
3. `mi_saludo("Juan")` - Llamamos la función usando la variable

### Ejemplo 2: Funciones como argumentos

```python
def ejecutar_dos_veces(func, valor):
    # Esta función recibe otra función como argumento
    func(valor)  # Primera ejecución
    func(valor)  # Segunda ejecución

def imprimir_mensaje(mensaje):
    print(f"Mensaje: {mensaje}")

# Pasamos la función como argumento
ejecutar_dos_veces(imprimir_mensaje, "Hola Mundo")
```

**Output:**
```
Mensaje: Hola Mundo
Mensaje: Hola Mundo
```

**Explicación:**
1. `ejecutar_dos_veces(func, valor)` - Recibe una función y un valor
2. `func(valor)` - Ejecuta la función recibida con el valor
3. `ejecutar_dos_veces(imprimir_mensaje, "Hola Mundo")` - Pasamos `imprimir_mensaje` como argumento

---

## Funciones Internas

Puedes definir funciones **dentro de otras funciones**. Esto es fundamental para entender decoradores.

### Ejemplo 3: Función dentro de función

```python
def funcion_externa():
    mensaje = "Hola desde la función externa"
    
    def funcion_interna():
        # La función interna puede acceder a variables de la función externa
        print(mensaje)
    
    # Llamar a la función interna
    funcion_interna()

funcion_externa()  # Output: Hola desde la función externa
```

**Explicación:**
1. `def funcion_externa():` - Función contenedora
2. `mensaje = "..."` - Variable local de la función externa
3. `def funcion_interna():` - Función definida dentro de otra función
4. `funcion_interna()` - Se llama dentro de `funcion_externa`

### Ejemplo 4: Retornar una función interna

```python
def crear_multiplicador(factor):
    # Esta función retorna otra función
    def multiplicar(numero):
        return numero * factor
    
    return multiplicar  # Retornamos la función (sin ejecutarla)

# Crear diferentes multiplicadores
multiplicar_por_2 = crear_multiplicador(2)
multiplicar_por_5 = crear_multiplicador(5)

print(multiplicar_por_2(10))  # Output: 20
print(multiplicar_por_5(10))  # Output: 50
```

**Explicación:**
1. `crear_multiplicador(factor)` - Función que crea multiplicadores personalizados
2. `def multiplicar(numero):` - Función interna que usa el `factor`
3. `return multiplicar` - Retorna la función (sin paréntesis = no la ejecuta)
4. `multiplicar_por_2 = crear_multiplicador(2)` - Guarda la función retornada
5. `multiplicar_por_2(10)` - Ejecuta la función guardada con un argumento

---

## Mi Primer Decorador

Ahora que entendemos los conceptos básicos, creemos nuestro primer decorador.

### Ejemplo 5: Decorador simple

```python
def mi_decorador(func):
    # El decorador recibe una función como argumento
    
    def wrapper():
        # Función interna que "envuelve" la función original
        print("Antes de ejecutar la función")
        func()  # Ejecutar la función original
        print("Después de ejecutar la función")
    
    return wrapper  # Retornar la función wrapper

# Forma 1: Sin el símbolo @
def decir_hola():
    print("¡Hola!")

decir_hola_decorada = mi_decorador(decir_hola)
decir_hola_decorada()
```

**Output:**
```
Antes de ejecutar la función
¡Hola!
Después de ejecutar la función
```

**Explicación paso a paso:**
1. `def mi_decorador(func):` - El decorador recibe una función
2. `def wrapper():` - Creamos una función que envolverá la original
3. `print("Antes...")` - Código que se ejecuta ANTES de la función original
4. `func()` - Llamamos a la función original
5. `print("Después...")` - Código que se ejecuta DESPUÉS de la función original
6. `return wrapper` - Retornamos la función wrapper
7. `mi_decorador(decir_hola)` - Aplicamos el decorador manualmente

### Ejemplo 6: Usando el símbolo @ (sintaxis de decorador)

```python
def mi_decorador(func):
    def wrapper():
        print("Antes de ejecutar la función")
        func()
        print("Después de ejecutar la función")
    return wrapper

# Forma 2: Con el símbolo @ (más común y elegante)
@mi_decorador
def decir_hola():
    print("¡Hola!")

# Ahora decir_hola YA está decorada automáticamente
decir_hola()
```

**Explicación del símbolo @:**
- `@mi_decorador` es equivalente a: `decir_hola = mi_decorador(decir_hola)`
- Es simplemente una forma más limpia de aplicar decoradores

---

## Decoradores con Argumentos

¿Qué pasa si tu función tiene argumentos? Necesitas que el wrapper también los acepte.

### Ejemplo 7: Decorador que acepta argumentos

```python
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        # *args captura argumentos posicionales
        # **kwargs captura argumentos con nombre
        print(f"Ejecutando {func.__name__} con argumentos: {args} {kwargs}")
        resultado = func(*args, **kwargs)  # Pasar los argumentos a la función original
        print(f"Resultado: {resultado}")
        return resultado
    return wrapper

@mi_decorador
def sumar(a, b):
    return a + b

@mi_decorador
def saludar(nombre, saludo="Hola"):
    return f"{saludo}, {nombre}!"

# Usar las funciones decoradas
sumar(5, 3)
saludar("Ana")
saludar("Carlos", saludo="Buenos días")
```

**Output:**
```
Ejecutando sumar con argumentos: (5, 3) {}
Resultado: 8
Ejecutando saludar con argumentos: ('Ana',) {}
Resultado: Hola, Ana!
Ejecutando saludar con argumentos: ('Carlos',) {'saludo': 'Buenos días'}
Resultado: Buenos días, Carlos!
```

**Explicación de *args y **kwargs:**
1. `*args` - Captura todos los argumentos posicionales como una tupla
2. `**kwargs` - Captura todos los argumentos con nombre como un diccionario
3. `func(*args, **kwargs)` - Desempaqueta y pasa los argumentos a la función original

---

## Preservar Metadata

Los decoradores pueden "ocultar" información de la función original. Para evitarlo, usamos `functools.wraps`.

### Ejemplo 8: Problema sin functools.wraps

```python
def mi_decorador(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@mi_decorador
def mi_funcion():
    """Esta es la documentación de mi función"""
    pass

print(mi_funcion.__name__)  # Output: wrapper (¡Debería ser mi_funcion!)
print(mi_funcion.__doc__)   # Output: None (¡Perdimos la documentación!)
```

### Ejemplo 9: Solución con functools.wraps

```python
from functools import wraps

def mi_decorador(func):
    @wraps(func)  # Esto preserva la metadata de la función original
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@mi_decorador
def mi_funcion():
    """Esta es la documentación de mi función"""
    pass

print(mi_funcion.__name__)  # Output: mi_funcion ✓
print(mi_funcion.__doc__)   # Output: Esta es la documentación de mi función ✓
```

**Explicación:**
- `@wraps(func)` copia el nombre, documentación y otros atributos de `func` a `wrapper`
- **Siempre usa `@wraps(func)` en tus decoradores**

---

## Decoradores con Parámetros

¿Y si quieres pasar argumentos al decorador mismo? Necesitas una función extra.

### Ejemplo 10: Decorador con parámetros

```python
from functools import wraps

def repetir(veces):
    # Nivel 1: Recibe los parámetros del decorador
    def decorador(func):
        # Nivel 2: Recibe la función a decorar
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Nivel 3: Ejecuta la función múltiples veces
            for i in range(veces):
                print(f"Ejecución {i + 1}:")
                resultado = func(*args, **kwargs)
            return resultado
        return wrapper
    return decorador

@repetir(veces=3)
def saludar(nombre):
    print(f"¡Hola, {nombre}!")

saludar("María")
```

**Output:**
```
Ejecución 1:
¡Hola, María!
Ejecución 2:
¡Hola, María!
Ejecución 3:
¡Hola, María!
```

**Explicación de los 3 niveles:**
1. `def repetir(veces):` - Recibe parámetros del decorador
2. `def decorador(func):` - Recibe la función a decorar
3. `def wrapper(*args, **kwargs):` - Envuelve la función con la lógica extra
4. `@repetir(veces=3)` - Se llama `repetir(3)` que retorna el decorador, que luego se aplica a la función

---

## Ejemplos Prácticos

### Ejemplo 11: Medir tiempo de ejecución

```python
import time
from functools import wraps

def medir_tiempo(func):
    """Decorador que mide cuánto tarda una función en ejecutarse"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()  # Tiempo antes de ejecutar
        resultado = func(*args, **kwargs)  # Ejecutar la función
        fin = time.time()  # Tiempo después de ejecutar
        
        tiempo_total = fin - inicio
        print(f"{func.__name__} tardó {tiempo_total:.4f} segundos")
        return resultado
    return wrapper

@medir_tiempo
def proceso_lento():
    time.sleep(2)  # Simular un proceso que tarda 2 segundos
    print("Proceso completado")

proceso_lento()
```

**Output:**
```
Proceso completado
proceso_lento tardó 2.0023 segundos
```

### Ejemplo 12: Validar tipos de argumentos

```python
from functools import wraps

def validar_tipos(*tipos):
    """Decorador que valida que los argumentos sean del tipo correcto"""
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Verificar cada argumento con su tipo esperado
            for arg, tipo_esperado in zip(args, tipos):
                if not isinstance(arg, tipo_esperado):
                    raise TypeError(f"Se esperaba {tipo_esperado}, se recibió {type(arg)}")
            return func(*args, **kwargs)
        return wrapper
    return decorador

@validar_tipos(int, int)
def sumar(a, b):
    return a + b

print(sumar(5, 3))       # ✓ Funciona: 8
# print(sumar(5, "3"))   # ✗ Error: TypeError
```

### Ejemplo 13: Cache/Memoización

```python
from functools import wraps

def cache(func):
    """Decorador que guarda resultados previos para evitar recalcular"""
    resultados_guardados = {}  # Diccionario para guardar resultados
    
    @wraps(func)
    def wrapper(*args):
        if args in resultados_guardados:
            print(f"Usando resultado guardado para {args}")
            return resultados_guardados[args]
        
        print(f"Calculando resultado para {args}")
        resultado = func(*args)
        resultados_guardados[args] = resultado  # Guardar resultado
        return resultado
    return wrapper

@cache
def fibonacci(n):
    """Calcula el número de Fibonacci de forma recursiva"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(5))
print(fibonacci(5))  # Esta vez usa el resultado guardado
```

### Ejemplo 14: Logging automático

```python
from functools import wraps
from datetime import datetime

def log(func):
    """Decorador que registra cada llamada a la función"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Llamando a {func.__name__}")
        print(f"  Argumentos: {args} {kwargs}")
        
        resultado = func(*args, **kwargs)
        
        print(f"  Resultado: {resultado}")
        return resultado
    return wrapper

@log
def dividir(a, b):
    return a / b

dividir(10, 2)
```

**Output:**
```
[2025-10-19 14:30:45] Llamando a dividir
  Argumentos: (10, 2) {}
  Resultado: 5.0
```

### Ejemplo 15: Autenticación/Autorización

```python
from functools import wraps

# Simular un usuario logueado
usuario_actual = {"nombre": "Juan", "es_admin": False}

def requiere_admin(func):
    """Decorador que verifica si el usuario es administrador"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not usuario_actual.get("es_admin"):
            raise PermissionError("Se requieren permisos de administrador")
        return func(*args, **kwargs)
    return wrapper

@requiere_admin
def eliminar_usuario(user_id):
    print(f"Usuario {user_id} eliminado")

# eliminar_usuario(123)  # ✗ Error: PermissionError

# Cambiar a admin
usuario_actual["es_admin"] = True
eliminar_usuario(123)  # ✓ Funciona
```

---

## Decoradores de Clase

También puedes aplicar decoradores a clases completas.

### Ejemplo 16: Decorador de clase simple

```python
def agregar_metodo_str(cls):
    """Decorador que agrega un método __str__ a la clase"""
    def __str__(self):
        return f"{cls.__name__}: {self.__dict__}"
    
    cls.__str__ = __str__  # Agregar el método a la clase
    return cls

@agregar_metodo_str
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

persona = Persona("Ana", 25)
print(persona)  # Output: Persona: {'nombre': 'Ana', 'edad': 25}
```

### Ejemplo 17: Singleton con decorador

```python
from functools import wraps

def singleton(cls):
    """Decorador que asegura que solo exista una instancia de la clase"""
    instancias = {}
    
    @wraps(cls)
    def get_instancia(*args, **kwargs):
        if cls not in instancias:
            instancias[cls] = cls(*args, **kwargs)
        return instancias[cls]
    
    return get_instancia

@singleton
class BaseDeDatos:
    def __init__(self):
        print("Conectando a la base de datos...")

# Ambas variables apuntan a la MISMA instancia
db1 = BaseDeDatos()  # Output: Conectando a la base de datos...
db2 = BaseDeDatos()  # No imprime nada, usa la instancia existente

print(db1 is db2)  # Output: True
```

---

## 🎯 Resumen de Conceptos Clave

1. **Decorador básico:** Función que envuelve otra función
2. **@decorador:** Sintaxis para aplicar decoradores de forma limpia
3. ***args, **kwargs:** Para aceptar cualquier cantidad de argumentos
4. **@wraps(func):** Preserva metadata de la función original
5. **Decoradores con parámetros:** Requieren 3 niveles de funciones
6. **Usos prácticos:** Logging, timing, caching, validación, autenticación

---

## 📝 Plantilla de Decorador

```python
from functools import wraps

def mi_decorador(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Código antes de ejecutar la función
        resultado = func(*args, **kwargs)
        # Código después de ejecutar la función
        return resultado
    return wrapper
```

---

## 🚀 Tips Finales

1. Siempre usa `@wraps(func)` en tus decoradores
2. Usa `*args, **kwargs` para flexibilidad
3. Los decoradores no modifican la función original, la envuelven
4. Puedes apilar múltiples decoradores: `@decorador1 @decorador2`
5. Los decoradores se aplican de abajo hacia arriba

---

## 📚 Recursos Adicionales

- [PEP 318 - Decorators for Functions and Methods](https://www.python.org/dev/peps/pep-0318/)
- [Real Python - Primer on Python Decorators](https://realpython.com/primer-on-python-decorators/)
- [Python Docs - functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)