{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 📊 Guía Completa de Matplotlib\n",
    "\n",
    "## Visualización de Datos Explicada Paso a Paso\n",
    "\n",
    "Esta guía te enseñará todo lo esencial sobre Matplotlib, la librería de visualización más usada en Python.\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1️⃣ Instalación e Importación"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Importar las librerías necesarias\n",
    "import matplotlib.pyplot as plt  # plt es el alias estándar\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "# Para mostrar gráficos en el notebook\n",
    "%matplotlib inline\n",
    "\n",
    "print(\"✅ Librerías importadas correctamente\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2️⃣ Crear Datos de Ejemplo\n",
    "\n",
    "Vamos a crear una tabla simple de ventas para usar en todos los ejemplos."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Crear DataFrame de ejemplo: Ventas de una tienda\n",
    "data = {\n",
    "    'month': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto'],\n",
    "    'sales': [150, 180, 165, 220, 240, 210, 260, 280],\n",
    "    'expenses': [100, 120, 110, 140, 150, 130, 160, 170],\n",
    "    'profit': [50, 60, 55, 80, 90, 80, 100, 110],\n",
    "    'customers': [45, 52, 48, 65, 70, 62, 75, 82]\n",
    "}\n",
    "\n",
    "df = pd.DataFrame(data)\n",
    "\n",
    "print(\"📋 Nuestros datos de ejemplo:\")\n",
    "print(df)\n",
    "print(f\"\\n📊 Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "\n",
    "# 📈 PARTE 1: GRÁFICOS BÁSICOS\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3️⃣ Gráfico de Líneas (Line Plot)\n",
    "\n",
    "**Cuándo usar:** Para mostrar tendencias a lo largo del tiempo o secuencias.\n",
    "\n",
    "### Gráfico básico"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# plt.plot(x, y) → crea un gráfico de líneas\n",
    "# x: valores del eje horizontal\n",
    "# y: valores del eje vertical\n",
    "\n",
    "plt.plot(df['month'], df['sales'])\n",
    "\n",
    "# plt.show() → muestra el gráfico\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Gráfico con personalización básica"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Crear gráfico de líneas con color\n",
    "plt.plot(df['month'], df['sales'], color='blue')\n",
    "\n",
    "# plt.xlabel() → etiqueta del eje X\n",
    "plt.xlabel('Mes')\n",
    "\n",
    "# plt.ylabel() → etiqueta del eje Y\n",
    "plt.ylabel('Ventas ($)')\n",
    "\n",
    "# plt.title() → título del gráfico\n",
    "plt.title('Ventas Mensuales')\n",
    "\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Parámetros importantes de `plt.plot()`"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.plot(\n",
    "    df['month'],           # x: datos del eje X\n",
    "    df['sales'],           # y: datos del eje Y\n",
    "    color='blue',          # color: color de la línea ('red', 'green', 'blue', '#FF5733', etc.)\n",
    "    linewidth=2,           # linewidth: grosor de la línea (número)\n",
    "    linestyle='-',         # linestyle: estilo de línea ('-', '--', '-.', ':')\n",
    "    marker='o',            # marker: marcador en cada punto ('o', 's', '^', 'D', '*', etc.)\n",
    "    markersize=6,          # markersize: tamaño del marcador\n",
    "    markerfacecolor='red', # markerfacecolor: color de relleno del marcador\n",
    "    markeredgecolor='black', # markeredgecolor: color del borde del marcador\n",
    "    label='Ventas'         # label: etiqueta para la leyenda\n",
    ")\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Ventas ($)')\n",
    "plt.title('Ventas con Todos los Parámetros')\n",
    "\n",
    "# plt.legend() → muestra la leyenda\n",
    "plt.legend()\n",
    "\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Estilos de línea disponibles"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Crear figura más grande\n",
    "# plt.figure(figsize=(ancho, alto)) → establece tamaño en pulgadas\n",
    "plt.figure(figsize=(10, 6))\n",
    "\n",
    "# Diferentes estilos de línea\n",
    "plt.plot(df['month'], df['sales'], linestyle='-', label='Sólida (-)', linewidth=2)\n",
    "plt.plot(df['month'], df['expenses'], linestyle='--', label='Discontinua (--)', linewidth=2)\n",
    "plt.plot(df['month'], df['profit'], linestyle='-.', label='Punto-guión (-.)', linewidth=2)\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Cantidad ($)')\n",
    "plt.title('Diferentes Estilos de Línea')\n",
    "plt.legend()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Tipos de marcadores comunes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "\n",
    "# Diferentes marcadores\n",
    "plt.plot(df['month'][:4], df['sales'][:4], marker='o', markersize=8, label='Círculo (o)', linewidth=2)\n",
    "plt.plot(df['month'][:4], df['expenses'][:4], marker='s', markersize=8, label='Cuadrado (s)', linewidth=2)\n",
    "plt.plot(df['month'][:4], df['profit'][:4], marker='^', markersize=8, label='Triángulo (^)', linewidth=2)\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Cantidad ($)')\n",
    "plt.title('Diferentes Marcadores')\n",
    "plt.legend()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4️⃣ Gráfico de Barras (Bar Plot)\n",
    "\n",
    "**Cuándo usar:** Para comparar cantidades entre diferentes categorías.\n",
    "\n",
    "### Barras verticales"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# plt.bar(x, height) → crea gráfico de barras verticales\n",
    "# x: posiciones o categorías\n",
    "# height: altura de cada barra\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "plt.bar(df['month'], df['sales'])\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Ventas ($)')\n",
    "plt.title('Ventas por Mes - Barras Verticales')\n",
    "\n",
    "# plt.xticks(rotation=45) → rota las etiquetas del eje X\n",
    "plt.xticks(rotation=45)\n",
    "\n",
    "# plt.tight_layout() → ajusta automáticamente el espaciado\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Parámetros importantes de `plt.bar()`"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "\n",
    "plt.bar(\n",
    "    df['month'],              # x: posiciones de las barras\n",
    "    df['sales'],              # height: altura de las barras\n",
    "    color='skyblue',          # color: color de las barras\n",
    "    edgecolor='navy',         # edgecolor: color del borde\n",
    "    linewidth=1.5,            # linewidth: grosor del borde\n",
    "    alpha=0.7,                # alpha: transparencia (0=transparente, 1=opaco)\n",
    "    width=0.6,                # width: ancho de las barras (0-1)\n",
    "    label='Ventas'            # label: etiqueta para leyenda\n",
    ")\n",
    "\n",
    "plt.xlabel('Mes', fontsize=12)\n",
    "plt.ylabel('Ventas ($)', fontsize=12)\n",
    "plt.title('Barras con Personalización Completa', fontsize=14, fontweight='bold')\n",
    "plt.xticks(rotation=45)\n",
    "plt.legend()\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Barras horizontales"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# plt.barh(y, width) → gráfico de barras horizontales\n",
    "# y: categorías en el eje Y\n",
    "# width: longitud de las barras\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "plt.barh(df['month'], df['sales'], color='coral')\n",
    "plt.xlabel('Ventas ($)')\n",
    "plt.ylabel('Mes')\n",
    "plt.title('Ventas por Mes - Barras Horizontales')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Barras agrupadas (comparar múltiples series)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(12, 6))\n",
    "\n",
    "# Crear posiciones para las barras\n",
    "x = np.arange(len(df['month']))  # [0, 1, 2, 3, 4, 5, 6, 7]\n",
    "width = 0.25  # Ancho de cada barra\n",
    "\n",
    "# Crear barras en diferentes posiciones\n",
    "plt.bar(x - width, df['sales'], width, label='Ventas', color='blue')\n",
    "plt.bar(x, df['expenses'], width, label='Gastos', color='red')\n",
    "plt.bar(x + width, df['profit'], width, label='Ganancia', color='green')\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Cantidad ($)')\n",
    "plt.title('Comparación: Ventas, Gastos y Ganancias')\n",
    "\n",
    "# plt.xticks(positions, labels) → establece posiciones y etiquetas personalizadas\n",
    "plt.xticks(x, df['month'], rotation=45)\n",
    "plt.legend()\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Barras apiladas"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "\n",
    "# bottom: indica sobre qué valores apilar\n",
    "plt.bar(df['month'], df['expenses'], label='Gastos', color='red')\n",
    "plt.bar(df['month'], df['profit'], bottom=df['expenses'], label='Ganancia', color='green')\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Cantidad ($)')\n",
    "plt.title('Barras Apiladas: Gastos + Ganancia')\n",
    "plt.xticks(rotation=45)\n",
    "plt.legend()\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5️⃣ Gráfico de Dispersión (Scatter Plot)\n",
    "\n",
    "**Cuándo usar:** Para mostrar la relación entre dos variables numéricas."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# plt.scatter(x, y) → crea gráfico de dispersión\n",
    "# x: valores del eje X\n",
    "# y: valores del eje Y\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "plt.scatter(df['customers'], df['sales'])\n",
    "plt.xlabel('Número de Clientes')\n",
    "plt.ylabel('Ventas ($)')\n",
    "plt.title('Relación entre Clientes y Ventas')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Parámetros importantes de `plt.scatter()`"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "\n",
    "plt.scatter(\n",
    "    df['customers'],       # x: valores del eje X\n",
    "    df['sales'],           # y: valores del eje Y\n",
    "    s=100,                 # s: tamaño de los puntos (número o array)\n",
    "    c='red',               # c: color (nombre, código hex, o array para colores por valor)\n",
    "    marker='o',            # marker: forma del marcador\n",
    "    alpha=0.6,             # alpha: transparencia\n",
    "    edgecolors='black',    # edgecolors: color del borde\n",
    "    linewidths=1.5,        # linewidths: grosor del borde\n",
    "    label='Datos'          # label: etiqueta\n",
    ")\n",
    "\n",
    "plt.xlabel('Número de Clientes', fontsize=12)\n",
    "plt.ylabel('Ventas ($)', fontsize=12)\n",
    "plt.title('Scatter Plot Personalizado', fontsize=14)\n",
    "plt.legend()\n",
    "plt.grid(True, alpha=0.3)  # Agregar cuadrícula\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Scatter con tamaños y colores variables"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "\n",
    "# s: tamaño basado en otra variable (profit)\n",
    "# c: color basado en otra variable (expenses)\n",
    "# cmap: mapa de colores ('viridis', 'plasma', 'coolwarm', 'spring', etc.)\n",
    "\n",
    "scatter = plt.scatter(\n",
    "    df['customers'],\n",
    "    df['sales'],\n",
    "    s=df['profit'] * 3,      # Tamaño proporcional a ganancia\n",
    "    c=df['expenses'],         # Color basado en gastos\n",
    "    cmap='viridis',          # Mapa de colores\n",
    "    alpha=0.6,\n",
    "    edgecolors='black'\n",
    ")\n",
    "\n",
    "plt.xlabel('Número de Clientes')\n",
    "plt.ylabel('Ventas ($)')\n",
    "plt.title('Scatter con Tamaño (Ganancia) y Color (Gastos)')\n",
    "\n",
    "# plt.colorbar() → muestra barra de colores\n",
    "plt.colorbar(scatter, label='Gastos ($)')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6️⃣ Histograma\n",
    "\n",
    "**Cuándo usar:** Para mostrar la distribución de una variable numérica."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# plt.hist(data) → crea histograma\n",
    "# data: array de valores\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "plt.hist(df['sales'])\n",
    "plt.xlabel('Ventas ($)')\n",
    "plt.ylabel('Frecuencia')\n",
    "plt.title('Distribución de Ventas')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Parámetros importantes de `plt.hist()`"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "\n",
    "plt.hist(\n",
    "    df['sales'],           # data: datos a graficar\n",
    "    bins=5,                # bins: número de barras/intervalos\n",
    "    color='skyblue',       # color: color de las barras\n",
    "    edgecolor='black',     # edgecolor: color del borde\n",
    "    alpha=0.7,             # alpha: transparencia\n",
    "    label='Ventas'         # label: etiqueta\n",
    ")\n",
    "\n",
    "plt.xlabel('Ventas ($)')\n",
    "plt.ylabel('Frecuencia')\n",
    "plt.title('Histograma Personalizado')\n",
    "plt.legend()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 7️⃣ Gráfico de Pastel (Pie Chart)\n",
    "\n",
    "**Cuándo usar:** Para mostrar proporciones de un todo."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Usar solo los primeros 4 meses para mejor visualización\n",
    "months_subset = df['month'][:4]\n",
    "sales_subset = df['sales'][:4]\n",
    "\n",
    "plt.figure(figsize=(8, 8))\n",
    "\n",
    "# plt.pie(sizes, labels) → crea gráfico de pastel\n",
    "# sizes: valores (proporciones)\n",
    "# labels: etiquetas de cada porción\n",
    "\n",
    "plt.pie(sales_subset, labels=months_subset)\n",
    "plt.title('Distribución de Ventas')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Parámetros importantes de `plt.pie()`"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 8))\n",
    "\n",
    "colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']\n",
    "explode = (0.1, 0, 0, 0)  # \"explotar\" la primera porción\n",
    "\n",
    "plt.pie(\n",
    "    sales_subset,          # sizes: valores\n",
    "    labels=months_subset,   # labels: etiquetas\n",
    "    autopct='%1.1f%%',     # autopct: formato de porcentaje\n",
    "    colors=colors,          # colors: lista de colores\n",
    "    explode=explode,        # explode: separar porciones (tupla con distancias)\n",
    "    shadow=True,            # shadow: agregar sombra\n",
    "    startangle=90           # startangle: ángulo de inicio (0-360)\n",
    ")\n",
    "\n",
    "plt.title('Gráfico de Pastel Personalizado', fontsize=14)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 8️⃣ Gráfico de Área (Area Plot)\n",
    "\n",
    "**Cuándo usar:** Para mostrar cambios acumulativos a lo largo del tiempo."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "\n",
    "# plt.fill_between(x, y) → rellena área bajo la curva\n",
    "# x: valores del eje X\n",
    "# y: valores del eje Y\n",
    "\n",
    "plt.fill_between(df['month'], df['sales'], alpha=0.3, color='blue', label='Ventas')\n",
    "plt.plot(df['month'], df['sales'], color='blue', linewidth=2)\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Ventas ($)')\n",
    "plt.title('Gráfico de Área - Ventas')\n",
    "plt.xticks(rotation=45)\n",
    "plt.legend()\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Áreas apiladas (múltiples series)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(12, 6))\n",
    "\n",
    "# Crear índices numéricos para el eje X\n",
    "x = np.arange(len(df['month']))\n",
    "\n",
    "# plt.stackplot(x, y1, y2, ...) → crea áreas apiladas\n",
    "plt.stackplot(\n",
    "    x,\n",
    "    df['expenses'],\n",
    "    df['profit'],\n",
    "    labels=['Gastos', 'Ganancia'],\n",
    "    colors=['#ff6b6b', '#4ecdc4'],\n",
    "    alpha=0.7\n",
    ")\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Cantidad ($)')\n",
    "plt.title('Áreas Apiladas: Gastos y Ganancia')\n",
    "plt.xticks(x, df['month'], rotation=45)\n",
    "plt.legend(loc='upper left')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "\n",
    "# 🎨 PARTE 2: PERSONALIZACIÓN AVANZADA\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 9️⃣ Tamaño y Resolución"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# plt.figure(figsize=(width, height)) → establece tamaño\n",
    "# Tamaño en pulgadas (inches)\n",
    "# Por defecto: (6.4, 4.8)\n",
    "\n",
    "plt.figure(figsize=(12, 4))  # Ancho y bajo\n",
    "plt.plot(df['month'], df['sales'], marker='o')\n",
    "plt.title('Gráfico Ancho')\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "plt.figure(figsize=(6, 8))  # Estrecho y alto\n",
    "plt.plot(df['month'], df['sales'], marker='o')\n",
    "plt.title('Gráfico Alto')\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🔟 Colores\n",
    "\n",
    "### Formas de especificar colores"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(12, 8))\n",
    "\n",
    "# 1. Nombres de colores básicos\n",
    "plt.plot(df['month'][:4], df['sales'][:4], color='red', linewidth=3, label='Nombre: red')\n",
    "\n",
    "# 2. Nombres de colores extendidos\n",
    "plt.plot(df['month'][:4], df['expenses'][:4], color='skyblue', linewidth=3, label='Nombre: skyblue')\n",
    "\n",
    "# 3. Código hexadecimal\n",
    "plt.plot(df['month'][:4], df['profit'][:4], color='#FF5733', linewidth=3, label='Hex: #FF5733')\n",
    "\n",
    "# 4. RGB (valores entre 0 y 1)\n",
    "plt.plot(df['month'][:4], df['customers'][:4], color=(0.2, 0.8, 0.3), linewidth=3, label='RGB: (0.2, 0.8, 0.3)')\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Valores')\n",
    "plt.title('Diferentes Formas de Especificar Colores')\n",
    "plt.legend(fontsize=10)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Colores básicos más usados\n",
    "\n",
    "```python\n",
    "'b' o 'blue'    → Azul\n",
    "'g' o 'green'   → Verde\n",
    "'r' o 'red'     → Rojo\n",
    "'c' o 'cyan'    → Cian\n",
    "'m' o 'magenta' → Magenta\n",
    "'y' o 'yellow'  → Amarillo\n",
    "'k' o 'black'   → Negro\n",
    "'w' o 'white'   → Blanco\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1️⃣1️⃣ Cuadrícula (Grid)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "plt.plot(df['month'], df['sales'], marker='o', linewidth=2)\n",
    "\n",
    "# plt.grid() → activa/desactiva cuadrícula\n",
    "# True/False: activar o desactivar\n",
    "# alpha: transparencia (0-1)\n",
    "# linestyle: estilo de línea\n",
    "# color: color de la cuadrícula\n",
    "\n",
    "plt.grid(\n",
    "    True,                  # Activar cuadrícula\n",
    "    alpha=0.3,            # Transparencia\n",
    "    linestyle='--',       # Línea discontinua\n",
    "    color='gray'          # Color gris\n",
    ")\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Ventas ($)')\n",
    "plt.title('Gráfico con Cuadrícula')\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Cuadrícula solo en un eje"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "plt.plot(df['month'], df['sales'], marker='o', linewidth=2)\n",
    "\n",
    "# axis='x': solo eje X\n",
    "# axis='y': solo eje Y\n",
    "# axis='both': ambos ejes (default)\n",
    "\n",
    "plt.grid(True, axis='y', alpha=0.3, linestyle='--')\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Ventas ($)')\n",
    "plt.title('Cuadrícula Solo en Eje Y')\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1️⃣2️⃣ Leyenda (Legend)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "\n",
    "plt.plot(df['month'], df['sales'], marker='o', label='Ventas')\n",
    "plt.plot(df['month'], df['expenses'], marker='s', label='Gastos')\n",
    "plt.plot(df['month'], df['profit'], marker='^', label='Ganancia')\n",
    "\n",
    "# plt.legend() → muestra la leyenda\n",
    "# loc: ubicación ('upper left', 'upper right', 'lower left', 'lower right', 'center', 'best')\n",
    "# fontsize: tamaño de fuente\n",
    "# frameon: mostrar/ocultar marco\n",
    "# shadow: agregar sombra\n",
    "\n",
    "plt.legend(\n",
    "    loc='upper left',     # Ubicación\n",
    "    fontsize=11,          # Tamaño de fuente\n",
    "    frameon=True,         # Mostrar marco\n",
    "    shadow=True,          # Sombra\n",
    "    fancybox=True         # Esquinas redondeadas\n",
    ")\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Cantidad ($)')\n",
    "plt.title('Gráfico con Leyenda Personalizada')\n",
    "plt.xticks(rotation=45)\n",
    "plt.grid(True, alpha=0.3)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Posiciones de leyenda disponibles\n",
    "\n",
    "```python\n",
    "'best'         → mejor posición automática\n",
    "'upper right'  → arriba derecha\n",
    "'upper left'   → arriba izquierda\n",
    "'lower left'   → abajo izquierda\n",
    "'lower right'  → abajo derecha\n",
    "'right'        → derecha centro\n",
    "'center left'  → centro izquierda\n",
    "'center right' → centro derecha\n",
    "'lower center' → abajo centro\n",
    "'upper center' → arriba centro\n",
    "'center'       → centro\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1️⃣3️⃣ Personalización de Texto"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "plt.plot(df['month'], df['sales'], marker='o', linewidth=2, color='blue')\n",
    "\n",
    "# Parámetros de formato de texto:\n",
    "# fontsize: tamaño (número o 'small', 'medium', 'large', 'x-large')\n",
    "# fontweight: grosor ('normal', 'bold', 'heavy', 'light')\n",
    "# fontstyle: estilo ('normal', 'italic', 'oblique')\n",
    "# color: color del texto\n",
    "\n",
    "plt.xlabel('Mes', fontsize=14, fontweight='bold', color='darkblue')\n",
    "plt.ylabel('Ventas ($)', fontsize=14, fontweight='bold', color='darkblue')\n",
    "plt.title('Título con Formato Personalizado', fontsize=16, fontweight='bold', fontstyle='italic', color='navy')\n",
    "\n",
    "plt.xticks(rotation=45, fontsize=10)\n",
    "plt.yticks(fontsize=10)\n",
    "plt.grid(True, alpha=0.3)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1️⃣4️⃣ Anotaciones y Texto"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "plt.plot(df['month'], df['sales'], marker='o', linewidth=2, color='blue')\n",
    "\n",
    "# plt.text(x, y, texto) → agrega texto en posición (x, y)\n",
    "plt.text(\n",
    "    3,                    # Posición X\n",
    "    250,                  # Posición Y\n",
    "    'Máximo',             # Texto\n",
    "    fontsize=12,\n",
    "    color='red',\n",
    "    fontweight='bold'\n",
    ")\n",
    "\n",
    "# plt.annotate() → agrega anotación con flecha\n",
    "max_idx = df['sales'].idxmax()  # Índice del valor máximo\n",
    "max_value = df['sales'].max()   # Valor máximo\n",
    "\n",
    "plt.annotate(\n",
    "    f'Pico: ${max_value}',        # Texto\n",
    "    xy=(max_idx, max_value),      # Punto a señalar (coordenadas del dato)\n",
    "    xytext=(max_idx-1, max_value+20),  # Posición del texto\n",
    "    fontsize=11,\n",
    "    color='red',\n",
    "    fontweight='bold',\n",
    "    arrowprops=dict(              # Propiedades de la flecha\n",
    "        arrowstyle='->',\n",
    "        color='red',\n",
    "        lw=2\n",
    "    )\n",
    ")\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Ventas ($)')\n",
    "plt.title('Gráfico con Anotaciones')\n",
    "plt.xticks(rotation=45)\n",
    "plt.grid(True, alpha=0.3)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1️⃣5️⃣ Límites de Ejes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "plt.plot(df['month'], df['sales'], marker='o', linewidth=2)\n",
    "\n",
    "# plt.xlim(min, max) → establece límites del eje X\n",
    "# plt.ylim(min, max) → establece límites del eje Y\n",
    "\n",
    "plt.ylim(100, 300)  # Eje Y de 100 a 300\n",
    "\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Ventas ($)')\n",
    "plt.title('Gráfico con Límites Personalizados en Y')\n",
    "plt.xticks(rotation=45)\n",
    "plt.grid(True, alpha=0.3)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1️⃣6️⃣ Múltiples Subgráficos (Subplots)\n",
    "\n",
    "**Muy útil para comparar múltiples gráficos lado a lado.**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# plt.subplot(filas, columnas, posición) → crea subgráfico\n",
    "# Ejemplo: plt.subplot(2, 2, 1) → 2 filas, 2 columnas, posición 1\n",
    "\n",
    "plt.figure(figsize=(12, 8))\n",
    "\n",
    "# Subgráfico 1 (arriba izquierda)\n",
    "plt.subplot(2, 2, 1)  # 2 filas, 2 columnas, posición 1\n",
    "plt.plot(df['month'], df['sales'], color='blue', marker='o')\n",
    "plt.title('Ventas')\n",
    "plt.xticks(rotation=45)\n",
    "plt.grid(True, alpha=0.3)\n",
    "\n",
    "# Subgráfico 2 (arriba derecha)\n",
    "plt.subplot(2, 2, 2)  # 2 filas, 2 columnas, posición 2\n",
    "plt.bar(df['month'], df['expenses'], color='red')\n",
    "plt.title('Gastos')\n",
    "plt.xticks(rotation=45)\n",
    "plt.grid(True, alpha=0.3)\n",
    "\n",
    "# Subgráfico 3 (abajo izquierda)\n",
    "plt.subplot(2, 2, 3)  # 2 filas, 2 columnas, posición 3\n",
    "plt.scatter(df['customers'], df['profit'], color='green', s=100)\n",
    "plt.title('Clientes vs Ganancia')\n",
    "plt.xlabel('Clientes')\n",
    "plt.ylabel('Ganancia')\n",
    "plt.grid(True, alpha=0.3)\n",
    "\n",
    "# Subgráfico 4 (abajo derecha)\n",
    "plt.subplot(2, 2, 4)  # 2 filas, 2 columnas, posición 4\n",
    "plt.hist(df['sales'], bins=4, color='orange', edgecolor='black')\n",
    "plt.title('Distribución de Ventas')\n",
    "plt.xlabel('Ventas')\n",
    "plt.ylabel('Frecuencia')\n",
    "plt.grid(True, alpha=0.3)\n",
    "\n",
    "plt.tight_layout()  # Ajusta espaciado automáticamente\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Método alternativo con `plt.subplots()`"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# fig, axes = plt.subplots(filas, columnas)\n",
    "# fig: objeto figura\n",
    "# axes: array de ejes (subgráficos)\n",
    "\n",
    "fig, axes = plt.subplots(2, 2, figsize=(12, 8))\n",
    "\n",
    "# axes[fila, columna] para acceder a cada subgráfico\n",
    "\n",
    "# Subgráfico [0, 0] (arriba izquierda)\n",
    "axes[0, 0].plot(df['month'], df['sales'], color='blue', marker='o')\n",
    "axes[0, 0].set_title('Ventas')\n",
    "axes[0, 0].tick_params(axis='x', rotation=45)\n",
    "axes[0, 0].grid(True, alpha=0.3)\n",
    "\n",
    "# Subgráfico [0, 1] (arriba derecha)\n",
    "axes[0, 1].bar(df['month'], df['expenses'], color='red')\n",
    "axes[0, 1].set_title('Gastos')\n",
    "axes[0, 1].tick_params(axis='x', rotation=45)\n",
    "axes[0, 1].grid(True, alpha=0.3)\n",
    "\n",
    "# Subgráfico [1, 0] (abajo izquierda)\n",
    "axes[1, 0].scatter(df['customers'], df['profit'], color='green', s=100)\n",
    "axes[1, 0].set_title('Clientes vs Ganancia')\n",
    "axes[1, 0].set_xlabel('Clientes')\n",
    "axes[1, 0].set_ylabel('Ganancia')\n",
    "axes[1, 0].grid(True, alpha=0.3)\n",
    "\n",
    "# Subgráfico [1, 1] (abajo derecha)\n",
    "axes[1, 1].hist(df['sales'], bins=4, color='orange', edgecolor='black')\n",
    "axes[1, 1].set_title('Distribución de Ventas')\n",
    "axes[1, 1].set_xlabel('Ventas')\n",
    "axes[1, 1].set_ylabel('Frecuencia')\n",
    "axes[1, 1].grid(True, alpha=0.3)\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1️⃣7️⃣ Guardar Gráficos"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "plt.plot(df['month'], df['sales'], marker='o', linewidth=2, color='blue')\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Ventas ($)')\n",
    "plt.title('Ventas Mensuales')\n",
    "plt.xticks(rotation=45)\n",
    "plt.grid(True, alpha=0.3)\n",
    "plt.tight_layout()\n",
    "\n",
    "# plt.savefig(nombre_archivo) → guarda el gráfico\n",
    "# Formatos soportados: .png, .jpg, .pdf, .svg\n",
    "\n",
    "plt.savefig(\n",
    "    'grafico_ventas.png',  # Nombre del archivo\n",
    "    dpi=300,               # dpi: resolución (dots per inch)\n",
    "    bbox_inches='tight',   # bbox_inches: ajustar bordes\n",
    "    transparent=False      # transparent: fondo transparente\n",
    ")\n",
    "\n",
    "plt.show()\n",
    "\n",
    "print(\"✅ Gráfico guardado como 'grafico_ventas.png'\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1️⃣8️⃣ Estilos Predefinidos"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Ver estilos disponibles\n",
    "print(\"🎨 Estilos disponibles:\")\n",
    "print(plt.style.available)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# plt.style.use('nombre_estilo') → aplica estilo predefinido\n",
    "\n",
    "# Estilo ggplot (similar a ggplot2 de R)\n",
    "plt.style.use('ggplot')\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "plt.plot(df['month'], df['sales'], marker='o', linewidth=2, label='Ventas')\n",
    "plt.plot(df['month'], df['expenses'], marker='s', linewidth=2, label='Gastos')\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Cantidad ($)')\n",
    "plt.title('Estilo: ggplot')\n",
    "plt.legend()\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# Restaurar estilo por defecto\n",
    "plt.style.use('default')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Estilo seaborn (más moderno)\n",
    "plt.style.use('seaborn-v0_8')\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "plt.plot(df['month'], df['sales'], marker='o', linewidth=2, label='Ventas')\n",
    "plt.plot(df['month'], df['expenses'], marker='s', linewidth=2, label='Gastos')\n",
    "plt.xlabel('Mes')\n",
    "plt.ylabel('Cantidad ($)')\n",
    "plt.title('Estilo: Seaborn')\n",
    "plt.legend()\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# Restaurar estilo por defecto\n",
    "plt.style.use('default')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "\n",
    "# 📚 CHEATSHEET DE MATPLOTLIB\n",
    "\n",
    "## Guía de referencia rápida\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🔷 IMPORTACIÓN\n",
    "\n",
    "```python\n",
    "import matplotlib.pyplot as plt\n",
    "%matplotlib inline  # Solo en notebooks\n",
    "```"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 🔷 TIPOS DE GRÁFICOS\n",
    "\n",
    "### Gráfico de Líneas\n",
    "```python\n",
    "plt.plot(x, y, color='blue', linewidth=2, linestyle='-', marker='o', label='Datos')\n",
    "```\n",
    "**Uso:** Tendencias, series temporales\n",
    "\n",
    "**Parámetros:**\n",
    "- `color`: Color de la línea\n",
    "- `linewidth`: Grosor de línea (número)\n",
    "- `linestyle`: Estilo (`'-'`, `'--'`, `'-.'`, `':'`)\n",
    "- `marker`: Marcador en puntos (`'o'`, `'s'`, `'^'`, `'D'`, `'*'`)\n",
    "- `markersize`: Tamaño del marcador\n",
    "- `label`: Etiqueta para leyenda\n",
    "\n",
    "---\n",
    "\n",
    "### Gráfico de Barras\n",
    "```python\n",
    "plt.bar(x, height, color='skyblue', edgecolor='black', width=0.8, alpha=0.7)\n",
    "plt.barh(y, width)  # Barras horizontales\n",
    "```\n",
    "**Uso:** Comparar categorías\n",
    "\n",
    "**Parámetros:**\n",
    "- `height` o `width`: Tamaño de las barras\n",
    "- `color`: Color de las barras\n",
    "- `edgecolor`: Color del borde\n",
    "- `linewidth`: Grosor del borde\n",
    "- `alpha`: Transparencia (0-1)\n",
    "- `width`: Ancho de las barras (para plt.bar)\n",
    "\n",
    "---\n",
    "\n",
    "### Gráfico de Dispersión\n",
    "```python\n",
    "plt.scatter(x, y, s=50, c='red', marker='o', alpha=0.5, edgecolors='black')\n",
    "```\n",
    "**Uso:** Relación entre dos variables\n",
    "\n",
    "**Parámetros:**\n",
    "- `s`: Tamaño de puntos (número o array)\n",
    "- `c`: Color (nombre, hex, o array para colores variables)\n",
    "- `marker`: Forma del marcador\n",
    "- `alpha`: Transparencia\n",
    "- `cmap`: Mapa de colores (`'viridis'`, `'plasma'`, `'coolwarm'`)\n",
    "- `edgecolors`: Color del borde\n",
    "\n",
    "---\n",
    "\n",
    "### Histograma\n",
    "```python\n",
    "plt.hist(data, bins=10, color='skyblue', edgecolor='black', alpha=0.7)\n",
    "```\n",
    "**Uso:** Distribución de datos\n",
    "\n",
    "**Parámetros:**\n",
    "- `bins`: Número de barras/intervalos\n",
    "- `color`: Color de las barras\n",
    "- `edgecolor`: Color del borde\n",
    "- `alpha`: Transparencia\n",
    "\n",
    "---\n",
    "\n",
    "### Gráfico de Pastel\n",
    "```python\n",
    "plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, explode=explode, shadow=True, startangle=90)\n",
    "```\n",
    "**Uso:** Proporciones de un total\n",
    "\n",
    "**Parámetros:**\n",
    "- `sizes`: Valores (proporciones)\n",
    "- `labels`: Etiquetas de cada porción\n",
    "- `autopct`: Formato de porcentaje (`'%1.1f%%'`)\n",
    "- `explode`: Separar porciones (tupla de distancias)\n",
    "- `colors`: Lista de colores\n",
    "- `shadow`: Agregar sombra (True/False)\n",
    "- `startangle`: Ángulo de inicio (0-360)\n",
    "\n",
    "---\n",
    "\n",
    "### Gráfico de Área\n",
    "```python\n",
    "plt.fill_between(x, y, alpha=0.3, color='blue')\n",
    "plt.stackplot(x, y1, y2, labels=['A', 'B'], colors=['red', 'blue'])\n",
    "```\n",
    "**Uso:** Cambios acumulativos, comparar proporciones"
   ]
  },
  {
   "cell_type
