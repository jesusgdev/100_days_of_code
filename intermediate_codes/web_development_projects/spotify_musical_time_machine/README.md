# Guía Completa: Cómo Desarrollar Spotify Musical Time Machine

## Proyecto Final
Crear una aplicación que tome las canciones del Billboard Hot 100 de cualquier fecha y cree automáticamente una playlist en Spotify.

---

## Requisitos Previos

### 1. Instalar Python (si no lo tienes)
```bash
python --version  # Verifica si ya tienes Python 3.x
```

### 2. Instalar librerías necesarias
```bash
pip install requests beautifulsoup4 python-dotenv spotipy
```

**¿Qué hace cada librería?**
- `requests`: Hace peticiones a sitios web
- `beautifulsoup4`: Extrae información de HTML
- `python-dotenv`: Lee variables de entorno desde archivo .env
- `spotipy`: Conecta con la API de Spotify

---

## PARTE 1: Configuración Inicial de Spotify

### Paso 1.1: Crear una aplicación en Spotify

1. Ve a https://developer.spotify.com/dashboard
2. Inicia sesión con tu cuenta de Spotify
3. Haz clic en "Create App"
4. Llena el formulario:
   - **App Name:** "Musical Time Machine"
   - **App Description:** "Creates playlists from Billboard charts"
   - **Redirect URI:** `http://localhost:8888/callback`
5. Acepta los términos y crea la app
6. Guarda tu **Client ID** y **Client Secret**

### Paso 1.2: Crear archivo .env

Crea un archivo llamado `.env` en la carpeta de tu proyecto:

```
SPOTIFY_CLIENT_ID=tu_client_id_aquí
SPOTIFY_CLIENT_SECRET=tu_client_secret_aquí
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

### Paso 1.3: Crear archivo .gitignore

```
.env
token.txt
__pycache__/
*.pyc
```

Esto evita subir información sensible a GitHub.

---

## PARTE 2: Desarrollo del Código (Paso a Paso)

### Paso 2.1: Importar librerías

```python
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
```

**¿Qué importamos?**
- `os`: Para trabajar con variables de entorno
- `requests`: Para obtener páginas web
- `BeautifulSoup`: Para extraer datos del HTML
- `load_dotenv`: Para cargar el archivo .env
- `spotipy` y `SpotifyOAuth`: Para conectar con Spotify

---

### Paso 2.2: Pedir fecha al usuario

```python
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
```

**Ejemplo de entrada:** `2000-08-12`

---

### Paso 2.3: Configurar el web scraping

```python
HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36"
}

URL = f"https://www.billboard.com/charts/hot-100/{date}/"
```

**¿Por qué el User-Agent?**
- Algunos sitios web bloquean bots
- El User-Agent hace que tu código parezca un navegador normal

---

### Paso 2.4: Obtener la página de Billboard

```python
try:
    response = requests.get(url=URL, headers=HEADER)
    response.encoding = "utf-8"
    response.raise_for_status()  # Si hay error (404, 500, etc.), se detiene
    billboard_html = response.text
except requests.exceptions.RequestException as e:
    print(f"Error fetching Billboard data: {e}")
    exit()
```

**¿Qué hace este código?**
1. Hace una petición GET a Billboard
2. Establece el encoding a UTF-8 para caracteres especiales
3. Verifica si hubo errores (fecha inválida, sin internet, etc.)
4. Guarda el HTML en `billboard_html`

---

### Paso 2.5: Parsear el HTML con BeautifulSoup

```python
soup = BeautifulSoup(billboard_html, "html.parser")
```

Ahora `soup` contiene el HTML estructurado que podemos buscar.

---

### Paso 2.6: Definir las clases CSS

```python
SONG_TITLE_CLASS = "c-title a-font-basic u-letter-spacing-0010..."
ARTIST_CLASS = "c-label a-no-trucate a-font-secondary..."
```

**¿Cómo encontrar estas clases?**
1. Ve a https://www.billboard.com/charts/hot-100/
2. Click derecho en un título de canción → "Inspeccionar"
3. Busca el elemento `<h3>` que contiene el nombre
4. Copia el valor del atributo `class`

**Nota:** Estas clases pueden cambiar. Si el código deja de funcionar, verifica las clases nuevamente.

---

### Paso 2.7: Extraer canciones y artistas

```python
song_tags = soup.find_all("h3", class_=SONG_TITLE_CLASS)
artist_tags = soup.find_all("span", class_=ARTIST_CLASS)
```

**Resultado:**
- `song_tags` = lista con 100 elementos `<h3>` (títulos de canciones)
- `artist_tags` = lista con 100 elementos `<span>` (nombres de artistas)

---

### Paso 2.8: Crear queries de búsqueda para Spotify

```python
search_queries = [
    f"track:{song_tags[i].get_text().strip()} artist:{artist_tags[i].get_text().strip()}"
    for i in range(min(len(song_tags), len(artist_tags)))
]
```

**Ejemplo de query generado:**
```
"track:Shape of You artist:Ed Sheeran"
```

**¿Por qué este formato?**
- Spotify busca mejor con `track:` y `artist:` explícitos
- `.strip()` quita espacios en blanco al inicio/final

---

### Paso 2.9: Autenticar con Spotify

```python
load_dotenv()  # Carga variables del archivo .env

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Verificar que las credenciales existen
if not all([SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI]):
    print("Error: Missing Spotify credentials in .env file")
    exit()
```

---

### Paso 2.10: Crear cliente de Spotify

```python
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-public playlist-modify-private",
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
```

**¿Qué pasa aquí?**
1. Se abre tu navegador
2. Te pide autorización para acceder a tu cuenta de Spotify
3. Aceptas y te redirige a `localhost:8888/callback`
4. Spotipy captura el código de autorización
5. Se guarda un token en `token.txt` para no pedir permiso cada vez

---

### Paso 2.11: Buscar canciones en Spotify

```python
track_uris = []
songs_not_found = []

# Recorrer cada query de búsqueda
for i in range(len(search_queries)):
    query = search_queries[i]
    
    try:
        # Buscar la canción en Spotify
        result = sp.search(q=query, type="track", limit=1)
        
        # Verificar si encontró alguna canción
        if result["tracks"]["items"]:
            # Extraer el URI de la primera canción encontrada
            track_uri = result["tracks"]["items"][0]["uri"]
            track_uris.append(track_uri)
            print(f"✓ Found song {i+1}/100")
        else:
            # La canción no está disponible en Spotify
            song_name = song_tags[i].get_text().strip()
            songs_not_found.append(song_name)
            print(f"✗ Not found: {song_name}")
    
    except Exception as e:
        print(f"✗ Error searching song {i+1}: {e}")
```

**Explicación línea por línea:**
1. `for i in range(len(search_queries))`: Recorre del 0 al 99 (100 canciones)
2. `query = search_queries[i]`: Obtiene la query en la posición i
3. `sp.search(q=query, type="track", limit=1)`: Busca en Spotify (máximo 1 resultado)
4. `if result["tracks"]["items"]:`: Verifica si encontró algo (lista no vacía)
5. `result["tracks"]["items"][0]`: Toma la primera canción del resultado
6. `["uri"]`: Extrae el URI (identificador único de Spotify)
7. `track_uris.append(track_uri)`: Agrega el URI a la lista
8. `i+1`: Muestra 1-100 en vez de 0-99 para el usuario

---

### Paso 2.12: Crear la playlist

```python
if track_uris:
    playlist = sp.user_playlist_create(
        user=user_id,
        name=f"Billboard Hot 100 - {date}",
        public=True,
        description=f"Top 100 songs from Billboard on {date}. Created with Python."
    )
    
    playlist_id = playlist["id"]
    print(f"Playlist created: {playlist['name']}")
```

**Parámetros:**
- `user`: Tu ID de Spotify
- `name`: Nombre de la playlist
- `public=True`: La playlist será visible públicamente
- `description`: Descripción que aparecerá en Spotify

---

### Paso 2.13: Agregar canciones a la playlist

```python
# Agregar todas las canciones encontradas a la playlist
sp.playlist_add_items(playlist_id, track_uris)

print(f"Added {len(track_uris)} songs to the playlist")
print(f"Playlist URL: https://open.spotify.com/playlist/{playlist_id}")
```

**Explicación:**
1. `sp.playlist_add_items()`: Método de Spotipy para agregar canciones
2. `playlist_id`: El ID de la playlist que acabas de crear
3. `track_uris`: La lista con todos los URIs de las canciones (máximo 100)
4. Spotify permite agregar hasta 100 canciones en una sola llamada

**Nota:** Como Billboard Top 100 tiene exactamente 100 canciones (o menos si algunas no se encontraron), no necesitamos dividir en grupos.

---

### Paso 2.14: Limpiar playlists vacías (opcional)

```python
playlists = sp.current_user_playlists(limit=50)
deleted_count = 0

for playlist in playlists["items"]:
    if playlist["owner"]["id"] == user_id and playlist["tracks"]["total"] == 0:
        sp.current_user_unfollow_playlist(playlist["id"])
        print(f"✓ Deleted empty playlist: {playlist['name']}")
        deleted_count += 1

if deleted_count > 0:
    print(f"Total empty playlists deleted: {deleted_count}")
```

**¿Para qué esto?**
- Si hubo errores anteriores, pueden quedar playlists vacías
- Este código las limpia automáticamente

---

## PARTE 3: Mejoras que Hice a Tu Código

### 1. **Manejo de errores**
```python
# Tu código original no manejaba errores de red
response = requests.get(url=URL)

# Versión mejorada
try:
    response = requests.get(url=URL, headers=HEADER)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    exit()
```

### 2. **Nombres de variables más claros**
```python
# Original
billboard_web = response.text

# Mejorado
billboard_html = response.text  # Más descriptivo
```

### 3. **Constantes en mayúsculas**
```python
# Original
header = {...}

# Mejorado
HEADER = {...}  # Convención para constantes
```

### 4. **Feedback al usuario**
```python
# Agregué mensajes de progreso
print(f"✓ {i}/100: Found")
print(f"✗ {i}/100: Not found")
```

### 5. **Validación de datos**
```python
# Verificar que encontramos las 100 canciones
if len(song_tags) < 100:
    print(f"Warning: Only found {len(song_tags)} songs")
```

### 6. **URLs de playlist**
```python
# Agregué el link directo
print(f"Playlist URL: https://open.spotify.com/playlist/{playlist_id}")
```

### 7. **Manejo del header en requests**
```python
# Original (no usabas el header)
response = requests.get(url=URL)

# Mejorado
response = requests.get(url=URL, headers=HEADER)
```

---

## PARTE 4: Estructura de Archivos del Proyecto

```
spotify-time-machine/
│
├── main.py              # Tu código principal
├── .env                 # Credenciales (NO subir a GitHub)
├── .gitignore           # Archivos a ignorar en Git
├── token.txt            # Token de Spotify (auto-generado)
└── README.md            # Documentación del proyecto
```

---

## PARTE 5: Cómo Ejecutar el Proyecto

### Primera vez:
```bash
# 1. Instalar dependencias
pip install requests beautifulsoup4 python-dotenv spotipy

# 2. Crear archivo .env con tus credenciales

# 3. Ejecutar
python main.py
```

### Siguiente veces:
```bash
python main.py
```

Ya no te pedirá autorización porque el token está guardado en `token.txt`.

---

## PARTE 6: Troubleshooting Común

### Problema 1: "Insufficient client scope"
**Solución:** Borra `token.txt` y vuelve a ejecutar

### Problema 2: "No se encontraron canciones"
**Solución:** Verifica las clases CSS en Billboard (pueden cambiar)

### Problema 3: "Invalid redirect URI"
**Solución:** El Redirect URI en tu código debe coincidir exactamente con el del dashboard de Spotify

### Problema 4: Caracteres raros (â en vez de –)
**Solución:** Ya está resuelto con `response.encoding = "utf-8"`

### Problema 5: "KeyError: 'id'"
**Solución:** Verifica que `playlist` no sea `None` antes de acceder a `playlist['id']`

---

## PARTE 7: Próximos Pasos para Mejorar

1. **Agregar interfaz gráfica** con Tkinter
2. **Crear múltiples playlists** de diferentes décadas
3. **Agregar más charts** (UK Top 40, Spotify Top 50, etc.)
4. **Análisis de datos** (géneros más populares por año)
5. **Compartir playlists** automáticamente con amigos

---

## Resumen de Conceptos Aprendidos

✓ Web scraping con BeautifulSoup
✓ Autenticación OAuth con APIs
✓ Manejo de variables de entorno
✓ Trabajo con APIs REST (Spotify)
✓ Manejo de errores y excepciones
✓ List comprehensions en Python
✓ Procesamiento de datos en batches
✓ Encoding de caracteres (UTF-8)

---

## Recursos Adicionales

- [Documentación de Spotipy](https://spotipy.readthedocs.io/)
- [BeautifulSoup Tutorial](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Spotify API Reference](https://developer.spotify.com/documentation/web-api/)
- [Billboard Charts](https://www.billboard.com/charts/)

---

**¡Felicidades!** Has creado tu primera aplicación que combina web scraping con APIs. Este proyecto demuestra habilidades valiosas en desarrollo de software.