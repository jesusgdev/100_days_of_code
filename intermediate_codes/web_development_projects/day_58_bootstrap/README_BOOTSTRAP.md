# Guía Completa de Bootstrap

## ¿Qué es Bootstrap?

Bootstrap es el framework CSS más popular del mundo para crear sitios web responsive y mobile-first. Ofrece componentes prediseñados, un sistema de grid flexible y utilidades CSS que aceleran el desarrollo web.

## Instalación

### Opción 1: CDN (Más Rápida)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Sitio Bootstrap</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    
    <!-- Tu contenido aquí -->
    
    <!-- Bootstrap JS (al final del body) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**Explicación línea por línea:**
- `<meta name="viewport"...>` - Esencial para que el diseño responsive funcione en móviles
- `<link href="...bootstrap.min.css">` - Carga los estilos CSS de Bootstrap desde un CDN
- `<script src="...bootstrap.bundle.min.js">` - Carga JavaScript de Bootstrap (incluye Popper.js para tooltips y dropdowns)
- Se coloca al final del `<body>` para no bloquear la carga de la página

### Opción 2: NPM (Para Proyectos con Node.js)

```bash
npm install bootstrap
```

---

## 1. Sistema de Grid - La Base de Bootstrap

El sistema de grid usa 12 columnas y es totalmente responsive.

```html
<div class="container">
    <div class="row">
        <div class="col-md-4">
            Columna 1 (ocupa 4 de 12 columnas)
        </div>
        <div class="col-md-4">
            Columna 2 (ocupa 4 de 12 columnas)
        </div>
        <div class="col-md-4">
            Columna 3 (ocupa 4 de 12 columnas)
        </div>
    </div>
</div>
```

**Explicación línea por línea:**
- `<div class="container">` - Contenedor principal con márgenes laterales automáticos
- `<div class="row">` - Fila que agrupa columnas
- `<div class="col-md-4">` - Columna que ocupa 4/12 del ancho en pantallas medianas (≥768px)
- `md` significa "medium" - en móviles las columnas se apilarán verticalmente
- El total siempre suma 12: 4 + 4 + 4 = 12

### Grid Responsive Avanzado

```html
<div class="container">
    <div class="row">
        <div class="col-12 col-sm-6 col-md-4 col-lg-3">
            Columna Responsive
        </div>
        <div class="col-12 col-sm-6 col-md-4 col-lg-3">
            Columna Responsive
        </div>
        <div class="col-12 col-sm-6 col-md-4 col-lg-3">
            Columna Responsive
        </div>
        <div class="col-12 col-sm-6 col-md-4 col-lg-3">
            Columna Responsive
        </div>
    </div>
</div>
```

**Explicación línea por línea:**
- `col-12` - En móviles extra pequeños (< 576px): ocupa todo el ancho (100%)
- `col-sm-6` - En móviles pequeños (≥576px): ocupa 6/12 (50%) - 2 columnas por fila
- `col-md-4` - En tablets (≥768px): ocupa 4/12 (33.33%) - 3 columnas por fila
- `col-lg-3` - En desktop (≥992px): ocupa 3/12 (25%) - 4 columnas por fila
- Esto crea un diseño que se adapta automáticamente al tamaño de pantalla

---

## 2. Contenedores

```html
<!-- Contenedor con ancho fijo y centrado -->
<div class="container">
    Contenido con márgenes laterales
</div>

<!-- Contenedor de ancho completo -->
<div class="container-fluid">
    Contenido que ocupa todo el ancho
</div>

<!-- Contenedor responsive con breakpoints -->
<div class="container-md">
    Se comporta como fluid en móviles, como container en tablets+
</div>
```

**Explicación línea por línea:**
- `.container` - Ancho máximo según breakpoint, centrado con padding lateral
- `.container-fluid` - Siempre ocupa el 100% del ancho de la ventana
- `.container-md` - Fluid hasta tablets, luego se comporta como container normal
- Los contenedores son la base para usar el sistema de grid

---

## 3. Tipografía

```html
<!-- Encabezados -->
<h1>Encabezado H1</h1>
<h2>Encabezado H2</h2>
<p class="h1">Párrafo con estilo de H1</p>

<!-- Display headings (más grandes y llamativos) -->
<h1 class="display-1">Display 1</h1>
<h1 class="display-4">Display 4</h1>

<!-- Lead text (texto destacado) -->
<p class="lead">
    Este es un párrafo destacado que resalta del resto del texto.
</p>

<!-- Utilidades de texto -->
<p class="text-start">Texto alineado a la izquierda</p>
<p class="text-center">Texto centrado</p>
<p class="text-end">Texto alineado a la derecha</p>

<p class="text-uppercase">texto en mayúsculas</p>
<p class="text-lowercase">TEXTO EN MINÚSCULAS</p>
<p class="text-capitalize">capitaliza cada palabra</p>

<p class="fw-bold">Texto en negrita</p>
<p class="fst-italic">Texto en cursiva</p>
```

**Explicación línea por línea:**
- `<h1>` a `<h6>` - Encabezados estilizados automáticamente por Bootstrap
- `.h1` a `.h6` - Clases para aplicar estilo de encabezado a cualquier elemento
- `.display-1` a `.display-6` - Encabezados extra grandes para títulos principales
- `.lead` - Hace que el párrafo se destaque con mayor tamaño y peso
- `.text-start/center/end` - Alineación de texto (start/end en lugar de left/right para soporte RTL)
- `.text-uppercase/lowercase/capitalize` - Transformación de texto
- `.fw-bold` - Font weight bold (negrita)
- `.fst-italic` - Font style italic (cursiva)

---

## 4. Colores

```html
<!-- Colores de texto -->
<p class="text-primary">Texto azul primario</p>
<p class="text-secondary">Texto gris secundario</p>
<p class="text-success">Texto verde éxito</p>
<p class="text-danger">Texto rojo peligro</p>
<p class="text-warning">Texto amarillo advertencia</p>
<p class="text-info">Texto cyan información</p>

<!-- Colores de fondo -->
<div class="bg-primary text-white p-3">Fondo azul con texto blanco</div>
<div class="bg-success text-white p-3">Fondo verde</div>
<div class="bg-warning text-dark p-3">Fondo amarillo</div>

<!-- Colores más sutiles (light) -->
<div class="bg-primary-subtle">Fondo azul claro</div>
<div class="bg-success-subtle">Fondo verde claro</div>
```

**Explicación línea por línea:**
- `.text-primary` - Color de texto azul (color principal de tu tema)
- `.text-success` - Verde para acciones exitosas
- `.text-danger` - Rojo para errores o acciones destructivas
- `.text-warning` - Amarillo para advertencias
- `.bg-primary` - Color de fondo azul
- `.text-white` - Texto blanco para contraste sobre fondos oscuros
- `.p-3` - Padding de tamaño 3 (explicado en sección de espaciado)
- `-subtle` - Versión más clara y suave del color

---

## 5. Botones

```html
<!-- Botones básicos -->
<button class="btn btn-primary">Botón Primario</button>
<button class="btn btn-secondary">Botón Secundario</button>
<button class="btn btn-success">Éxito</button>
<button class="btn btn-danger">Peligro</button>
<button class="btn btn-warning">Advertencia</button>
<button class="btn btn-info">Información</button>

<!-- Botones outline (solo borde) -->
<button class="btn btn-outline-primary">Outline Primario</button>
<button class="btn btn-outline-danger">Outline Peligro</button>

<!-- Tamaños de botones -->
<button class="btn btn-primary btn-lg">Botón Grande</button>
<button class="btn btn-primary">Botón Normal</button>
<button class="btn btn-primary btn-sm">Botón Pequeño</button>

<!-- Botón de ancho completo -->
<button class="btn btn-primary w-100">Botón Ancho Completo</button>

<!-- Botón deshabilitado -->
<button class="btn btn-primary" disabled>Deshabilitado</button>

<!-- Grupo de botones -->
<div class="btn-group" role="group">
    <button class="btn btn-primary">Izquierda</button>
    <button class="btn btn-primary">Centro</button>
    <button class="btn btn-primary">Derecha</button>
</div>
```

**Explicación línea por línea:**
- `.btn` - Clase base obligatoria para todos los botones
- `.btn-primary` - Estilo de botón con color principal (azul)
- `.btn-outline-primary` - Botón transparente con solo borde azul
- `.btn-lg` - Botón grande (large)
- `.btn-sm` - Botón pequeño (small)
- `.w-100` - Width 100% (ancho completo del contenedor)
- `disabled` - Atributo HTML que deshabilita el botón
- `.btn-group` - Agrupa botones uno al lado del otro sin espacios

---

## 6. Tarjetas (Cards)

```html
<div class="card" style="width: 18rem;">
    <img src="imagen.jpg" class="card-img-top" alt="Descripción">
    <div class="card-body">
        <h5 class="card-title">Título de la Tarjeta</h5>
        <p class="card-text">
            Contenido de la tarjeta con información relevante.
        </p>
        <a href="#" class="btn btn-primary">Ver Más</a>
    </div>
</div>
```

**Explicación línea por línea:**
- `.card` - Contenedor principal de la tarjeta con bordes y sombra
- `style="width: 18rem;"` - Ancho fijo (puedes usar clases de Bootstrap también)
- `.card-img-top` - Imagen que va en la parte superior de la tarjeta
- `.card-body` - Contenedor para el contenido principal con padding
- `.card-title` - Título estilizado de la tarjeta
- `.card-text` - Texto del contenido con espaciado apropiado
- Botón dentro de card-body para acciones

### Card con Header y Footer

```html
<div class="card">
    <div class="card-header">
        Encabezado de la Tarjeta
    </div>
    <div class="card-body">
        <h5 class="card-title">Título Especial</h5>
        <p class="card-text">Contenido de la tarjeta.</p>
        <a href="#" class="btn btn-primary">Acción</a>
    </div>
    <div class="card-footer text-muted">
        Hace 2 días
    </div>
</div>
```

**Explicación línea por línea:**
- `.card-header` - Sección superior con fondo gris claro
- `.card-body` - Sección central con el contenido principal
- `.card-footer` - Sección inferior separada del body
- `.text-muted` - Texto gris apagado para información secundaria

---

## 7. Navbar (Barra de Navegación)

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Mi Sitio</a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" href="#">Inicio</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Servicios</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Contacto</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

**Explicación línea por línea:**
- `.navbar` - Clase base para la barra de navegación
- `.navbar-expand-lg` - Se colapsa en móviles, se expande en pantallas large (≥992px)
- `.navbar-dark` - Estilo oscuro con texto blanco
- `.bg-dark` - Fondo negro/gris oscuro
- `.navbar-brand` - Logo o nombre del sitio con estilo especial
- `.navbar-toggler` - Botón hamburguesa que aparece en móviles
- `data-bs-toggle="collapse"` - Indica que controla un elemento colapsable
- `data-bs-target="#navbarNav"` - ID del elemento que se colapsa/expande
- `.navbar-toggler-icon` - El ícono de hamburguesa (tres líneas)
- `.collapse navbar-collapse` - Contenedor que se oculta en móviles
- `.navbar-nav` - Lista de navegación
- `.nav-item` - Cada elemento de la lista
- `.nav-link` - Enlaces con estilo de navbar
- `.active` - Marca el enlace de la página actual

---

## 8. Formularios

```html
<form>
    <!-- Campo de texto -->
    <div class="mb-3">
        <label for="nombre" class="form-label">Nombre</label>
        <input type="text" class="form-control" id="nombre" placeholder="Juan Pérez">
    </div>
    
    <!-- Email -->
    <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" class="form-control" id="email" placeholder="correo@ejemplo.com">
        <div class="form-text">Nunca compartiremos tu email.</div>
    </div>
    
    <!-- Select (dropdown) -->
    <div class="mb-3">
        <label for="pais" class="form-label">País</label>
        <select class="form-select" id="pais">
            <option selected>Selecciona...</option>
            <option value="mx">México</option>
            <option value="ar">Argentina</option>
            <option value="es">España</option>
        </select>
    </div>
    
    <!-- Textarea -->
    <div class="mb-3">
        <label for="mensaje" class="form-label">Mensaje</label>
        <textarea class="form-control" id="mensaje" rows="3"></textarea>
    </div>
    
    <!-- Checkbox -->
    <div class="mb-3 form-check">
        <input type="checkbox" class="form-check-input" id="terminos">
        <label class="form-check-label" for="terminos">
            Acepto los términos y condiciones
        </label>
    </div>
    
    <!-- Botón de envío -->
    <button type="submit" class="btn btn-primary">Enviar</button>
</form>
```

**Explicación línea por línea:**
- `.mb-3` - Margin bottom de tamaño 3 (espaciado entre campos)
- `.form-label` - Estilo para etiquetas de formulario
- `.form-control` - Estilo para inputs de texto, email, number, textarea
- `placeholder` - Texto de ayuda dentro del campo
- `.form-text` - Texto de ayuda debajo del campo (gris y pequeño)
- `.form-select` - Estilo para elementos `<select>` (dropdown)
- `rows="3"` - Altura del textarea en líneas
- `.form-check` - Contenedor para checkbox/radio
- `.form-check-input` - Estilo para checkbox/radio
- `.form-check-label` - Etiqueta asociada al checkbox/radio

### Formulario Horizontal

```html
<form>
    <div class="row mb-3">
        <label for="email" class="col-sm-2 col-form-label">Email</label>
        <div class="col-sm-10">
            <input type="email" class="form-control" id="email">
        </div>
    </div>
    
    <div class="row mb-3">
        <label for="password" class="col-sm-2 col-form-label">Password</label>
        <div class="col-sm-10">
            <input type="password" class="form-control" id="password">
        </div>
    </div>
    
    <button type="submit" class="btn btn-primary">Entrar</button>
</form>
```

**Explicación línea por línea:**
- `.row` - Fila del grid system
- `.col-sm-2` - Label ocupa 2 columnas en pantallas small+
- `.col-form-label` - Alinea verticalmente el label con el input
- `.col-sm-10` - Input ocupa 10 columnas (2+10=12 total)
- Crea un formulario donde labels e inputs están en la misma línea

---

## 9. Alertas

```html
<!-- Alertas básicas -->
<div class="alert alert-primary" role="alert">
    Esta es una alerta primaria
</div>

<div class="alert alert-success" role="alert">
    ¡Operación exitosa!
</div>

<div class="alert alert-danger" role="alert">
    ¡Error! Algo salió mal.
</div>

<div class="alert alert-warning" role="alert">
    Advertencia: Revisa esta información.
</div>

<!-- Alerta con encabezado -->
<div class="alert alert-success" role="alert">
    <h4 class="alert-heading">¡Bien hecho!</h4>
    <p>Has completado el registro exitosamente.</p>
    <hr>
    <p class="mb-0">Ahora puedes acceder a todas las funciones.</p>
</div>

<!-- Alerta dismissible (que se puede cerrar) -->
<div class="alert alert-warning alert-dismissible fade show" role="alert">
    Esta alerta se puede cerrar.
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

**Explicación línea por línea:**
- `.alert` - Clase base para alertas
- `.alert-primary/success/danger/warning` - Color de la alerta
- `role="alert"` - Atributo de accesibilidad para lectores de pantalla
- `.alert-heading` - Estilo especial para encabezados dentro de alertas
- `<hr>` - Línea horizontal separadora
- `.mb-0` - Sin margen inferior
- `.alert-dismissible` - Permite cerrar la alerta
- `.fade show` - Animación de desvanecimiento al cerrar
- `.btn-close` - Botón X para cerrar
- `data-bs-dismiss="alert"` - Conecta el botón con la funcionalidad de cerrar

---

## 10. Modales (Ventanas Emergentes)

```html
<!-- Botón que abre el modal -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" 
        data-bs-target="#miModal">
    Abrir Modal
</button>

<!-- El Modal -->
<div class="modal fade" id="miModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Título del Modal</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Contenido del modal aquí...</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                    Cerrar
                </button>
                <button type="button" class="btn btn-primary">
                    Guardar Cambios
                </button>
            </div>
        </div>
    </div>
</div>
```

**Explicación línea por línea:**
- `data-bs-toggle="modal"` - Indica que el botón abre un modal
- `data-bs-target="#miModal"` - ID del modal que se abrirá
- `.modal` - Contenedor principal del modal
- `.fade` - Animación de desvanecimiento al abrir/cerrar
- `tabindex="-1"` - Manejo de teclado para accesibilidad
- `.modal-dialog` - Contenedor del diálogo (controla ancho)
- `.modal-content` - Contenido visible del modal (fondo blanco, bordes)
- `.modal-header` - Sección superior con título
- `.modal-title` - Título estilizado
- `.btn-close` - Botón X para cerrar
- `data-bs-dismiss="modal"` - Cierra el modal al hacer clic
- `.modal-body` - Contenido principal del modal
- `.modal-footer` - Pie con botones de acción

### Modal Grande

```html
<!-- Modal extra grande -->
<div class="modal-dialog modal-xl">
    <!-- contenido... -->
</div>

<!-- Modal grande -->
<div class="modal-dialog modal-lg">
    <!-- contenido... -->
</div>

<!-- Modal pequeño -->
<div class="modal-dialog modal-sm">
    <!-- contenido... -->
</div>
```

**Explicación:**
- `.modal-xl` - Modal extra grande (1140px)
- `.modal-lg` - Modal grande (800px)
- Sin clase adicional - Modal normal (500px)
- `.modal-sm` - Modal pequeño (300px)

---

## 11. Badges (Insignias)

```html
<h1>Título <span class="badge bg-secondary">Nuevo</span></h1>

<button class="btn btn-primary">
    Mensajes <span class="badge bg-danger">4</span>
</button>

<!-- Badges con diferentes colores -->
<span class="badge bg-primary">Primario</span>
<span class="badge bg-success">Éxito</span>
<span class="badge bg-danger">Peligro</span>
<span class="badge bg-warning text-dark">Advertencia</span>

<!-- Badge en forma de píldora -->
<span class="badge rounded-pill bg-primary">Píldora</span>
```

**Explicación línea por línea:**
- `.badge` - Clase base para insignias pequeñas
- `.bg-secondary` - Color de fondo gris
- `.bg-danger` - Color de fondo rojo (para notificaciones)
- `.text-dark` - Texto oscuro (necesario en fondos claros como warning)
- `.rounded-pill` - Bordes completamente redondeados (forma de cápsula)
- Los badges se adaptan al tamaño de la fuente del elemento padre

---

## 12. Spacing (Espaciado)

Bootstrap usa un sistema de espaciado basado en márgenes y paddings.

```html
<!-- Margin (m) -->
<div class="m-3">Margen en todos los lados</div>
<div class="mt-3">Margen superior (top)</div>
<div class="mb-3">Margen inferior (bottom)</div>
<div class="ms-3">Margen izquierdo (start)</div>
<div class="me-3">Margen derecho (end)</div>
<div class="mx-3">Margen horizontal (left + right)</div>
<div class="my-3">Margen vertical (top + bottom)</div>

<!-- Padding (p) -->
<div class="p-3">Padding en todos los lados</div>
<div class="pt-3">Padding superior</div>
<div class="pb-3">Padding inferior</div>
<div class="ps-3">Padding izquierdo</div>
<div class="pe-3">Padding derecho</div>
<div class="px-3">Padding horizontal</div>
<div class="py-3">Padding vertical</div>

<!-- Sin espaciado -->
<div class="m-0">Sin margen</div>
<div class="p-0">Sin padding</div>

<!-- Auto (para centrar) -->
<div class="mx-auto" style="width: 200px;">Centrado horizontalmente</div>
```

**Explicación del sistema:**
- `m` = margin, `p` = padding
- `t` = top, `b` = bottom, `s` = start (left), `e` = end (right)
- `x` = horizontal, `y` = vertical
- Números del 0 al 5:
  - `0` = 0px
  - `1` = 0.25rem (4px)
  - `2` = 0.5rem (8px)
  - `3` = 1rem (16px)
  - `4` = 1.5rem (24px)
  - `5` = 3rem (48px)
- `auto` - Valor automático (útil para centrar)

---

## 13. Utilidades de Display

```html
<!-- Display block, inline, inline-block -->
<div class="d-block">Display block</div>
<div class="d-inline">Display inline</div>
<div class="d-inline-block">Display inline-block</div>

<!-- Ocultar elementos -->
<div class="d-none">Oculto en todas las pantallas</div>
<div class="d-sm-none">Oculto solo en móviles pequeños</div>
<div class="d-md-block d-none">Visible solo en tablets y superiores</div>

<!-- Flexbox -->
<div class="d-flex">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>

<!-- Flex con justificación -->
<div class="d-flex justify-content-center">Centrado</div>
<div class="d-flex justify-content-between">Espacio entre elementos</div>
<div class="d-flex justify-content-around">Espacio alrededor</div>

<!-- Flex con alineación -->
<div class="d-flex align-items-center" style="height: 200px;">
    Centrado verticalmente
</div>

<!-- Dirección del flex -->
<div class="d-flex flex-column">Items en columna (vertical)</div>
<div class="d-flex flex-row">Items en fila (horizontal)</div>
```

**Explicación línea por línea:**
- `.d-block` - Display block (elemento ocupa todo el ancho)
- `.d-inline` - Display inline (elemento solo ocupa su contenido)
- `.d-inline-block` - Híbrido (inline pero con dimensiones de block)
- `.d-none` - Display none (elemento completamente oculto)
- `.d-sm-none` - Oculto solo en pantallas small (≥576px)
- `.d-md-block` - Visible como block en medium (≥768px)
- `.d-flex` - Activa Flexbox
- `.justify-content-center` - Centra horizontalmente
- `.justify-content-between` - Espacio entre items, sin espacio en bordes
- `.justify-content-around` - Espacio uniforme alrededor de cada item
- `.align-items-center` - Centra verticalmente
- `.flex-column` - Items apilados verticalmente
- `.flex-row` - Items en fila horizontal (default)

---

## 14. Imágenes Responsive

```html
<!-- Imagen responsive (se adapta al contenedor) -->
<img src="imagen.jpg" class="img-fluid" alt="Descripción">

<!-- Imagen con bordes redondeados -->
<img src="imagen.jpg" class="rounded" alt="Descripción">

<!-- Imagen circular -->
<img src="avatar.jpg" class="rounded-circle" alt="Avatar">

<!-- Imagen tipo thumbnail -->
<img src="imagen.jpg" class="img-thumbnail" alt="Miniatura">

<!-- Figura con caption -->
<figure class="figure">
    <img src="imagen.jpg" class="figure-img img-fluid rounded" alt="...">
    <figcaption class="figure-caption">Descripción de la imagen</figcaption>
</figure>
```

**Explicación línea por línea:**
- `.img-fluid` - Hace la imagen responsive (max-width: 100%, height: auto)
- `.rounded` - Bordes redondeados pequeños
- `.rounded-circle` - Imagen completamente circular (requiere imagen cuadrada)
- `.img-thumbnail` - Borde de 1px y padding (estilo miniatura)
- `.figure` - Contenedor semántico para imagen con descripción
- `.figure-img` - Estilo para la imagen dentro de figure
- `.figure-caption` - Estilo para el texto descriptivo

---

## 15. Tablas

```html
<table class="table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Email</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>Juan Pérez</td>
            <td>juan@ejemplo.com</td>
        </tr>
        <tr>
            <td>2</td>
            <td>María García</td>
            <td>maria@ejemplo.com</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Carlos López</td>
            <td>carlos@ejemplo.com</td>
        </tr>
    </tbody>
</table>
```

**Explicación línea por línea:**
- `.table` - Clase base que aplica estilos básicos a la tabla
- `<thead>` - Encabezado de la tabla con fondo gris claro
- `<th>` - Celdas de encabezado (en negrita por defecto)
- `<tbody>` - Cuerpo de la tabla con las filas de datos
- `<tr>` - Table row (fila)
- `<td>` - Table data (celda de datos)

### Tabla con Variaciones

```html
<!-- Tabla con rayas (striped) -->
<table class="table table-striped">
    <!-- contenido... -->
</table>

<!-- Tabla con hover -->
<table class="table table-hover">
    <!-- contenido... -->
</table>

<!-- Tabla con bordes -->
<table class="table table-bordered">
    <!-- contenido... -->
</table>

<!-- Tabla oscura -->
<table class="table table-dark">
    <!-- contenido... -->
</table>

<!-- Tabla pequeña (más compacta) -->
<table class="table table-sm">
    <!-- contenido... -->
</table>

<!-- Tabla responsive (scroll horizontal en móviles) -->
<div class="table-responsive">
    <table class="table">
        <!-- contenido... -->
    </table>
</div>
```

**Explicación línea por línea:**
- `.table-striped` - Alterna colores de fondo en las filas (cebra)
- `.table-hover` - Resalta la fila al pasar el mouse
- `.table-bordered` - Añade bordes a todas las celdas
- `.table-dark` - Tema oscuro para la tabla
- `.table-sm` - Reduce el padding para tabla más compacta
- `.table-responsive` - Contenedor que permite scroll horizontal en pantallas pequeñas
- Puedes combinar clases: `table table-striped table-hover`

### Filas con Colores

```html
<table class="table">
    <tbody>
        <tr class="table-primary">
            <td>Fila primaria</td>
        </tr>
        <tr class="table-success">
            <td>Fila de éxito</td>
        </tr>
        <tr class="table-danger">
            <td>Fila de peligro</td>
        </tr>
        <tr class="table-warning">
            <td>Fila de advertencia</td>
        </tr>
        <tr class="table-info">
            <td>Fila de información</td>
        </tr>
    </tbody>
</table>
```

**Explicación:**
- `.table-primary/success/danger/warning/info` - Colorea la fila completa
- Útil para destacar estados o categorías
- También se puede aplicar a celdas individuales `<td>`

---

## 16. Tooltips y Popovers

### Tooltips

```html
<!-- Tooltip básico -->
<button type="button" class="btn btn-secondary" 
        data-bs-toggle="tooltip" 
        data-bs-placement="top"
        title="Este es un tooltip">
    Hover sobre mí
</button>

<!-- Diferentes posiciones -->
<button data-bs-toggle="tooltip" data-bs-placement="top" title="Tooltip arriba">
    Arriba
</button>
<button data-bs-toggle="tooltip" data-bs-placement="right" title="Tooltip derecha">
    Derecha
</button>
<button data-bs-toggle="tooltip" data-bs-placement="bottom" title="Tooltip abajo">
    Abajo
</button>
<button data-bs-toggle="tooltip" data-bs-placement="left" title="Tooltip izquierda">
    Izquierda
</button>

<!-- JavaScript necesario para inicializar tooltips -->
<script>
// Inicializar todos los tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})
</script>
```

**Explicación línea por línea:**
- `data-bs-toggle="tooltip"` - Activa el tooltip en el elemento
- `data-bs-placement="top"` - Posición: top, right, bottom, left
- `title="..."` - El texto que se mostrará en el tooltip
- Los tooltips requieren inicialización con JavaScript
- `document.querySelectorAll(...)` - Selecciona todos los elementos con tooltips
- `new bootstrap.Tooltip(...)` - Crea instancia de tooltip para cada elemento

### Popovers

```html
<!-- Popover básico -->
<button type="button" class="btn btn-lg btn-danger" 
        data-bs-toggle="popover" 
        data-bs-title="Título del Popover"
        data-bs-content="Contenido más largo del popover aquí...">
    Click para popover
</button>

<!-- JavaScript necesario -->
<script>
// Inicializar todos los popovers
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
})
</script>
```

**Explicación línea por línea:**
- `data-bs-toggle="popover"` - Activa el popover
- `data-bs-title="..."` - Título del popover
- `data-bs-content="..."` - Contenido del popover (puede ser largo)
- Similar a tooltip pero con más contenido y un título
- También requiere inicialización con JavaScript
- Los popovers se muestran al hacer clic (tooltips al hover)

---

## 17. Acordeón (Collapse)

```html
<div class="accordion" id="miAcordeon">
    <!-- Item 1 -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="heading1">
            <button class="accordion-button" type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#collapse1">
                Sección 1
            </button>
        </h2>
        <div id="collapse1" class="accordion-collapse collapse show" 
             data-bs-parent="#miAcordeon">
            <div class="accordion-body">
                Contenido de la primera sección del acordeón.
            </div>
        </div>
    </div>
    
    <!-- Item 2 -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="heading2">
            <button class="accordion-button collapsed" type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#collapse2">
                Sección 2
            </button>
        </h2>
        <div id="collapse2" class="accordion-collapse collapse" 
             data-bs-parent="#miAcordeon">
            <div class="accordion-body">
                Contenido de la segunda sección del acordeón.
            </div>
        </div>
    </div>
    
    <!-- Item 3 -->
    <div class="accordion-item">
        <h2 class="accordion-header" id="heading3">
            <button class="accordion-button collapsed" type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#collapse3">
                Sección 3
            </button>
        </h2>
        <div id="collapse3" class="accordion-collapse collapse" 
             data-bs-parent="#miAcordeon">
            <div class="accordion-body">
                Contenido de la tercera sección del acordeón.
            </div>
        </div>
    </div>
</div>
```

**Explicación línea por línea:**
- `.accordion` - Contenedor principal del acordeón
- `id="miAcordeon"` - ID único para el acordeón
- `.accordion-item` - Cada sección del acordeón
- `.accordion-header` - Encabezado clickeable
- `.accordion-button` - Botón que expande/contrae
- `data-bs-toggle="collapse"` - Activa funcionalidad de colapsar
- `data-bs-target="#collapse1"` - ID del contenido a mostrar/ocultar
- `.accordion-collapse collapse` - Contenedor del contenido colapsable
- `.show` - Clase para mostrar por defecto (solo en el primer item)
- `data-bs-parent="#miAcordeon"` - Cierra otros items al abrir uno nuevo
- `.accordion-body` - Contenido con padding apropiado
- `.collapsed` - Estado inicial cerrado (en items 2 y 3)

---

## 18. Carousel (Carrusel de Imágenes)

```html
<div id="miCarousel" class="carousel slide" data-bs-ride="carousel">
    <!-- Indicadores -->
    <div class="carousel-indicators">
        <button type="button" data-bs-target="#miCarousel" data-bs-slide-to="0" class="active"></button>
        <button type="button" data-bs-target="#miCarousel" data-bs-slide-to="1"></button>
        <button type="button" data-bs-target="#miCarousel" data-bs-slide-to="2"></button>
    </div>
    
    <!-- Slides -->
    <div class="carousel-inner">
        <div class="carousel-item active">
            <img src="imagen1.jpg" class="d-block w-100" alt="Slide 1">
            <div class="carousel-caption d-none d-md-block">
                <h5>Primera Imagen</h5>
                <p>Descripción de la primera imagen.</p>
            </div>
        </div>
        <div class="carousel-item">
            <img src="imagen2.jpg" class="d-block w-100" alt="Slide 2">
            <div class="carousel-caption d-none d-md-block">
                <h5>Segunda Imagen</h5>
                <p>Descripción de la segunda imagen.</p>
            </div>
        </div>
        <div class="carousel-item">
            <img src="imagen3.jpg" class="d-block w-100" alt="Slide 3">
            <div class="carousel-caption d-none d-md-block">
                <h5>Tercera Imagen</h5>
                <p>Descripción de la tercera imagen.</p>
            </div>
        </div>
    </div>
    
    <!-- Controles -->
    <button class="carousel-control-prev" type="button" data-bs-target="#miCarousel" data-bs-slide="prev">
        <span class="carousel-control-prev-icon"></span>
        <span class="visually-hidden">Anterior</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#miCarousel" data-bs-slide="next">
        <span class="carousel-control-next-icon"></span>
        <span class="visually-hidden">Siguiente</span>
    </button>
</div>
```

**Explicación línea por línea:**
- `.carousel slide` - Contenedor principal con animación de deslizamiento
- `data-bs-ride="carousel"` - Inicia el carousel automáticamente
- `.carousel-indicators` - Puntos indicadores en la parte inferior
- `data-bs-slide-to="0"` - Indica a qué slide ir (índice basado en 0)
- `.active` - Marca el slide o indicador activo
- `.carousel-inner` - Contenedor de todos los slides
- `.carousel-item` - Cada slide individual
- `.d-block w-100` - Display block y ancho 100% para la imagen
- `.carousel-caption` - Texto sobre la imagen
- `.d-none d-md-block` - Oculto en móviles, visible en tablets+
- `.carousel-control-prev` - Botón para ir al slide anterior
- `.carousel-control-next` - Botón para ir al slide siguiente
- `data-bs-slide="prev/next"` - Dirección del movimiento
- `.visually-hidden` - Oculto visualmente pero accesible para lectores de pantalla

---

## 19. Breadcrumb (Migas de Pan)

```html
<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="#">Inicio</a></li>
        <li class="breadcrumb-item"><a href="#">Productos</a></li>
        <li class="breadcrumb-item active" aria-current="page">Laptops</li>
    </ol>
</nav>
```

**Explicación línea por línea:**
- `<nav aria-label="breadcrumb">` - Elemento de navegación semántico
- `.breadcrumb` - Lista ordenada con estilo de breadcrumb
- `.breadcrumb-item` - Cada elemento del camino
- `<a href="#">` - Enlaces a páginas anteriores
- `.active` - Página actual (sin enlace)
- `aria-current="page"` - Indica la página actual para accesibilidad
- Automáticamente añade separadores "/" entre items

---

## 20. Pagination (Paginación)

```html
<nav>
    <ul class="pagination">
        <li class="page-item disabled">
            <a class="page-link" href="#" tabindex="-1">Anterior</a>
        </li>
        <li class="page-item"><a class="page-link" href="#">1</a></li>
        <li class="page-item active"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item"><a class="page-link" href="#">4</a></li>
        <li class="page-item"><a class="page-link" href="#">5</a></li>
        <li class="page-item">
            <a class="page-link" href="#">Siguiente</a>
        </li>
    </ul>
</nav>

<!-- Paginación con iconos -->
<nav>
    <ul class="pagination">
        <li class="page-item">
            <a class="page-link" href="#">«</a>
        </li>
        <li class="page-item"><a class="page-link" href="#">1</a></li>
        <li class="page-item"><a class="page-link" href="#">2</a></li>
        <li class="page-item"><a class="page-link" href="#">3</a></li>
        <li class="page-item">
            <a class="page-link" href="#">»</a>
        </li>
    </ul>
</nav>

<!-- Tamaños -->
<ul class="pagination pagination-lg"><!-- Grande --></ul>
<ul class="pagination"><!-- Normal --></ul>
<ul class="pagination pagination-sm"><!-- Pequeña --></ul>
```

**Explicación línea por línea:**
- `.pagination` - Lista sin estilo que crea la paginación
- `.page-item` - Cada elemento de la paginación
- `.page-link` - El enlace dentro del item
- `.disabled` - Item deshabilitado (gris y sin clic)
- `tabindex="-1"` - No se puede acceder con teclado
- `.active` - Página actual (resaltada)
- `«` y `»` - Entidades HTML para flechas
- `.pagination-lg` - Paginación grande
- `.pagination-sm` - Paginación pequeña

---

## 21. Progress Bars (Barras de Progreso)

```html
<!-- Barra de progreso básica -->
<div class="progress">
    <div class="progress-bar" style="width: 25%"></div>
</div>

<!-- Con etiqueta -->
<div class="progress">
    <div class="progress-bar" style="width: 50%">50%</div>
</div>

<!-- Con colores -->
<div class="progress">
    <div class="progress-bar bg-success" style="width: 25%"></div>
</div>

<div class="progress">
    <div class="progress-bar bg-info" style="width: 50%"></div>
</div>

<div class="progress">
    <div class="progress-bar bg-warning" style="width: 75%"></div>
</div>

<div class="progress">
    <div class="progress-bar bg-danger" style="width: 100%"></div>
</div>

<!-- Barra rayada -->
<div class="progress">
    <div class="progress-bar progress-bar-striped" style="width: 40%"></div>
</div>

<!-- Barra rayada animada -->
<div class="progress">
    <div class="progress-bar progress-bar-striped progress-bar-animated" 
         style="width: 75%"></div>
</div>

<!-- Múltiples barras -->
<div class="progress">
    <div class="progress-bar bg-success" style="width: 15%"></div>
    <div class="progress-bar bg-warning" style="width: 30%"></div>
    <div class="progress-bar bg-danger" style="width: 20%"></div>
</div>

<!-- Diferentes alturas -->
<div class="progress" style="height: 5px;">
    <div class="progress-bar" style="width: 25%"></div>
</div>

<div class="progress" style="height: 30px;">
    <div class="progress-bar" style="width: 50%">50%</div>
</div>
```

**Explicación línea por línea:**
- `.progress` - Contenedor de la barra (fondo gris claro)
- `.progress-bar` - La barra que indica el progreso
- `style="width: 25%"` - Controla el porcentaje de progreso
- Texto dentro de progress-bar muestra el porcentaje
- `.bg-success/info/warning/danger` - Colores de la barra
- `.progress-bar-striped` - Añade patrón de rayas diagonales
- `.progress-bar-animated` - Anima las rayas (movimiento continuo)
- Múltiples `.progress-bar` en un `.progress` crea segmentos
- `style="height: ..."` en `.progress` cambia la altura

---

## 22. Spinners (Indicadores de Carga)

```html
<!-- Spinner circular -->
<div class="spinner-border" role="status">
    <span class="visually-hidden">Cargando...</span>
</div>

<!-- Spinner con colores -->
<div class="spinner-border text-primary"></div>
<div class="spinner-border text-success"></div>
<div class="spinner-border text-danger"></div>
<div class="spinner-border text-warning"></div>
<div class="spinner-border text-info"></div>

<!-- Spinner pequeño -->
<div class="spinner-border spinner-border-sm"></div>

<!-- Spinner creciente -->
<div class="spinner-grow" role="status">
    <span class="visually-hidden">Cargando...</span>
</div>

<!-- Spinner creciente con colores -->
<div class="spinner-grow text-primary"></div>
<div class="spinner-grow text-success"></div>

<!-- Spinner en botón -->
<button class="btn btn-primary" type="button" disabled>
    <span class="spinner-border spinner-border-sm"></span>
    Cargando...
</button>

<button class="btn btn-primary" type="button" disabled>
    <span class="spinner-grow spinner-grow-sm"></span>
    Cargando...
</button>

<!-- Spinners centrados -->
<div class="d-flex justify-content-center">
    <div class="spinner-border"></div>
</div>
```

**Explicación línea por línea:**
- `.spinner-border` - Spinner circular con borde giratorio
- `role="status"` - Atributo de accesibilidad
- `.visually-hidden` - Texto oculto para lectores de pantalla
- `.text-primary/success/danger` - Color del spinner
- `.spinner-border-sm` - Versión pequeña del spinner
- `.spinner-grow` - Spinner que crece y se encoge (pulsante)
- `.spinner-grow-sm` - Versión pequeña del spinner creciente
- `disabled` en botón - Deshabilita el botón durante carga
- `.d-flex justify-content-center` - Centra el spinner

---

## 23. Offcanvas (Panel Lateral)

```html
<!-- Botón que abre el offcanvas -->
<button class="btn btn-primary" type="button" 
        data-bs-toggle="offcanvas" 
        data-bs-target="#offcanvasEjemplo">
    Abrir menú lateral
</button>

<!-- Offcanvas -->
<div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasEjemplo">
    <div class="offcanvas-header">
        <h5 class="offcanvas-title">Menú</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
    </div>
    <div class="offcanvas-body">
        <p>Contenido del panel lateral aquí...</p>
        <ul class="list-unstyled">
            <li><a href="#">Enlace 1</a></li>
            <li><a href="#">Enlace 2</a></li>
            <li><a href="#">Enlace 3</a></li>
        </ul>
    </div>
</div>

<!-- Diferentes posiciones -->
<!-- Izquierda -->
<div class="offcanvas offcanvas-start">...</div>

<!-- Derecha -->
<div class="offcanvas offcanvas-end">...</div>

<!-- Arriba -->
<div class="offcanvas offcanvas-top">...</div>

<!-- Abajo -->
<div class="offcanvas offcanvas-bottom">...</div>
```

**Explicación línea por línea:**
- `data-bs-toggle="offcanvas"` - Activa el offcanvas
- `data-bs-target="#offcanvasEjemplo"` - ID del offcanvas a abrir
- `.offcanvas` - Clase base del panel lateral
- `.offcanvas-start` - Panel desliza desde la izquierda
- `.offcanvas-end` - Panel desliza desde la derecha
- `.offcanvas-top` - Panel desliza desde arriba
- `.offcanvas-bottom` - Panel desliza desde abajo
- `.offcanvas-header` - Encabezado con título y botón cerrar
- `.offcanvas-title` - Título del panel
- `.btn-close` - Botón X para cerrar
- `data-bs-dismiss="offcanvas"` - Cierra el offcanvas
- `.offcanvas-body` - Contenido scrolleable del panel

---

## 24. Toasts (Notificaciones)

```html
<!-- Toast básico -->
<div class="toast" role="alert">
    <div class="toast-header">
        <strong class="me-auto">Notificación</strong>
        <small>Hace 5 min</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
    </div>
    <div class="toast-body">
        Este es el mensaje de la notificación.
    </div>
</div>

<!-- Toast con color -->
<div class="toast align-items-center text-bg-primary border-0" role="alert">
    <div class="d-flex">
        <div class="toast-body">
            Notificación con fondo de color.
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                data-bs-dismiss="toast"></button>
    </div>
</div>

<!-- Contenedor para posicionar toasts -->
<div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div class="toast" role="alert">
        <div class="toast-header">
            <strong class="me-auto">Bootstrap</strong>
            <small>justo ahora</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            ¡Operación completada con éxito!
        </div>
    </div>
</div>

<!-- JavaScript para mostrar toast -->
<script>
var toastElList = [].slice.call(document.querySelectorAll('.toast'))
var toastList = toastElList.map(function(toastEl) {
    return new bootstrap.Toast(toastEl)
})

// Mostrar el primer toast
toastList[0].show()
</script>
```

**Explicación línea por línea:**
- `.toast` - Contenedor principal de la notificación
- `role="alert"` - Indica que es una alerta para accesibilidad
- `.toast-header` - Encabezado con título, tiempo y botón cerrar
- `.me-auto` - Margin-end auto (empuja elementos a la derecha)
- `.toast-body` - Contenido del mensaje
- `.text-bg-primary` - Texto blanco sobre fondo azul
- `.border-0` - Sin bordes
- `.align-items-center` - Centra verticalmente
- `.toast-container` - Contenedor para agrupar múltiples toasts
- `.position-fixed` - Posición fija en la ventana
- `.bottom-0 end-0` - Esquina inferior derecha
- `.p-3` - Padding de tamaño 3
- `new bootstrap.Toast(toastEl)` - Crea instancia del toast
- `.show()` - Muestra el toast

---

## 25. List Groups (Grupos de Listas)

```html
<!-- Lista básica -->
<ul class="list-group">
    <li class="list-group-item">Un elemento</li>
    <li class="list-group-item">Segundo elemento</li>
    <li class="list-group-item">Tercer elemento</li>
    <li class="list-group-item">Cuarto elemento</li>
</ul>

<!-- Lista con elemento activo -->
<ul class="list-group">
    <li class="list-group-item active">Elemento activo</li>
    <li class="list-group-item">Segundo elemento</li>
    <li class="list-group-item">Tercer elemento</li>
</ul>

<!-- Lista con elemento deshabilitado -->
<ul class="list-group">
    <li class="list-group-item disabled">Elemento deshabilitado</li>
    <li class="list-group-item">Segundo elemento</li>
    <li class="list-group-item">Tercer elemento</li>
</ul>

<!-- Lista con enlaces -->
<div class="list-group">
    <a href="#" class="list-group-item list-group-item-action active">
        Enlace activo
    </a>
    <a href="#" class="list-group-item list-group-item-action">Segundo enlace</a>
    <a href="#" class="list-group-item list-group-item-action">Tercer enlace</a>
</div>

<!-- Lista con colores -->
<ul class="list-group">
    <li class="list-group-item list-group-item-primary">Primario</li>
    <li class="list-group-item list-group-item-success">Éxito</li>
    <li class="list-group-item list-group-item-danger">Peligro</li>
    <li class="list-group-item list-group-item-warning">Advertencia</li>
    <li class="list-group-item list-group-item-info">Información</li>
</ul>

<!-- Lista con badges -->
<ul class="list-group">
    <li class="list-group-item d-flex justify-content-between align-items-center">
        Mensajes
        <span class="badge bg-primary rounded-pill">14</span>
    </li>
    <li class="list-group-item d-flex justify-content-between align-items-center">
        Notificaciones
        <span class="badge bg-danger rounded-pill">2</span>
    </li>
</ul>

<!-- Lista sin bordes (flush) -->
<ul class="list-group list-group-flush">
    <li class="list-group-item">Elemento sin bordes laterales</li>
    <li class="list-group-item">Segundo elemento</li>
    <li class="list-group-item">Tercer elemento</li>
</ul>

<!-- Lista numerada -->
<ol class="list-group list-group-numbered">
    <li class="list-group-item">Primer elemento</li>
    <li class="list-group-item">Segundo elemento</li>
    <li class="list-group-item">Tercer elemento</li>
</ol>

<!-- Lista horizontal -->
<ul class="list-group list-group-horizontal">
    <li class="list-group-item">Item 1</li>
    <li class="list-group-item">Item 2</li>
    <li class="list-group-item">Item 3</li>
</ul>
```

**Explicación línea por línea:**
- `.list-group` - Contenedor de la lista con bordes y esquinas redondeadas
- `.list-group-item` - Cada elemento de la lista
- `.active` - Resalta el elemento activo
- `.disabled` - Elemento deshabilitado (gris y sin hover)
- `.list-group-item-action` - Añade hover y cursor pointer (para enlaces)
- `.list-group-item-primary/success/danger` - Colores de fondo
- `.d-flex justify-content-between` - Flexbox para alinear badge a la derecha
- `.align-items-center` - Centra verticalmente
- `.list-group-flush` - Remueve bordes laterales (para usar dentro de cards)
- `.list-group-numbered` - Añade numeración automática
- `.list-group-horizontal` - Lista en fila horizontal en lugar de vertical

---

## 26. Dropdown (Menús Desplegables)

```html
<!-- Dropdown básico -->
<div class="dropdown">
    <button class="btn btn-secondary dropdown-toggle" type="button" 
            data-bs-toggle="dropdown">
        Dropdown button
    </button>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#">Acción</a></li>
        <li><a class="dropdown-item" href="#">Otra acción</a></li>
        <li><a class="dropdown-item" href="#">Algo más aquí</a></li>
    </ul>
</div>

<!-- Dropdown con separadores -->
<div class="dropdown">
    <button class="btn btn-primary dropdown-toggle" type="button" 
            data-bs-toggle="dropdown">
        Opciones
    </button>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#">Acción</a></li>
        <li><a class="dropdown-item" href="#">Otra acción</a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="#">Separado por línea</a></li>
    </ul>
</div>

<!-- Dropdown con headers -->
<div class="dropdown">
    <button class="btn btn-info dropdown-toggle" type="button" 
            data-bs-toggle="dropdown">
        Menú
    </button>
    <ul class="dropdown-menu">
        <li><h6 class="dropdown-header">Encabezado del menú</h6></li>
        <li><a class="dropdown-item" href="#">Acción</a></li>
        <li><a class="dropdown-item" href="#">Otra acción</a></li>
        <li><hr class="dropdown-divider"></li>
        <li><h6 class="dropdown-header">Otra sección</h6></li>
        <li><a class="dropdown-item" href="#">Algo más</a></li>
    </ul>
</div>

<!-- Dropdown con items deshabilitados -->
<div class="dropdown">
    <button class="btn btn-secondary dropdown-toggle" type="button" 
            data-bs-toggle="dropdown">
        Dropdown
    </button>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#">Elemento activo</a></li>
        <li><a class="dropdown-item disabled" href="#">Elemento deshabilitado</a></li>
        <li><a class="dropdown-item" href="#">Elemento normal</a></li>
    </ul>
</div>

<!-- Dropup (hacia arriba) -->
<div class="dropup">
    <button class="btn btn-secondary dropdown-toggle" type="button" 
            data-bs-toggle="dropdown">
        Dropup
    </button>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#">Acción</a></li>
        <li><a class="dropdown-item" href="#">Otra acción</a></li>
    </ul>
</div>

<!-- Dropend (hacia la derecha) -->
<div class="dropend">
    <button class="btn btn-secondary dropdown-toggle" type="button" 
            data-bs-toggle="dropdown">
        Dropend
    </button>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#">Acción</a></li>
        <li><a class="dropdown-item" href="#">Otra acción</a></li>
    </ul>
</div>

<!-- Dropstart (hacia la izquierda) -->
<div class="dropstart">
    <button class="btn btn-secondary dropdown-toggle" type="button" 
            data-bs-toggle="dropdown">
        Dropstart
    </button>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#">Acción</a></li>
        <li><a class="dropdown-item" href="#">Otra acción</a></li>
    </ul>
</div>
```

**Explicación línea por línea:**
- `.dropdown` - Contenedor del dropdown (se abre hacia abajo)
- `.dropdown-toggle` - Botón que abre/cierra el menú (añade flecha)
- `data-bs-toggle="dropdown"` - Activa la funcionalidad dropdown
- `.dropdown-menu` - El menú que se despliega
- `.dropdown-item` - Cada opción del menú
- `.dropdown-divider` - Línea horizontal separadora
- `.dropdown-header` - Encabezado de sección (texto no clickeable)
- `.disabled` - Item deshabilitado (gris y sin clic)
- `.dropup` - Menú se abre hacia arriba
- `.dropend` - Menú se abre hacia la derecha
- `.dropstart` - Menú se abre hacia la izquierda

---

## 27. Tabs (Pestañas)

```html
<!-- Nav tabs -->
<ul class="nav nav-tabs" id="myTab" role="tablist">
    <li class="nav-item" role="presentation">
        <button class="nav-link active" id="home-tab" data-bs-toggle="tab" 
                data-bs-target="#home" type="button">
            Inicio
        </button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="profile-tab" data-bs-toggle="tab" 
                data-bs-target="#profile" type="button">
            Perfil
        </button>
    </li>
    <li class="nav-item" role="presentation">
        <button class="nav-link" id="contact-tab" data-bs-toggle="tab" 
                data-bs-target="#contact" type="button">
            Contacto
        </button>
    </li>
</ul>

<!-- Tab content -->
<div class="tab-content" id="myTabContent">
    <div class="tab-pane fade show active" id="home">
        <p>Contenido de la pestaña Inicio...</p>
    </div>
    <div class="tab-pane fade" id="profile">
        <p>Contenido de la pestaña Perfil...</p>
    </div>
    <div class="tab-pane fade" id="contact">
        <p>Contenido de la pestaña Contacto...</p>
    </div>
</div>
```

**Explicación línea por línea:**
- `.nav nav-tabs` - Estilo de pestañas con bordes
- `role="tablist"` - Atributo de accesibilidad
- `.nav-item` - Cada pestaña del menú
- `.nav-link` - Enlace/botón de la pestaña
- `.active` - Pestaña actualmente seleccionada
- `data-bs-toggle="tab"` - Activa funcionalidad de tabs
- `data-bs-target="#home"` - ID del contenido a mostrar
- `.tab-content` - Contenedor de todos los contenidos
- `.tab-pane` - Cada panel de contenido
- `.fade` - Animación de desvanecimiento al cambiar
- `.show` - Muestra el tab (combinado con active)

### Pills (Variante de Tabs)

```html
<!-- Nav pills -->
<ul class="nav nav-pills">
    <li class="nav-item">
        <a class="nav-link active" href="#">Activo</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">Enlace</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="#">Enlace</a>
    </li>
    <li class="nav-item">
        <a class="nav-link disabled">Deshabilitado</a>
    </li>
</ul>

<!-- Pills verticales -->
<div class="d-flex">
    <div class="nav flex-column nav-pills me-3" style="width: 200px;">
        <a class="nav-link active" href="#">Inicio</a>
        <a class="nav-link" href="#">Perfil</a>
        <a class="nav-link" href="#">Mensajes</a>
        <a class="nav-link" href="#">Configuración</a>
    </div>
    <div>
        Contenido aquí...
    </div>
</div>
```

**Explicación línea por línea:**
- `.nav-pills` - Estilo de botones redondeados (píldoras)
- `.flex-column` - Organiza pills verticalmente
- `.me-3` - Margin-end (derecha) de tamaño 3
- Funcionan igual que tabs pero con diferente apariencia

---

## 28. Shadows (Sombras)

```html
<!-- Diferentes tamaños de sombra -->
<div class="shadow-none p-3 mb-3 bg-light">Sin sombra</div>
<div class="shadow-sm p-3 mb-3 bg-white">Sombra pequeña</div>
<div class="shadow p-3 mb-3 bg-white">Sombra regular</div>
<div class="shadow-lg p-3 mb-3 bg-white">Sombra grande</div>
```

**Explicación línea por línea:**
- `.shadow-none` - Sin sombra
- `.shadow-sm` - Sombra pequeña y sutil
- `.shadow` - Sombra regular (default)
- `.shadow-lg` - Sombra grande y pronunciada
- Se usa con `.p-3` (padding) para que la sombra sea visible
- `.bg-white` o `.bg-light` - Fondo para contrastar la sombra

---

## 29. Borders (Bordes)

```html
<!-- Añadir bordes -->
<div class="border p-3">Borde en todos los lados</div>
<div class="border-top p-3">Solo borde superior</div>
<div class="border-end p-3">Solo borde derecho</div>
<div class="border-bottom p-3">Solo borde inferior</div>
<div class="border-start p-3">Solo borde izquierdo</div>

<!-- Colores de borde -->
<div class="border border-primary p-3">Borde azul</div>
<div class="border border-success p-3">Borde verde</div>
<div class="border border-danger p-3">Borde rojo</div>
<div class="border border-warning p-3">Borde amarillo</div>

<!-- Grosor del borde -->
<div class="border border-1 p-3">Borde delgado</div>
<div class="border border-2 p-3">Borde medio</div>
<div class="border border-3 p-3">Borde grueso</div>
<div class="border border-4 p-3">Borde muy grueso</div>
<div class="border border-5 p-3">Borde extra grueso</div>

<!-- Bordes redondeados -->
<div class="border rounded p-3">Bordes redondeados</div>
<div class="border rounded-top p-3">Redondeado arriba</div>
<div class="border rounded-end p-3">Redondeado derecha</div>
<div class="border rounded-bottom p-3">Redondeado abajo</div>
<div class="border rounded-start p-3">Redondeado izquierda</div>
<div class="border rounded-circle p-3">Completamente circular</div>
<div class="border rounded-pill p-3">Forma de píldora</div>

<!-- Tamaños de redondeo -->
<div class="border rounded-0 p-3">Sin redondeo</div>
<div class="border rounded-1 p-3">Redondeo pequeño</div>
<div class="border rounded-2 p-3">Redondeo medio</div>
<div class="border rounded-3 p-3">Redondeo grande</div>
```

**Explicación línea por línea:**
- `.border` - Añade borde de 1px en todos los lados
- `.border-top/end/bottom/start` - Borde en un lado específico
- `.border-primary/success/danger` - Color del borde
- `.border-1` a `.border-5` - Grosor del borde (1px a 5px)
- `.rounded` - Esquinas redondeadas (0.375rem)
- `.rounded-top/end/bottom/start` - Redondea solo un lado
- `.rounded-circle` - Completamente circular (50%)
- `.rounded-pill` - Forma de cápsula
- `.rounded-0` - Sin redondeo
- `.rounded-1` a `.rounded-3` - Diferentes radios de redondeo

---

## 30. Width y Height (Ancho y Altura)

```html
<!-- Ancho -->
<div class="w-25 p-3 bg-primary">Ancho 25%</div>
<div class="w-50 p-3 bg-primary">Ancho 50%</div>
<div class="w-75 p-3 bg-primary">Ancho 75%</div>
<div class="w-100 p-3 bg-primary">Ancho 100%</div>
<div class="w-auto p-3 bg-primary">Ancho automático</div>

<!-- Altura -->
<div style="height: 200px; border: 1px solid #dee2e6;">
    <div class="h-25 d-inline-block bg-primary" style="width: 120px;">Altura 25%</div>
    <div class="h-50 d-inline-block bg-primary" style="width: 120px;">Altura 50%</div>
    <div class="h-75 d-inline-block bg-primary" style="width: 120px;">Altura 75%</div>
    <div class="h-100 d-inline-block bg-primary" style="width: 120px;">Altura 100%</div>
</div>

<!-- Max width y max height -->
<div class="mw-100 p-3 bg-info">Max width 100%</div>
<div class="mh-100 p-3 bg-info" style="height: 200px;">Max height 100%</div>

<!-- Viewport width y height -->
<div class="vw-100 p-3 bg-warning">Ancho 100% del viewport</div>
<div class="vh-100 p-3 bg-warning">Altura 100% del viewport</div>
```

**Explicación línea por línea:**
- `.w-25/50/75/100` - Ancho relativo al contenedor padre (25%, 50%, 75%, 100%)
- `.w-auto` - Ancho automático basado en el contenido
- `.h-25/50/75/100` - Altura relativa al contenedor padre
- `.mw-100` - Max-width 100% (no excederá el ancho del padre)
- `.mh-100` - Max-height 100% (no excederá la altura del padre)
- `.vw-100` - Width 100% del viewport (ancho de la ventana)
- `.vh-100` - Height 100% del viewport (altura de la ventana)

---

## 31. Position (Posicionamiento)

```html
<!-- Position static (default) -->
<div class="position-static">Position static</div>

<!-- Position relative -->
<div class="position-relative" style="height: 200px;">
    Position relative
    <div class="position-absolute top-0 start-0 bg-primary text-white p-2">
        Esquina superior izquierda
    </div>
</div>

<!-- Position absolute -->
<div class="position-relative" style="height: 200px; border: 1px solid #dee2e6;">
    <div class="position-absolute top-0 end-0 bg-danger text-white p-2">
        Top-End
    </div>
    <div class="position-absolute bottom-0 end-0 bg-success text-white p-2">
        Bottom-End
    </div>
    <div class="position-absolute bottom-0 start-0 bg-warning p-2">
        Bottom-Start
    </div>
</div>

<!-- Position fixed -->
<div class="position-fixed bottom-0 end-0 m-3">
    <button class="btn btn-primary">Botón fijo</button>
</div>

<!-- Position sticky -->
<div class="position-sticky top-0 bg-info p-3">
    Este elemento se queda pegado al hacer scroll
</div>

<!-- Translate middle (centrar) -->
<div class="position-relative" style="height: 200px; border: 1px solid #dee2e6;">
    <div class="position-absolute top-50 start-50 translate-middle bg-primary text-white p-3">
        Centrado perfectamente
    </div>
</div>
```

**Explicación línea por línea:**
- `.position-static` - Posicionamiento normal (default)
- `.position-relative` - Relativo a su posición original
- `.position-absolute` - Absoluto respecto al padre position-relative
- `.position-fixed` - Fijo respecto al viewport
- `.position-sticky` - Se comporta como relative hasta cierto scroll, luego fixed
- `.top-0/50/100` - Distancia desde arriba
- `.bottom-0/50/100` - Distancia desde abajo
- `.start-0/50/100` - Distancia desde izquierda
- `.end-0/50/100` - Distancia desde derecha
- `.translate-middle` - Centra el elemento usando transform

---

## 32. Overflow

```html
<!-- Overflow auto -->
<div class="overflow-auto" style="max-width: 300px; max-height: 100px;">
    Este es un texto muy largo que necesitará scroll porque excede el tamaño del contenedor. 
    Más texto aquí para forzar el scroll vertical y horizontal si es necesario.
</div>

<!-- Overflow hidden -->
<div class="overflow-hidden" style="max-width: 300px; max-height: 100px;">
    Este texto se cortará y no se verá completo porque el overflow está oculto.
</div>

<!-- Overflow visible -->
<div class="overflow-visible" style="height: 100px;">
    Este contenido puede salirse del contenedor.
</div>

<!-- Overflow scroll -->
<div class="overflow-scroll" style="max-width: 300px; max-height: 100px;">
    Siempre muestra scrollbars, incluso si no son necesarias.
</div>

<!-- Overflow específico (x o y) -->
<div class="overflow-x-auto overflow-y-hidden" style="max-width: 300px;">
    Scroll horizontal permitido, vertical oculto.
</div>
```

**Explicación línea por línea:**
- `.overflow-auto` - Añade scroll solo si es necesario
- `.overflow-hidden` - Oculta contenido que se sale
- `.overflow-visible` - Permite que el contenido se salga (default)
- `.overflow-scroll` - Siempre muestra scrollbars
- `.overflow-x-auto` - Scroll horizontal automático
- `.overflow-y-auto` - Scroll vertical automático
- `.overflow-x-hidden` - Oculta desbordamiento horizontal
- `.overflow-y-hidden` - Oculta desbordamiento vertical

---

## 33. Visibility

```html
<!-- Visible -->
<div class="visible">Este elemento es visible</div>

<!-- Invisible (ocupa espacio pero no se ve) -->
<div class="invisible">Este elemento es invisible pero ocupa espacio</div>

<!-- Oculto completamente (no ocupa espacio) -->
<div class="d-none">Este elemento no se muestra ni ocupa espacio</div>
```

**Explicación línea por línea:**
- `.visible` - Elemento visible (comportamiento normal)
- `.invisible` - visibility: hidden (invisible pero ocupa espacio en el layout)
- `.d-none` - display: none (completamente removido del flujo del documento)

## 34. Z-Index (Orden de Apilamiento)

```html
<div class="position-relative" style="height: 150px;">
    <div class="position-absolute bg-primary text-white p-3 z-3">
        Z-index 3 (encima)
    </div>
    <div class="position-absolute bg-success text-white p-3 z-2" style="top: 20px; left: 20px;">
        Z-index 2 (medio)
    </div>
    <div class="position-absolute bg-danger text-white p-3 z-1" style="top: 40px; left: 40px;">
        Z-index 1 (abajo)
    </div>
</div>

<!-- Z-index negativo -->
<div class="position-relative">
    <div class="position-absolute z-n1 bg-warning p-3">
        Z-index negativo (detrás)
    </div>
    <div class="bg-white p-3">
        Contenido normal (delante)
    </div>
</div>
```

**Explicación línea por línea:**
- `.z-1` a `.z-3` - Z-index de 1 a 3 (números más altos aparecen encima)
- `.z-n1` - Z-index negativo (aparece detrás de elementos sin z-index)
- Los elementos con mayor z-index se superponen a los de menor z-index
- Solo funciona en elementos con position (relative, absolute, fixed, sticky)

---

## 35. Breakpoints Responsive

Bootstrap tiene 6 breakpoints responsive:

```html
<!-- Clases responsive con breakpoints -->
<div class="d-none d-sm-block">Visible desde SM (≥576px)</div>
<div class="d-none d-md-block">Visible desde MD (≥768px)</div>
<div class="d-none d-lg-block">Visible desde LG (≥992px)</div>
<div class="d-none d-xl-block">Visible desde XL (≥1200px)</div>
<div class="d-none d-xxl-block">Visible desde XXL (≥1400px)</div>

<!-- Ocultar en ciertos tamaños -->
<div class="d-block d-md-none">Solo visible en móviles (< 768px)</div>
<div class="d-none d-md-block d-lg-none">Solo visible en tablets (768-991px)</div>

<!-- Texto responsive -->
<p class="text-start text-md-center text-lg-end">
    Izquierda en móvil, centro en tablet, derecha en desktop
</p>

<!-- Márgenes responsive -->
<div class="mt-3 mt-md-4 mt-lg-5">
    Margen superior crece según el tamaño de pantalla
</div>
```

**Tabla de Breakpoints:**

| Breakpoint | Prefijo | Tamaño | Dispositivo |
|------------|---------|---------|-------------|
| Extra small | (ninguno) | < 576px | Móviles portrait |
| Small | sm | ≥ 576px | Móviles landscape |
| Medium | md | ≥ 768px | Tablets |
| Large | lg | ≥ 992px | Desktops |
| Extra large | xl | ≥ 1200px | Desktops grandes |
| Extra extra large | xxl | ≥ 1400px | Desktops muy grandes |

**Explicación:**
- Sin prefijo - Se aplica a todos los tamaños
- Con prefijo (sm, md, lg, xl, xxl) - Se aplica desde ese tamaño hacia arriba
- Puedes combinar múltiples breakpoints en un elemento

---

## 36. Flex Utilities Avanzadas

```html
<!-- Dirección del flex -->
<div class="d-flex flex-row">Items en fila →</div>
<div class="d-flex flex-row-reverse">Items en fila invertida ←</div>
<div class="d-flex flex-column">Items en columna ↓</div>
<div class="d-flex flex-column-reverse">Items en columna invertida ↑</div>

<!-- Justificar contenido (eje principal) -->
<div class="d-flex justify-content-start">Inicio</div>
<div class="d-flex justify-content-end">Final</div>
<div class="d-flex justify-content-center">Centro</div>
<div class="d-flex justify-content-between">Espacio entre</div>
<div class="d-flex justify-content-around">Espacio alrededor</div>
<div class="d-flex justify-content-evenly">Espacio uniforme</div>

<!-- Alinear items (eje cruzado) -->
<div class="d-flex align-items-start" style="height: 100px;">Inicio</div>
<div class="d-flex align-items-end" style="height: 100px;">Final</div>
<div class="d-flex align-items-center" style="height: 100px;">Centro</div>
<div class="d-flex align-items-baseline">Línea base</div>
<div class="d-flex align-items-stretch" style="height: 100px;">Estirar</div>

<!-- Wrap (envolver items) -->
<div class="d-flex flex-wrap">Items se envuelven a nueva línea</div>
<div class="d-flex flex-nowrap">Items no se envuelven</div>
<div class="d-flex flex-wrap-reverse">Wrap invertido</div>

<!-- Gap (espacio entre items) -->
<div class="d-flex gap-1">Gap pequeño</div>
<div class="d-flex gap-2">Gap medio</div>
<div class="d-flex gap-3">Gap grande</div>

<!-- Flex grow y shrink -->
<div class="d-flex">
    <div class="flex-grow-1 p-2 bg-primary">Crece para llenar espacio</div>
    <div class="p-2 bg-success">Tamaño fijo</div>
</div>

<div class="d-flex">
    <div class="flex-shrink-1 p-2 bg-primary" style="width: 200px;">Puede encogerse</div>
    <div class="flex-shrink-0 p-2 bg-success" style="width: 200px;">No se encoge</div>
</div>

<!-- Alinear un item específico -->
<div class="d-flex align-items-start" style="height: 200px;">
    <div class="p-2 bg-primary">Item 1</div>
    <div class="p-2 bg-success align-self-center">Centrado</div>
    <div class="p-2 bg-danger">Item 3</div>
</div>

<!-- Order (orden de items) -->
<div class="d-flex">
    <div class="order-3 p-2 bg-primary">Primero en HTML, tercero visualmente</div>
    <div class="order-1 p-2 bg-success">Segundo en HTML, primero visualmente</div>
    <div class="order-2 p-2 bg-danger">Tercero en HTML, segundo visualmente</div>
</div>
```

**Explicación línea por línea:**
- `.flex-row` - Dirección horizontal (default)
- `.flex-column` - Dirección vertical
- `-reverse` - Invierte el orden
- `.justify-content-*` - Alineación en eje principal (horizontal en row)
- `.align-items-*` - Alineación en eje cruzado (vertical en row)
- `.flex-wrap` - Permite que items pasen a nueva línea
- `.gap-1/2/3` - Espacio entre items (sin afectar bordes externos)
- `.flex-grow-1` - Item crece para llenar espacio disponible
- `.flex-shrink-0` - Item no se encoge cuando falta espacio
- `.align-self-*` - Alinea un item específico diferente al resto
- `.order-1/2/3` - Cambia el orden visual (1 aparece primero)

---

## 37. Ejemplo Completo - Landing Page

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Landing Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="#">MiEmpresa</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link" href="#servicios">Servicios</a></li>
                    <li class="nav-item"><a class="nav-link" href="#testimonios">Testimonios</a></li>
                    <li class="nav-item"><a class="nav-link" href="#contacto">Contacto</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="bg-primary text-white text-center py-5">
        <div class="container">
            <h1 class="display-3 fw-bold">Bienvenido a MiEmpresa</h1>
            <p class="lead my-4">Soluciones innovadoras para tu negocio</p>
            <button class="btn btn-light btn-lg">Comenzar Ahora</button>
        </div>
    </section>

    <!-- Servicios -->
    <section id="servicios" class="py-5">
        <div class="container">
            <h2 class="text-center mb-5">Nuestros Servicios</h2>
            <div class="row g-4">
                <div class="col-md-4">
                    <div class="card h-100 shadow">
                        <div class="card-body text-center">
                            <h3 class="card-title">Diseño Web</h3>
                            <p class="card-text">Creamos sitios web modernos y responsive.</p>
                            <a href="#" class="btn btn-primary">Más Info</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card h-100 shadow">
                        <div class="card-body text-center">
                            <h3 class="card-title">Desarrollo</h3>
                            <p class="card-text">Aplicaciones web robustas y escalables.</p>
                            <a href="#" class="btn btn-primary">Más Info</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card h-100 shadow">
                        <div class="card-body text-center">
                            <h3 class="card-title">Marketing</h3>
                            <p class="card-text">Estrategias digitales efectivas.</p>
                            <a href="#" class="btn btn-primary">Más Info</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Testimonios -->
    <section id="testimonios" class="bg-light py-5">
        <div class="container">
            <h2 class="text-center mb-5">Lo Que Dicen Nuestros Clientes</h2>
            <div class="row">
                <div class="col-lg-6 mb-4">
                    <div class="card">
                        <div class="card-body">
                            <p class="card-text">"Excelente servicio, superaron nuestras expectativas."</p>
                            <footer class="blockquote-footer">Juan Pérez, <cite>CEO TechCorp</cite></footer>
                        </div>
                    </div>
                </div>
                <div class="col-lg-6 mb-4">
                    <div class="card">
                        <div class="card-body">
                            <p class="card-text">"Profesionales y creativos. Muy recomendados."</p>
                            <footer class="blockquote-footer">María García, <cite>Directora StartupX</cite></footer>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contacto -->
    <section id="contacto" class="py-5">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-6">
                    <h2 class="text-center mb-4">Contáctanos</h2>
                    <form>
                        <div class="mb-3">
                            <label for="nombre" class="form-label">Nombre</label>
                            <input type="text" class="form-control" id="nombre" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" required>
                        </div>
                        <div class="mb-3">
                            <label for="mensaje" class="form-label">Mensaje</label>
                            <textarea class="form-control" id="mensaje" rows="4" required></textarea>
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">Enviar Mensaje</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-4">
        <div class="container">
            <p class="mb-0">&copy; 2024 MiEmpresa. Todos los derechos reservados.</p>
            <div class="mt-3">
                <a href="#" class="text-white me-3">Facebook</a>
                <a href="#" class="text-white me-3">Twitter</a>
                <a href="#" class="text-white">LinkedIn</a>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

**Explicación del ejemplo completo:**
- **Navbar**: Barra de navegación responsive con collapse en móviles
- `.ms-auto`: Alinea los items del menú a la derecha
- **Hero Section**: Sección principal con fondo de color y texto centrado
- `.py-5`: Padding vertical grande para espaciado
- `.display-3`: Título extra grande
- **Servicios**: Grid de 3 columnas con cards
- `.g-4`: Gap de tamaño 4 entre columnas
- `.h-100`: Altura 100% para que todas las cards tengan la misma altura
- **Testimonios**: Sección con fondo claro
- `.bg-light`: Fondo gris muy claro
- **Contacto**: Formulario centrado
- `.justify-content-center`: Centra la columna del formulario
- `.d-grid`: Hace que el botón ocupe todo el ancho
- **Footer**: Pie de página oscuro con enlaces

---

## 38. Personalización con Variables CSS

Bootstrap usa variables CSS que puedes sobrescribir:

```html
<style>
    /* Personalizar colores principales */
    :root {
        --bs-primary: #6610f2;
        --bs-success: #198754;
        --bs-danger: #dc3545;
        --bs-font-sans-serif: 'Arial', sans-serif;
        --bs-border-radius: 0.5rem;
    }
    
    /* Personalizar un componente específico */
    .btn-custom {
        background-color: #ff6b6b;
        border-color: #ff6b6b;
        color: white;
    }
    
    .btn-custom:hover {
        background-color: #ff5252;
        border-color: #ff5252;
    }
</style>

<button class="btn btn-custom">Mi Botón Personalizado</button>
```

**Explicación:**
- `:root` - Define variables globales CSS
- `--bs-primary` - Variable de color primario de Bootstrap
- Puedes sobrescribir cualquier variable de Bootstrap
- También puedes crear tus propias clases personalizadas

---

## 39. Utilidades de Print (Impresión)

```html
<!-- Ocultar en impresión -->
<div class="d-print-none">No se imprime</div>

<!-- Mostrar solo en impresión -->
<div class="d-none d-print-block">Solo se ve al imprimir</div>

<!-- Inline en impresión -->
<div class="d-print-inline">Inline al imprimir</div>

<!-- Inline-block en impresión -->
<div class="d-print-inline-block">Inline-block al imprimir</div>
```

**Explicación:**
- `.d-print-none` - Oculta el elemento al imprimir
- `.d-print-block` - Muestra como block solo al imprimir
- `.d-print-inline` - Muestra como inline solo al imprimir
- `.d-print-inline-block` - Muestra como inline-block solo al imprimir
- Útil para ocultar menús, botones o mostrar información adicional en versión impresa

---

## 40. Icons con Bootstrap Icons

Bootstrap tiene su propia librería de iconos (opcional):

```html
<!-- CDN de Bootstrap Icons -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">

<!-- Usar iconos -->
<i class="bi bi-heart-fill text-danger"></i>
<i class="bi bi-star-fill text-warning"></i>
<i class="bi bi-check-circle-fill text-success"></i>
<i class="bi bi-x-circle-fill text-danger"></i>
<i class="bi bi-envelope-fill"></i>
<i class="bi bi-telephone-fill"></i>
<i class="bi bi-geo-alt-fill"></i>

<!-- Iconos en botones -->
<button class="btn btn-primary">
    <i class="bi bi-download"></i> Descargar
</button>

<button class="btn btn-success">
    <i class="bi bi-check-lg"></i> Guardar
</button>

<button class="btn btn-danger">
    <i class="bi bi-trash"></i> Eliminar
</button>

<!-- Tamaños de iconos -->
<i class="bi bi-heart" style="font-size: 1rem;"></i>
<i class="bi bi-heart" style="font-size: 2rem;"></i>
<i class="bi bi-heart" style="font-size: 3rem;"></i>
```

**Explicación:**
- Bootstrap Icons es una librería separada (debe incluirse aparte)
- `<i class="bi bi-nombre-del-icono">` - Estructura básica
- Funciona con todas las clases de color de Bootstrap (text-primary, text-danger, etc.)
- Se puede ajustar el tamaño con `font-size`
- Más de 1,800 iconos disponibles
- Totalmente gratuito y open source

---

## 41. Ratio (Aspect Ratios)

```html
<!-- Video responsive 16:9 -->
<div class="ratio ratio-16x9">
    <iframe src="https://www.youtube.com/embed/..." allowfullscreen></iframe>
</div>

<!-- Video 4:3 -->
<div class="ratio ratio-4x3">
    <iframe src="https://www.youtube.com/embed/..." allowfullscreen></iframe>
</div>

<!-- Cuadrado 1:1 -->
<div class="ratio ratio-1x1">
    <div class="bg-primary"></div>
</div>

<!-- 21:9 (ultrawide) -->
<div class="ratio ratio-21x9">
    <iframe src="https://www.youtube.com/embed/..." allowfullscreen></iframe>
</div>

<!-- Custom ratio -->
<div class="ratio" style="--bs-aspect-ratio: 50%;">
    <div class="bg-success"></div>
</div>
```

**Explicación:**
- `.ratio` - Clase base para mantener aspect ratio
- `.ratio-16x9` - Proporción 16:9 (videos HD)
- `.ratio-4x3` - Proporción 4:3 (videos clásicos)
- `.ratio-1x1` - Proporción cuadrada
- `.ratio-21x9` - Proporción ultrawide
- `--bs-aspect-ratio` - Variable CSS para ratios personalizados
- El contenido hijo se ajusta automáticamente al ratio

---

## 42. Object Fit

```html
<!-- Cover (cubre todo el espacio, puede recortar) -->
<img src="imagen.jpg" class="object-fit-cover" style="width: 300px; height: 200px;" alt="Cover">

<!-- Contain (cabe completo, puede dejar espacios) -->
<img src="imagen.jpg" class="object-fit-contain" style="width: 300px; height: 200px;" alt="Contain">

<!-- Fill (estira para llenar) -->
<img src="imagen.jpg" class="object-fit-fill" style="width: 300px; height: 200px;" alt="Fill">

<!-- Scale down -->
<img src="imagen.jpg" class="object-fit-scale" style="width: 300px; height: 200px;" alt="Scale">

<!-- None (mantiene tamaño original) -->
<img src="imagen.jpg" class="object-fit-none" style="width: 300px; height: 200px;" alt="None">
```

**Explicación:**
- `.object-fit-cover` - Imagen cubre el contenedor, mantiene proporción, puede recortar
- `.object-fit-contain` - Imagen completa visible, puede dejar espacios vacíos
- `.object-fit-fill` - Estira la imagen para llenar el espacio (distorsiona)
- `.object-fit-scale` - Como contain pero nunca agranda
- `.object-fit-none` - Mantiene tamaño original (puede recortar o dejar espacios)
- Requiere especificar width y height en el contenedor

---

## 43. Mejores Prácticas

### 1. Mobile First
```html
<!-- ✅ CORRECTO: Empezar sin prefijo (móviles), luego añadir -->
<div class="col-12 col-md-6 col-lg-4">
    Móvil: 100%, Tablet: 50%, Desktop: 33%
</div>

<!-- ❌ INCORRECTO: No usar solo lg sin definir comportamiento móvil -->
<div class="col-lg-4">
    <!-- Mal: no definido para móviles -->
</div>
```

### 2. No Mezclar Sistema de Grid con Flexbox Innecesariamente
```html
<!-- ✅ CORRECTO: Usar sistema de grid -->
<div class="container">
    <div class="row">
        <div class="col-md-6">Contenido</div>
        <div class="col-md-6">Contenido</div>
    </div>
</div>

<!-- ❌ EVITAR: Mezclar innecesariamente -->
<div class="container">
    <div class="d-flex">
        <div class="col-md-6">Contenido</div>
        <div class="col-md-6">Contenido</div>
    </div>
</div>
```

### 3. Usar Clases de Espaciado en lugar de CSS Inline
```html
<!-- ✅ CORRECTO: Usar clases de Bootstrap -->
<div class="mt-3 mb-4 px-2">Contenido</div>

<!-- ❌ EVITAR: CSS inline -->
<div style="margin-top: 1rem; margin-bottom: 1.5rem; padding-left: 0.5rem; padding-right: 0.5rem;">
    Contenido
</div>
```

### 4. Accesibilidad
```html
<!-- ✅ CORRECTO: Atributos ARIA y alt -->
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal" aria-label="Abrir modal">
    <i class="bi bi-plus"></i>
</button>

<img src="imagen.jpg" class="img-fluid" alt="Descripción significativa de la imagen">

<!-- ❌ EVITAR: Sin atributos de accesibilidad -->
<button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">
    <i class="bi bi-plus"></i>
</button>

<img src="imagen.jpg" class="img-fluid">
```

### 5. Rendimiento
```html
<!-- ✅ CORRECTO: Cargar JS al final del body -->
<body>
    <!-- contenido -->
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>

<!-- ✅ CORRECTO: Solo incluir componentes JS que necesites -->
<!-- Si no usas modals, popovers, etc., considera usar solo CSS -->
```

---

## 44. Recursos y Documentación

### Documentación Oficial
- **Sitio oficial**: https://getbootstrap.com/
- **Documentación**: https://getbootstrap.com/docs/5.3/
- **Ejemplos**: https://getbootstrap.com/docs/5.3/examples/
- **Bootstrap Icons**: https://icons.getbootstrap.com/

### CDN Links (Bootstrap 5.3)
```html
<!-- CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- JS Bundle (incluye Popper) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Bootstrap Icons -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
```

### Herramientas Útiles
- **Bootstrap Build**: Personaliza y descarga solo lo que necesitas
- **BootstrapCDN**: CDN rápido y confiable
- **Bootsnipp**: Snippets de código Bootstrap
- **Start Bootstrap**: Plantillas gratuitas

### Diferencias Bootstrap 5 vs 4
- jQuery ya NO es requerido
- Iconos propios (Bootstrap Icons)
- Utilidades mejoradas (gap, ratios, etc.)
- Offcanvas nativo
- Formularios mejorados
- RTL (Right-to-Left) support incorporado

---

## 45. Cheat Sheet Rápida

### Grid System
```
.container / .container-fluid
.row
.col / .col-{breakpoint}-{number}
.g-{size} // gap
```

### Spacing
```
m/p-{side}-{size}
sides: t(op), b(ottom), s(tart), e(nd), x(horizontal), y(vertical)
size: 0-5, auto
```

### Display
```
.d-{value}
.d-{breakpoint}-{value}
values: none, inline, block, flex, grid
```

### Colors
```
.text-{color}
.bg-{color}
colors: primary, secondary, success, danger, warning, info, light, dark
```

### Typography
```
.h1 - .h6
.display-1 - .display-6
.lead
.text-start/center/end
.fw-bold, .fst-italic
```

### Components
```
.btn .btn-{color}
.card .card-body
.navbar .nav-item .nav-link
.modal .modal-dialog
.alert .alert-{color}
```

---

## Resumen Final

Bootstrap es un framework potente que te permite:
- ✅ Crear sitios responsive rápidamente
- ✅ Usar componentes prediseñados y probados
- ✅ Mantener consistencia en tu diseño
- ✅ Ahorrar tiempo de desarrollo
- ✅ Tener código mantenible y escalable

**Tips Finales:**
1. Aprende bien el sistema de grid - es la base de todo
2. Usa las clases de utilidad en lugar de CSS personalizado cuando sea posible
3. Personaliza los colores y variables para tu marca
4. Siempre piensa mobile-first
5. Consulta la documentación oficial regularmente
6. Practica construyendo proyectos reales

**¡Ahora estás listo para crear sitios web increíbles con Bootstrap!** 🚀