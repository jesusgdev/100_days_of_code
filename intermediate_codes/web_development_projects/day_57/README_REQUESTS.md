# Guía Completa de Requests para APIs en Python

## ¿Qué es Requests?

`requests` es una librería de Python que facilita realizar peticiones HTTP. Es la forma más simple y elegante de interactuar con APIs REST, consumir servicios web y hacer solicitudes a servidores.

## Instalación

```bash
pip install requests
```

---

## 1. Importar la Librería

```python
import requests
```

**Explicación:**
- Importamos la librería `requests` para poder usar todas sus funcionalidades
- Debe estar instalada previamente con pip

---

## 2. GET - Obtener Datos de una API

### Ejemplo Básico

```python
import requests

# Realizamos una petición GET a una API pública
response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

# Imprimimos el código de estado
print(response.status_code)

# Imprimimos el contenido en formato JSON
print(response.json())
```

**Explicación línea por línea:**
- `response = requests.get(...)` - Enviamos una petición GET a la URL especificada y guardamos la respuesta
- `response.status_code` - Obtenemos el código HTTP (200 = éxito, 404 = no encontrado, etc.)
- `response.json()` - Convierte automáticamente la respuesta JSON en un diccionario de Python

### GET con Parámetros

```python
import requests

# Definimos los parámetros de búsqueda
parametros = {
    'userId': 1,
    'id': 5
}

# Realizamos GET con parámetros
response = requests.get(
    'https://jsonplaceholder.typicode.com/posts',
    params=parametros
)

print(response.url)  # Muestra la URL completa con parámetros
print(response.json())
```

**Explicación línea por línea:**
- `parametros = {...}` - Creamos un diccionario con los parámetros que queremos enviar
- `params=parametros` - Requests automáticamente añade estos parámetros a la URL como `?userId=1&id=5`
- `response.url` - Muestra la URL final construida con los parámetros

---

## 3. POST - Enviar Datos a una API

### POST con JSON

```python
import requests

# Datos que queremos enviar
nuevo_post = {
    'title': 'Mi Nuevo Post',
    'body': 'Este es el contenido de mi post',
    'userId': 1
}

# Enviamos una petición POST
response = requests.post(
    'https://jsonplaceholder.typicode.com/posts',
    json=nuevo_post
)

print(f"Código de estado: {response.status_code}")
print(f"Respuesta del servidor: {response.json()}")
```

**Explicación línea por línea:**
- `nuevo_post = {...}` - Creamos un diccionario con los datos que queremos enviar
- `json=nuevo_post` - Requests automáticamente convierte el diccionario a JSON y establece el header `Content-Type: application/json`
- El servidor responde con el objeto creado (usualmente incluye un ID generado)

### POST con Datos de Formulario

```python
import requests

# Datos en formato formulario
datos_formulario = {
    'username': 'usuario123',
    'password': 'mipassword'
}

# Enviamos como formulario (application/x-www-form-urlencoded)
response = requests.post(
    'https://httpbin.org/post',
    data=datos_formulario
)

print(response.json())
```

**Explicación línea por línea:**
- `data=datos_formulario` - Usa `data` en lugar de `json` para enviar como formulario
- Este formato es común en formularios HTML tradicionales
- El Content-Type será `application/x-www-form-urlencoded`

---

## 4. PUT - Actualizar Datos Completamente

```python
import requests

# Datos actualizados (reemplaza TODO el recurso)
post_actualizado = {
    'id': 1,
    'title': 'Título Actualizado',
    'body': 'Contenido completamente nuevo',
    'userId': 1
}

# Enviamos PUT para actualizar
response = requests.put(
    'https://jsonplaceholder.typicode.com/posts/1',
    json=post_actualizado
)

print(f"Código: {response.status_code}")
print(response.json())
```

**Explicación línea por línea:**
- `requests.put(...)` - PUT reemplaza completamente el recurso en el servidor
- Incluimos el ID en la URL (`/posts/1`) para especificar qué recurso actualizar
- Todos los campos deben enviarse, no solo los que cambian

---

## 5. PATCH - Actualizar Datos Parcialmente

```python
import requests

# Solo enviamos los campos que queremos cambiar
cambios_parciales = {
    'title': 'Solo cambio el título'
}

# Enviamos PATCH para actualización parcial
response = requests.patch(
    'https://jsonplaceholder.typicode.com/posts/1',
    json=cambios_parciales
)

print(response.json())
```

**Explicación línea por línea:**
- `requests.patch(...)` - PATCH actualiza solo los campos especificados
- No necesitamos enviar todos los campos del recurso
- Más eficiente que PUT cuando solo cambias algunos campos

---

## 6. DELETE - Eliminar Datos

```python
import requests

# Eliminamos un recurso
response = requests.delete('https://jsonplaceholder.typicode.com/posts/1')

print(f"Código de estado: {response.status_code}")

# 204 significa "eliminado exitosamente, sin contenido"
if response.status_code == 204:
    print("Recurso eliminado exitosamente")
```

**Explicación línea por línea:**
- `requests.delete(...)` - Envía una petición DELETE al servidor
- Especificamos el recurso exacto a eliminar en la URL
- Usualmente retorna código 204 (No Content) si fue exitoso

---

## 7. Headers Personalizados

```python
import requests

# Definimos headers personalizados
headers = {
    'User-Agent': 'MiApp/1.0',
    'Authorization': 'Bearer mi_token_secreto',
    'Content-Type': 'application/json'
}

# Enviamos la petición con headers
response = requests.get(
    'https://api.ejemplo.com/datos',
    headers=headers
)

print(response.status_code)
```

**Explicación línea por línea:**
- `headers = {...}` - Creamos un diccionario con los headers HTTP que queremos enviar
- `User-Agent` - Identifica nuestra aplicación
- `Authorization` - Header común para autenticación (Bearer tokens, API keys, etc.)
- `headers=headers` - Pasamos nuestros headers personalizados a la petición

---

## 8. Autenticación Básica

```python
import requests
from requests.auth import HTTPBasicAuth

# Opción 1: Usando HTTPBasicAuth
response = requests.get(
    'https://api.ejemplo.com/datos',
    auth=HTTPBasicAuth('usuario', 'password')
)

# Opción 2: Forma abreviada (tupla)
response = requests.get(
    'https://api.ejemplo.com/datos',
    auth=('usuario', 'password')
)

print(response.status_code)
```

**Explicación línea por línea:**
- `from requests.auth import HTTPBasicAuth` - Importamos la clase para autenticación básica
- `auth=HTTPBasicAuth(...)` - Requests maneja automáticamente la codificación Base64 requerida
- `auth=('usuario', 'password')` - Forma simplificada, hace lo mismo que HTTPBasicAuth
- La autenticación básica envía credenciales en cada petición

---

## 9. Manejo de Timeouts

```python
import requests

try:
    # Timeout de 5 segundos
    response = requests.get(
        'https://api.ejemplo.com/datos',
        timeout=5
    )
    print(response.json())
    
except requests.Timeout:
    print("La petición tardó demasiado y se canceló")
    
except requests.RequestException as e:
    print(f"Error en la petición: {e}")
```

**Explicación línea por línea:**
- `timeout=5` - Si el servidor no responde en 5 segundos, se lanza una excepción
- `except requests.Timeout` - Capturamos específicamente errores de timeout
- `except requests.RequestException` - Captura cualquier otro error de requests
- Los timeouts previenen que tu aplicación se quede esperando indefinidamente

---

## 10. Manejo de Errores y Códigos de Estado

```python
import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts/999999')

# Verificar si la petición fue exitosa
if response.status_code == 200:
    print("Éxito!")
    print(response.json())
elif response.status_code == 404:
    print("Recurso no encontrado")
elif response.status_code == 500:
    print("Error del servidor")
else:
    print(f"Código de estado: {response.status_code}")

# Forma alternativa: lanzar excepción si hay error
try:
    response.raise_for_status()
except requests.HTTPError as e:
    print(f"Error HTTP: {e}")
```

**Explicación línea por línea:**
- `response.status_code` - Contiene el código HTTP de la respuesta
- `200` - Éxito
- `404` - No encontrado
- `500` - Error interno del servidor
- `response.raise_for_status()` - Lanza una excepción automáticamente si el código es 4xx o 5xx
- `requests.HTTPError` - Excepción específica para errores HTTP

---

## 11. Trabajar con Respuestas

```python
import requests

response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

# Diferentes formas de acceder a la respuesta
print(response.text)           # Contenido como string
print(response.json())         # Contenido como diccionario (si es JSON)
print(response.content)        # Contenido como bytes
print(response.headers)        # Headers de la respuesta
print(response.encoding)       # Codificación detectada
print(response.url)           # URL final (después de redirecciones)
```

**Explicación línea por línea:**
- `response.text` - Contenido decodificado como string (útil para HTML, XML, texto)
- `response.json()` - Parsea automáticamente JSON a diccionario Python
- `response.content` - Bytes crudos (útil para imágenes, PDFs, archivos)
- `response.headers` - Diccionario con todos los headers de respuesta del servidor
- `response.encoding` - Codificación de caracteres (UTF-8, ISO-8859-1, etc.)
- `response.url` - URL final después de redirecciones

---

## 12. Sesiones - Mantener Cookies y Configuración

```python
import requests

# Creamos una sesión
session = requests.Session()

# Configuramos headers que se usarán en todas las peticiones
session.headers.update({
    'User-Agent': 'MiApp/1.0'
})

# Todas estas peticiones comparten cookies y configuración
response1 = session.get('https://httpbin.org/cookies/set/sessioncookie/123')
response2 = session.get('https://httpbin.org/cookies')

print(response2.json())  # Veremos la cookie que se estableció

# Cerramos la sesión cuando terminamos
session.close()
```

**Explicación línea por línea:**
- `session = requests.Session()` - Crea un objeto de sesión que mantiene estado
- `session.headers.update(...)` - Headers que se aplicarán a todas las peticiones de la sesión
- Las sesiones mantienen cookies automáticamente entre peticiones
- `session.get(...)` - Funciona igual que `requests.get()` pero con estado compartido
- `session.close()` - Libera recursos de red (buena práctica)
- Las sesiones son útiles para APIs que requieren login o mantienen estado

---

## 13. Descargar Archivos

```python
import requests

# Descargar un archivo pequeño
response = requests.get('https://www.example.com/imagen.jpg')

# Guardar el archivo
with open('imagen_descargada.jpg', 'wb') as archivo:
    archivo.write(response.content)

print("Archivo descargado exitosamente")
```

**Explicación línea por línea:**
- `response.content` - Obtenemos el contenido como bytes (no como texto)
- `open(..., 'wb')` - Abrimos archivo en modo escritura binaria ('wb')
- `archivo.write(response.content)` - Escribimos los bytes al archivo
- Usamos `with` para cerrar el archivo automáticamente

### Descargar Archivos Grandes (Streaming)

```python
import requests

# Stream para archivos grandes (no carga todo en memoria)
response = requests.get(
    'https://www.example.com/archivo_grande.zip',
    stream=True
)

# Guardar por chunks (pedazos)
with open('archivo_grande.zip', 'wb') as archivo:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            archivo.write(chunk)

print("Descarga completada")
```

**Explicación línea por línea:**
- `stream=True` - No descarga todo inmediatamente, lo hace por partes
- `response.iter_content(chunk_size=8192)` - Lee el archivo en bloques de 8KB
- `for chunk in ...` - Procesa cada bloque uno por uno
- Esto evita llenar la memoria RAM con archivos grandes

---

## 14. Ejemplo Práctico Completo - Consumir API Real

```python
import requests
import json

def obtener_datos_pokemon(nombre):
    """
    Obtiene información de un Pokemon desde la PokeAPI
    """
    # URL base de la API
    url = f'https://pokeapi.co/api/v2/pokemon/{nombre.lower()}'
    
    try:
        # Hacemos la petición con timeout
        response = requests.get(url, timeout=10)
        
        # Verificamos que fue exitosa
        response.raise_for_status()
        
        # Parseamos la respuesta JSON
        datos = response.json()
        
        # Extraemos información relevante
        info_pokemon = {
            'nombre': datos['name'].capitalize(),
            'id': datos['id'],
            'altura': datos['height'],
            'peso': datos['weight'],
            'tipos': [tipo['type']['name'] for tipo in datos['types']],
            'habilidades': [hab['ability']['name'] for hab in datos['abilities']]
        }
        
        return info_pokemon
        
    except requests.Timeout:
        return {'error': 'La petición tardó demasiado'}
    
    except requests.HTTPError as e:
        if response.status_code == 404:
            return {'error': f'Pokemon "{nombre}" no encontrado'}
        return {'error': f'Error HTTP: {e}'}
    
    except requests.RequestException as e:
        return {'error': f'Error en la petición: {e}'}

# Usar la función
pokemon = obtener_datos_pokemon('pikachu')

if 'error' in pokemon:
    print(f"Error: {pokemon['error']}")
else:
    print(json.dumps(pokemon, indent=2, ensure_ascii=False))
```

**Explicación línea por línea:**
- `def obtener_datos_pokemon(nombre):` - Definimos función que recibe el nombre del Pokemon
- `url = f'https://...'` - Construimos la URL usando f-string con el nombre
- `nombre.lower()` - La API requiere nombres en minúsculas
- `timeout=10` - Esperamos máximo 10 segundos
- `response.raise_for_status()` - Lanza excepción si el código no es 2xx
- `datos = response.json()` - Convertimos JSON a diccionario
- `[tipo['type']['name'] for tipo in datos['types']]` - List comprehension para extraer nombres de tipos
- `except requests.Timeout` - Manejamos timeout específicamente
- `except requests.HTTPError` - Manejamos errores HTTP (404, 500, etc.)
- `except requests.RequestException` - Catch-all para otros errores de requests
- `json.dumps(..., indent=2)` - Formatea el JSON con indentación bonita
- `ensure_ascii=False` - Permite caracteres especiales (tildes, ñ, etc.)

---

## 15. Tips y Mejores Prácticas

### Usar Context Manager con Sesiones

```python
import requests

# Forma recomendada: la sesión se cierra automáticamente
with requests.Session() as session:
    session.headers.update({'Authorization': 'Bearer token123'})
    response = session.get('https://api.ejemplo.com/datos')
    print(response.json())
# Aquí la sesión ya está cerrada automáticamente
```

**Explicación:**
- `with requests.Session() as session:` - Crea sesión que se cierra automáticamente
- No necesitas llamar `session.close()` manualmente
- Más seguro y limpio

### Verificar SSL (Certificados)

```python
import requests

# Por defecto, requests verifica certificados SSL
response = requests.get('https://api.segura.com')

# Deshabilitar verificación SSL (NO RECOMENDADO en producción)
response = requests.get('https://api.insegura.com', verify=False)

# Usar un certificado personalizado
response = requests.get('https://api.com', verify='/ruta/al/certificado.pem')
```

**Explicación:**
- `verify=True` (default) - Verifica que el certificado SSL sea válido
- `verify=False` - Deshabilita verificación (solo para desarrollo/testing)
- `verify='/ruta/...'` - Usa un certificado específico

---

## Códigos de Estado HTTP Comunes

| Código | Significado |
|--------|-------------|
| 200 | OK - Petición exitosa |
| 201 | Created - Recurso creado exitosamente |
| 204 | No Content - Exitoso pero sin contenido (común en DELETE) |
| 400 | Bad Request - La petición está mal formada |
| 401 | Unauthorized - No autenticado |
| 403 | Forbidden - No autorizado (aunque estés autenticado) |
| 404 | Not Found - Recurso no encontrado |
| 429 | Too Many Requests - Has excedido el límite de peticiones |
| 500 | Internal Server Error - Error del servidor |
| 502 | Bad Gateway - El servidor recibió una respuesta inválida |
| 503 | Service Unavailable - Servidor temporalmente no disponible |

---

## Recursos Adicionales

- **Documentación Oficial:** https://requests.readthedocs.io/
- **API de prueba gratuita:** https://jsonplaceholder.typicode.com/
- **Otra API de prueba:** https://httpbin.org/
- **PokeAPI (ejemplo real):** https://pokeapi.co/

---

## Resumen de Métodos Principales

```python
# GET - Obtener datos
requests.get(url, params=dict, headers=dict, timeout=int)

# POST - Crear datos
requests.post(url, json=dict, data=dict, headers=dict)

# PUT - Actualizar completamente
requests.put(url, json=dict, headers=dict)

# PATCH - Actualizar parcialmente
requests.patch(url, json=dict, headers=dict)

# DELETE - Eliminar datos
requests.delete(url, headers=dict)
```

---

**¡Felicitaciones!** Ahora tienes una guía completa para trabajar con APIs usando Requests en Python. Practica con APIs públicas y gradualmente avanza a proyectos más complejos.