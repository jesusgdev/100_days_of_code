# PyCharm Live Templates para Python - Guía Completa

## 📋 Índice
1. [¿Cómo Instalar Live Templates?](#cómo-instalar-live-templates)
2. [Python Básico](#python-básico)
3. [Flask](#flask)
4. [Selenium WebDriver](#selenium-webdriver)
5. [Decoradores](#decoradores)
6. [Manejo de Archivos](#manejo-de-archivos)
7. [Testing](#testing)
8. [POO (Programación Orientada a Objetos)](#poo-programación-orientada-a-objetos)
9. [API & Requests](#api--requests)
10. [Utilidades](#utilidades)

---

## ¿Cómo Instalar Live Templates?

### Paso 1: Abrir configuración
1. En PyCharm: `File` → `Settings` (Windows/Linux) o `PyCharm` → `Preferences` (Mac)
2. Navegar a: `Editor` → `Live Templates`

### Paso 2: Crear nuevo template
1. Click en el `+` (Add)
2. Seleccionar `Live Template`
3. Escribir:
   - **Abbreviation**: El shortcut (ej: `pyinit`)
   - **Description**: Descripción del template
   - **Template text**: El código del snippet
4. Click en `Define` → Seleccionar `Python`
5. Click `Apply` y `OK`

### Paso 3: Usar el template
- Escribe el abbreviation (ej: `pyinit`)
- Presiona `Tab` o `Enter`

---

## Python Básico

### 1. `pyinit` - Python Main Structure
**Descripción:** Estructura básica de un archivo Python ejecutable

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
$MODULE_NAME$

Description: $DESCRIPTION$
Author: $AUTHOR$
Date: $DATE$
"""

def main():
    """Main function to execute the program"""
    $END$
    pass


if __name__ == "__main__":
    main()
```

**Variables:**
- `$MODULE_NAME$` → Expression: `capitalize(fileNameWithoutExtension())`
- `$DESCRIPTION$` → Default value: `Module description here`
- `$AUTHOR$` → Default value: `Your Name`
- `$DATE$` → Expression: `date()`
- `$END$` → Posición final del cursor

---

### 2. `pyclass` - Python Class Template
**Descripción:** Template completo para crear una clase

```python
class $CLASS_NAME$:
    """
    $DESCRIPTION$
    
    Attributes:
        $ATTRIBUTE$ ($TYPE$): Description of attribute
    """
    
    def __init__(self, $PARAMS$):
        """
        Initialize $CLASS_NAME$ instance
        
        Args:
            $PARAMS$: Parameter description
        """
        self.$ATTRIBUTE$ = $PARAMS$
        $END$
    
    def __str__(self):
        """String representation of the object"""
        return f"$CLASS_NAME$({self.$ATTRIBUTE$})"
    
    def __repr__(self):
        """Official string representation"""
        return f"$CLASS_NAME$($ATTRIBUTE$={self.$ATTRIBUTE$!r})"
```

**Variables:**
- `$CLASS_NAME$` → Default: `MyClass`
- `$DESCRIPTION$` → Default: `Class description`
- `$ATTRIBUTE$` → Default: `attribute`
- `$TYPE$` → Default: `str`
- `$PARAMS$` → Default: `param`

---

### 3. `pyfunc` - Function with Docstring
**Descripción:** Función documentada con docstring estilo Google

```python
def $FUNCTION_NAME$($PARAMS$) -> $RETURN_TYPE$:
    """
    $DESCRIPTION$
    
    Args:
        $PARAMS$ ($PARAM_TYPE$): Parameter description
    
    Returns:
        $RETURN_TYPE$: Return value description
    
    Raises:
        $EXCEPTION$: When error occurs
    
    Example:
        >>> $FUNCTION_NAME$($EXAMPLE_ARGS$)
        $EXAMPLE_OUTPUT$
    """
    $END$
    pass
```

**Variables:**
- `$FUNCTION_NAME$` → Default: `my_function`
- `$PARAMS$` → Default: `param`
- `$RETURN_TYPE$` → Default: `None`
- `$DESCRIPTION$` → Default: `Function description`

---

### 4. `pytry` - Try-Except Block
**Descripción:** Bloque try-except con logging

```python
try:
    $STATEMENT$
except $EXCEPTION$ as e:
    # Handle $EXCEPTION$ error
    print(f"Error: {e}")
    $END$
except Exception as e:
    # Handle any other unexpected errors
    print(f"Unexpected error: {e}")
finally:
    # Cleanup code (optional)
    pass
```

**Variables:**
- `$STATEMENT$` → Default: `# Your code here`
- `$EXCEPTION$` → Default: `ValueError`

---

### 5. `pyloop` - Common Loop Patterns
**Descripción:** Patrones comunes de loops

```python
# Loop through list with index and value
for index, $ITEM$ in enumerate($LIST$):
    $END$
    pass

# Loop through dictionary
for key, value in $DICT$.items():
    pass

# Loop with range
for i in range($START$, $END$, $STEP$):
    pass
```

**Variables:**
- `$ITEM$` → Default: `item`
- `$LIST$` → Default: `my_list`
- `$DICT$` → Default: `my_dict`

---

## Flask

### 6. `flaskapp` - Flask Basic App
**Descripción:** Estructura básica de una aplicación Flask

```python
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

# Initialize Flask application
app = Flask(__name__)
app.secret_key = '$SECRET_KEY$'  # Change this in production!

# ==============================================================================
# ROUTES
# ==============================================================================

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html')


@app.route('/$ROUTE$', methods=['GET', 'POST'])
def $FUNCTION_NAME$():
    """$DESCRIPTION$"""
    if request.method == 'POST':
        # Handle POST request
        data = request.form.get('$FIELD$')
        return redirect(url_for('index'))
    
    # Handle GET request
    return render_template('$TEMPLATE$.html')


# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == '__main__':
    # Run the application
    # debug=True: Auto-reload on code changes (ONLY for development)
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Variables:**
- `$SECRET_KEY$` → Default: `your-secret-key-change-in-production`
- `$ROUTE$` → Default: `route`
- `$FUNCTION_NAME$` → Default: `my_route`

---

### 7. `flaskroute` - Flask Route Template
**Descripción:** Template para crear rutas Flask rápidamente

```python
@app.route('/$ROUTE$', methods=['$METHODS$'])
def $FUNCTION_NAME$():
    """
    $DESCRIPTION$
    
    Methods: $METHODS$
    Returns: $RETURN_DESC$
    """
    if request.method == 'POST':
        # Handle POST request
        $POST_LOGIC$
        return redirect(url_for('$REDIRECT$'))
    
    # Handle GET request
    $GET_LOGIC$
    return render_template('$TEMPLATE$.html', $VARIABLES$)
```

**Variables:**
- `$ROUTE$` → Default: `my-route`
- `$METHODS$` → Default: `GET, POST`
- `$FUNCTION_NAME$` → Default: `my_function`

---

### 8. `flaskapi` - Flask API Endpoint
**Descripción:** Endpoint API RESTful con JSON

```python
@app.route('/api/$ENDPOINT$', methods=['$METHODS$'])
def $FUNCTION_NAME$():
    """
    API endpoint for $DESCRIPTION$
    
    Methods: $METHODS$
    
    Request Body (JSON):
        {
            "$FIELD1$": "value1",
            "$FIELD2$": "value2"
        }
    
    Response (JSON):
        {
            "status": "success",
            "data": {...},
            "message": "Description"
        }
    """
    try:
        if request.method == 'POST':
            # Get JSON data from request
            data = request.json
            
            # Validate required fields
            if not data or '$FIELD1$' not in data:
                return jsonify({
                    "status": "error",
                    "message": "Missing required field: $FIELD1$"
                }), 400
            
            # Process data
            $PROCESSING_LOGIC$
            
            # Return success response
            return jsonify({
                "status": "success",
                "data": $RESULT$,
                "message": "$SUCCESS_MESSAGE$"
            }), 201
        
        elif request.method == 'GET':
            # Handle GET request
            $GET_LOGIC$
            return jsonify({
                "status": "success",
                "data": $DATA$
            }), 200
            
    except Exception as e:
        # Handle errors
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
```

**Variables:**
- `$ENDPOINT$` → Default: `resource`
- `$METHODS$` → Default: `GET, POST`
- `$FUNCTION_NAME$` → Default: `api_function`

---

## Selenium WebDriver

### 9. `selsetup` - Selenium Setup
**Descripción:** Configuración inicial de Selenium WebDriver

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# ==============================================================================
# WEBDRIVER SETUP
# ==============================================================================

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keep browser open
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Uncomment to run headless (no browser window)
# chrome_options.add_argument("--headless")

# Initialize Chrome driver
driver = webdriver.Chrome(options=chrome_options)

# Hide webdriver detection
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Set implicit wait (optional)
driver.implicitly_wait(10)

# Maximize window
driver.maximize_window()

try:
    # Navigate to webpage
    driver.get("$URL$")
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    $END$
    
finally:
    # Cleanup
    # driver.quit()  # Uncomment to close browser
    pass
```

**Variables:**
- `$URL$` → Default: `https://www.example.com`

---

### 10. `selfind` - Selenium Find Element
**Descripción:** Buscar elementos con espera explícita

```python
# Wait for element to be clickable
$ELEMENT$ = WebDriverWait(driver, $TIMEOUT$).until(
    ec.element_to_be_clickable((By.$BY_TYPE$, "$SELECTOR$"))
)

# Click the element
$ELEMENT$.click()

# Alternative: Find multiple elements
$ELEMENTS$ = driver.find_elements(By.$BY_TYPE$, "$SELECTOR$")

# Loop through elements
for element in $ELEMENTS$:
    print(element.text)
    $END$
```

**Variables:**
- `$ELEMENT$` → Default: `element`
- `$TIMEOUT$` → Default: `10`
- `$BY_TYPE$` → Default: `CSS_SELECTOR`
- `$SELECTOR$` → Default: `.class-name`

---

### 11. `selform` - Selenium Fill Form
**Descripción:** Template para llenar formularios

```python
# Wait for form to be ready
form_loaded = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.$FORM_BY$, "$FORM_SELECTOR$"))
)

# Find input fields
$FIELD1$ = driver.find_element(By.$BY_TYPE$, "$SELECTOR1$")
$FIELD2$ = driver.find_element(By.$BY_TYPE$, "$SELECTOR2$")

# Clear and fill fields
$FIELD1$.clear()
$FIELD1$.click()
time.sleep(0.5)
$FIELD1$.send_keys("$VALUE1$")

$FIELD2$.clear()
$FIELD2$.click()
time.sleep(0.5)
$FIELD2$.send_keys("$VALUE2$")

# Submit form
submit_button = WebDriverWait(driver, 10).until(
    ec.element_to_be_clickable((By.$SUBMIT_BY$, "$SUBMIT_SELECTOR$"))
)
submit_button.click()

# Wait for submission to complete
time.sleep(2)
$END$
```

**Variables:**
- `$FORM_BY$` → Default: `CSS_SELECTOR`
- `$FORM_SELECTOR$` → Default: `form`
- `$BY_TYPE$` → Default: `NAME`

---

### 12. `selclass` - Selenium Bot Class
**Descripción:** Clase para bot de Selenium organizado

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time


class $CLASS_NAME$:
    """
    $DESCRIPTION$
    
    Attributes:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance for explicit waits
    """
    
    def __init__(self):
        """Initialize the bot with Chrome driver"""
        # Configure Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Initialize driver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        # Hide webdriver detection
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
    
    def navigate_to(self, url):
        """
        Navigate to a specific URL
        
        Args:
            url (str): The URL to navigate to
        """
        self.driver.get(url)
        time.sleep(2)
    
    def find_element_safe(self, by, selector, timeout=10):
        """
        Safely find an element with explicit wait
        
        Args:
            by: Selenium By locator type
            selector (str): Element selector
            timeout (int): Wait timeout in seconds
            
        Returns:
            WebElement: Found element or None
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                ec.presence_of_element_located((by, selector))
            )
            return element
        except Exception as e:
            print(f"Error finding element {selector}: {e}")
            return None
    
    def click_element(self, by, selector, scroll=True):
        """
        Click an element with optional scroll
        
        Args:
            by: Selenium By locator type
            selector (str): Element selector
            scroll (bool): Whether to scroll to element first
        """
        element = self.find_element_safe(by, selector)
        if element:
            if scroll:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", 
                    element
                )
                time.sleep(0.5)
            element.click()
    
    def $METHOD_NAME$(self, $PARAMS$):
        """
        $METHOD_DESCRIPTION$
        
        Args:
            $PARAMS$: Parameter description
        """
        $END$
        pass
    
    def quit(self):
        """Close the browser and clean up"""
        if self.driver:
            self.driver.quit()
```

**Variables:**
- `$CLASS_NAME$` → Default: `WebBot`
- `$DESCRIPTION$` → Default: `Selenium automation bot`
- `$METHOD_NAME$` → Default: `custom_method`

---

## Decoradores

### 13. `pydec` - Decorator Template
**Descripción:** Template para crear decoradores

```python
from functools import wraps
import time


def $DECORATOR_NAME$($PARAMS$):
    """
    $DESCRIPTION$
    
    Args:
        $PARAMS$: Decorator parameters
        
    Usage:
        @$DECORATOR_NAME$($EXAMPLE_ARGS$)
        def my_function():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Before function execution
            $BEFORE_LOGIC$
            
            # Execute the function
            result = func(*args, **kwargs)
            
            # After function execution
            $AFTER_LOGIC$
            
            return result
        return wrapper
    return decorator
```

**Variables:**
- `$DECORATOR_NAME$` → Default: `my_decorator`
- `$PARAMS$` → Default: `param`
- `$DESCRIPTION$` → Default: `Decorator description`

---

### 14. `dectime` - Timing Decorator
**Descripción:** Decorador para medir tiempo de ejecución

```python
from functools import wraps
import time


def measure_time(func):
    """
    Decorator to measure function execution time
    
    Usage:
        @measure_time
        def my_function():
            time.sleep(1)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        # Execute function
        result = func(*args, **kwargs)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"⏱️  {func.__name__} took {execution_time:.4f} seconds")
        
        return result
    return wrapper
```

---

### 15. `declog` - Logging Decorator
**Descripción:** Decorador para logging automático

```python
from functools import wraps
from datetime import datetime


def log_calls(func):
    """
    Decorator to log function calls with arguments and results
    
    Usage:
        @log_calls
        def add(a, b):
            return a + b
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log function call
        print(f"[{timestamp}] 📞 Calling: {func.__name__}")
        print(f"  Args: {args}")
        print(f"  Kwargs: {kwargs}")
        
        # Execute function
        try:
            result = func(*args, **kwargs)
            print(f"  ✅ Result: {result}")
            return result
        except Exception as e:
            print(f"  ❌ Error: {e}")
            raise
    
    return wrapper
```

---

## Manejo de Archivos

### 16. `pyfile` - File Operations
**Descripción:** Operaciones comunes con archivos

```python
import os
import json


# ==============================================================================
# READ FILE
# ==============================================================================

def read_file(filepath):
    """
    Read text file content
    
    Args:
        filepath (str): Path to the file
        
    Returns:
        str: File content
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


# ==============================================================================
# WRITE FILE
# ==============================================================================

def write_file(filepath, content):
    """
    Write content to text file
    
    Args:
        filepath (str): Path to the file
        content (str): Content to write
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"✅ File saved: {filepath}")
    except Exception as e:
        print(f"❌ Error writing file: {e}")


# ==============================================================================
# JSON OPERATIONS
# ==============================================================================

def read_json(filepath):
    """Read JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: JSON file '{filepath}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return None


def write_json(filepath, data):
    """Write data to JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"✅ JSON saved: {filepath}")
    except Exception as e:
        print(f"❌ Error writing JSON: {e}")


# ==============================================================================
# FILE UTILITIES
# ==============================================================================

def file_exists(filepath):
    """Check if file exists"""
    return os.path.exists(filepath)


def create_directory(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"✅ Directory created: {directory}")


$END$
```

---

### 17. `pycsv` - CSV Operations
**Descripción:** Operaciones con archivos CSV

```python
import csv
import os


def read_csv(filepath):
    """
    Read CSV file and return list of dictionaries
    
    Args:
        filepath (str): Path to CSV file
        
    Returns:
        list: List of dictionaries (one per row)
    """
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(dict(row))
        print(f"✅ Read {len(data)} rows from {filepath}")
        return data
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found")
        return []
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return []


def write_csv(filepath, data, fieldnames=None):
    """
    Write list of dictionaries to CSV file
    
    Args:
        filepath (str): Path to CSV file
        data (list): List of dictionaries to write
        fieldnames (list): Column names (optional, inferred from first row)
    """
    if not data:
        print("⚠️  Warning: No data to write")
        return
    
    if fieldnames is None:
        fieldnames = data[0].keys()
    
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(data)
        print(f"✅ Wrote {len(data)} rows to {filepath}")
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")


$END$
```

---

## Testing

### 18. `pytest` - Pytest Test Class
**Descripción:** Template para tests con pytest

```python
import pytest
from $MODULE$ import $FUNCTION_OR_CLASS$


class Test$CLASS_NAME$:
    """
    Test suite for $DESCRIPTION$
    """
    
    @pytest.fixture
    def setup_data(self):
        """
        Fixture to set up test data
        
        Returns:
            dict: Test data
        """
        data = {
            "$KEY1$": "$VALUE1$",
            "$KEY2$": "$VALUE2$"
        }
        return data
    
    def test_$TEST_NAME$(self, setup_data):
        """
        Test $TEST_DESCRIPTION$
        
        Args:
            setup_data: Fixture providing test data
        """
        # Arrange
        expected = $EXPECTED_VALUE$
        input_value = setup_data["$KEY1$"]
        
        # Act
        result = $FUNCTION_OR_CLASS$(input_value)
        
        # Assert
        assert result == expected, f"Expected {expected}, got {result}"
    
    def test_$TEST_NAME$_edge_case(self):
        """Test edge case for $TEST_DESCRIPTION$"""
        # Test with empty input
        result = $FUNCTION_OR_CLASS$("")
        assert result is not None
        
        # Test with None
        with pytest.raises($EXCEPTION$):
            $FUNCTION_OR_CLASS$(None)
    
    @pytest.mark.parametrize("input_val, expected", [
        ("$INPUT1$", "$OUTPUT1$"),
        ("$INPUT2$", "$OUTPUT2$"),
        ("$INPUT3$", "$OUTPUT3$"),
    ])
    def test_$TEST_NAME$_multiple_cases(self, input_val, expected):
        """Test multiple cases with parametrize"""
        result = $FUNCTION_OR_CLASS$(input_val)
        assert result == expected


$END$
```

**Variables:**
- `$MODULE$` → Default: `my_module`
- `$CLASS_NAME$` → Default: `MyFunction`
- `$TEST_NAME$` → Default: `basic_functionality`

---

## POO (Programación Orientada a Objetos)

### 19. `pydataclass` - Dataclass Template
**Descripción:** Clase usando dataclasses (Python 3.7+)

```python
from dataclasses import dataclass, field
from typing import $TYPE_HINTS$


@dataclass
class $CLASS_NAME$:
    """
    $DESCRIPTION$
    
    Attributes:
        $ATTR1$ ($TYPE1$): Description of attribute 1
        $ATTR2$ ($TYPE2$): Description of attribute 2
    """
    
    # Required attributes
    $ATTR1$: $TYPE1$
    $ATTR2$: $TYPE2$
    
    # Optional attributes with defaults
    $ATTR3$: $TYPE3$ = $DEFAULT_VALUE$
    
    # Attribute with default factory (for mutable defaults)
    $ATTR4$: list = field(default_factory=list)
    
    def __post_init__(self):
        """Executed after __init__ for validation or processing"""
        # Validate attributes
        if not isinstance(self.$ATTR1$, $TYPE1$):
            raise TypeError(f"$ATTR1$ must be of type $TYPE1$")
        
        $END$
    
    def $METHOD_NAME$(self):
        """$METHOD_DESCRIPTION$"""
        pass
```

**Variables:**
- `$CLASS_NAME$` → Default: `MyDataClass`
- `$TYPE_HINTS$` → Default: `List, Dict, Optional`
- `$ATTR1$` → Default: `name`

---

### 20. `pyabstract` - Abstract Base Class
**Descripción:** Clase abstracta con ABC

```python
from abc import ABC, abstractmethod
from typing import $TYPE_HINTS$


class $CLASS_NAME$(ABC):
    """
    Abstract base class for $DESCRIPTION$
    
    This class defines the interface that all subclasses must implement.
    """
    
    def __init__(self, $PARAMS$):
        """
        Initialize the abstract class
        
        Args:
            $PARAMS$: Parameter description
        """
        self.$ATTRIBUTE$ = $PARAMS$
    
    @abstractmethod
    def $ABSTRACT_METHOD$(self, $METHOD_PARAMS$) -> $RETURN_TYPE$:
        """
        Abstract method that must be implemented by subclasses
        
        Args:
            $METHOD_PARAMS$: Parameter description
            
        Returns:
            $RETURN_TYPE$: Return value description
        """
        pass
    
    @abstractmethod
    def $ABSTRACT_METHOD2$(self) -> $RETURN_TYPE2$:
        """Another abstract method"""
        pass
    
    def concrete_method(self):
        """
        Concrete method available to all subclasses
        """
        return f"Concrete implementation using {self.$ATTRIBUTE$}"


# Example implementation
class $CONCRETE_CLASS$(ClassName):
    """Concrete implementation of $CLASS_NAME$"""
    
    def $ABSTRACT_METHOD$(self, $METHOD_PARAMS$) -> $RETURN_TYPE$:
        """Implementation of abstract method"""
        $END$
        pass
    
    def $ABSTRACT_METHOD2$(self) -> $RETURN_TYPE2$:
        """Implementation of abstract method 2"""
        pass
```

---

## API & Requests

### 21. `pyreq` - Requests API Template
**Descripción:** Template para hacer peticiones HTTP con requests

```python
import requests
import json
from typing import Optional, Dict, Any


class APIClient:
    """
    HTTP API Client using requests library
    
    Attributes:
        base_url (str): Base URL for the API
        headers (dict): Default headers for requests
        timeout (int): Request timeout in seconds
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = 30
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Make GET request
        
        Args:
            endpoint: API endpoint (e.g., '/users')
            params: Query parameters
            
        Returns:
            dict: Response data or None if error
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: Unable to connect to {url}")
            return None
        except requests.exceptions.Timeout:
            print(f"❌ Timeout Error: Request took longer than {self.timeout}s")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Make POST request
        
        Args:
            endpoint: API endpoint
            data: Data to send in request body
            
        Returns:
            dict: Response data or None if error
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.post(
                url,
                json=data,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")
            print(f"Response: {response.text}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make PUT request"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.put(url, json=data, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ PUT Error: {e}")
            return None
    
    def delete(self, endpoint: str) -> bool:
        """
        Make DELETE request
        
        Args:
            endpoint: API endpoint
            
        Returns:
            bool: True if successful, False otherwise
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.delete(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ DELETE Error: {e}")
            return False


# ==============================================================================
# USAGE EXAMPLE
# ==============================================================================

if __name__ == "__main__":
    # Initialize client
    client = APIClient("https://api.example.com", api_key="your-api-key")
    
    # GET request
    users = client.get("/users", params={"page": 1, "limit": 10})
    if users:
        print(f"✅ Retrieved {len(users)} users")
    
    # POST request
    new_user = {
        "name": "John Doe",
        "email": "john@example.com"
    }
    result = client.post("/users", data=new_user)
    if result:
        print(f"✅ User created: {result}")
    
    $END$
```

---

## Utilidades

### 22. `pyenv` - Environment Variables
**Descripción:** Template para manejo de variables de entorno

```python
import os
from dotenv import load_dotenv
from typing import Optional


# ==============================================================================
# LOAD ENVIRONMENT VARIABLES
# ==============================================================================

# Load variables from .env file
load_dotenv(dotenv_path=".env")


# ==============================================================================
# ENVIRONMENT CONFIGURATION
# ==============================================================================

class Config:
    """
    Configuration class to manage environment variables
    
    Usage:
        config = Config()
        api_key = config.API_KEY
    """
    
    # Required variables (will raise error if not set)
    API_KEY: str = os.environ["API_KEY"]
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    
    # Optional variables with defaults
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    PORT: int = int(os.getenv("PORT", "5000"))
    HOST: str = os.getenv("HOST", "localhost")
    
    # Environment type
    ENV: str = os.getenv("ENV", "development")
    
    @classmethod
    def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get environment variable with optional default
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            str: Environment variable value or default
        """
        return os.getenv(key, default)
    
    @classmethod
    def validate(cls):
        """
        Validate that all required environment variables are set
        
        Raises:
            EnvironmentError: If required variables are missing
        """
        required_vars = ["API_KEY", "DATABASE_URL"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
        
        print("✅ All required environment variables are set")


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Get environment variable with error handling
    
    Args:
        key: Variable name
        default: Default value if not found
        required: If True, raises error when variable not found
        
    Returns:
        str: Variable value
        
    Raises:
        EnvironmentError: If required variable not found
    """
    value = os.getenv(key, default)
    
    if required and value is None:
        raise EnvironmentError(f"Required environment variable '{key}' not found")
    
    return value


$END$


# ==============================================================================
# EXAMPLE .env FILE
# ==============================================================================
"""
# .env file example
# Copy this to create your own .env file

# API Configuration
API_KEY=your-api-key-here
API_SECRET=your-api-secret-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Application Settings
DEBUG=True
PORT=5000
HOST=0.0.0.0
ENV=development

# External Services
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
"""
```

---

### 23. `pylog` - Logging Configuration
**Descripción:** Configuración completa de logging

```python
import logging
import sys
from datetime import datetime
from pathlib import Path


# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================

def setup_logging(
    log_file: str = "app.log",
    log_level: int = logging.INFO,
    console_output: bool = True
) -> logging.Logger:
    """
    Configure logging with file and console handlers
    
    Args:
        log_file: Path to log file
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Whether to output logs to console
        
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        fmt='%(levelname)s: %(message)s'
    )
    
    # File handler (detailed logs)
    file_handler = logging.FileHandler(
        log_dir / log_file,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Console handler (simple logs)
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)
    
    return logger


# ==============================================================================
# USAGE EXAMPLE
# ==============================================================================

# Initialize logger
logger = setup_logging(
    log_file=f"app_{datetime.now().strftime('%Y%m%d')}.log",
    log_level=logging.DEBUG,
    console_output=True
)

# Log messages at different levels
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

# Log with exception information
try:
    result = 1 / 0
except Exception as e:
    logger.exception("An error occurred:")  # Automatically includes traceback


# ==============================================================================
# CUSTOM LOGGER CLASS
# ==============================================================================

class CustomLogger:
    """
    Custom logger wrapper with emoji and colored output
    """
    
    def __init__(self, name: str = __name__):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler with custom format
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def success(self, message: str):
        """Log success message"""
        self.logger.info(f"✅ {message}")
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(f"❌ {message}")
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(f"⚠️  {message}")
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(f"ℹ️  {message}")
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(f"🐛 {message}")


$END$
```

---

### 24. `pyarg` - Argparse Template
**Descripción:** Template para argumentos de línea de comandos

```python
import argparse
import sys
from typing import Namespace


def parse_arguments() -> Namespace:
    """
    Parse command line arguments
    
    Returns:
        Namespace: Parsed arguments
        
    Usage:
        python script.py --input file.txt --output result.txt --verbose
    """
    
    parser = argparse.ArgumentParser(
        description="$SCRIPT_DESCRIPTION$",
        epilog="Example: python script.py --input data.txt --output result.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Required arguments
    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Input file path'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Output file path'
    )
    
    # Optional arguments
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.json',
        help='Configuration file path (default: config.json)'
    )
    
    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'csv', 'xml'],
        default='json',
        help='Output format (default: json)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=100,
        help='Maximum number of items to process (default: 100)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate arguments
    if args.limit <= 0:
        parser.error("--limit must be a positive integer")
    
    return args


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main():
    """Main function to execute the script"""
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Access arguments
    input_file = args.input
    output_file = args.output
    verbose = args.verbose
    config_file = args.config
    output_format = args.format
    limit = args.limit
    
    # Display configuration
    if verbose:
        print("=" * 50)
        print("Configuration:")
        print(f"  Input:  {input_file}")
        print(f"  Output: {output_file}")
        print(f"  Format: {output_format}")
        print(f"  Limit:  {limit}")
        print(f"  Config: {config_file}")
        print("=" * 50)
    
    # Your script logic here
    $END$
    print("✅ Process completed successfully!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
```

---

### 25. `pyscrape` - Web Scraping Template
**Descripción:** Template para web scraping con BeautifulSoup

```python
import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict, Optional


class WebScraper:
    """
    Web scraping utility using BeautifulSoup
    
    Attributes:
        base_url (str): Base URL for scraping
        headers (dict): Request headers
        session: Requests session for connection pooling
    """
    
    def __init__(self, base_url: str):
        """
        Initialize web scraper
        
        Args:
            base_url: Base URL to scrape
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """
        Get BeautifulSoup object from URL
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup: Parsed HTML or None if error
        """
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
            return None
    
    def scrape_$ENTITY$(self, url: str) -> List[Dict[str, str]]:
        """
        Scrape $ENTITY$ data from URL
        
        Args:
            url: URL to scrape
            
        Returns:
            list: List of dictionaries containing scraped data
        """
        soup = self.get_soup(url)
        if not soup:
            return []
        
        results = []
        
        # Find all items (adjust selector as needed)
        items = soup.find_all('$ITEM_SELECTOR, class_='$ITEM_CLASS)
        
        for item in items:
            try:
                data = {
                    '$FIELD1: self.clean_text(item.find('$SELECTOR1).text),
                    '$FIELD2: self.clean_text(item.find('$SELECTOR2).text),
                    '$FIELD3: item.find('$SELECTOR3)['href'] if item.find('$SELECTOR3) else None
                }
                results.append(data)
                
            except AttributeError as e:
                print(f"⚠️  Warning: Could not parse item - {e}")
                continue
        
        print(f"✅ Scraped {len(results)} items from {url}")
        return results
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean scraped text
        
        Args:
            text: Raw text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        import re
        cleaned = re.sub(r'\s+', ' ', text.strip())
        return cleaned
    
    def save_to_json(self, data: List[Dict], filename: str):
        """
        Save scraped data to JSON file
        
        Args:
            data: Data to save
            filename: Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"✅ Data saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")
    
    def close(self):
        """Close the session"""
        self.session.close()


# ==============================================================================
# USAGE EXAMPLE
# ==============================================================================

if __name__ == "__main__":
    # Initialize scraper
    scraper = WebScraper("https://example.com")
    
    # Scrape data
    data = scraper.scrape_$ENTITY$("https://example.com/page")
    
    # Save to JSON
    if data:
        scraper.save_to_json(data, "scraped_data.json")
    
    # Close session
    scraper.close()
    
    $END$
```

---

## 🎯 Quick Reference Table

| Abbreviation | Description | Use Case |
|-------------|-------------|----------|
| `pyinit` | Python main structure | Start new Python script |
| `pyclass` | Complete class template | Create new class |
| `pyfunc` | Documented function | Create function with docstring |
| `pytry` | Try-except block | Error handling |
| `pyloop` | Common loop patterns | Iteration |
| `flaskapp` | Flask application | Start Flask project |
| `flaskroute` | Flask route | Add new route |
| `flaskapi` | Flask API endpoint | Create REST API |
| `selsetup` | Selenium setup | Start Selenium project |
| `selfind` | Find element | Locate web elements |
| `selform` | Fill form | Automate form filling |
| `selclass` | Selenium bot class | Organized bot structure |
| `pydec` | Decorator template | Create decorator |
| `dectime` | Timing decorator | Measure execution time |
| `declog` | Logging decorator | Auto-log function calls |
| `pyfile` | File operations | Read/write files |
| `pycsv` | CSV operations | Work with CSV files |
| `pytest` | Pytest test class | Write unit tests |
| `pydataclass` | Dataclass | Modern Python class |
| `pyabstract` | Abstract class | Define interfaces |
| `pyreq` | API client | HTTP requests |
| `pyenv` | Environment vars | Config management |
| `pylog` | Logging config | Setup logging |
| `pyarg` | Argparse | CLI arguments |
| `pyscrape` | Web scraper | Scrape websites |

---

## 💡 Tips para Usar Live Templates

1. **Personaliza variables**: Ajusta los valores por defecto según tus necesidades
2. **Usa Tab para navegar**: Presiona Tab para moverte entre variables
3. **Combina templates**: Puedes usar varios templates en el mismo archivo
4. **Crea tus propios**: Estos son ejemplos, ¡crea los tuyos!
5. **Exporta/Importa**: Puedes exportar tus templates para compartirlos

---

## 📤 Exportar Templates

1. `File` → `Manage IDE Settings` → `Export Settings`
2. Selecciona `Live templates`
3. Guarda el archivo `.zip`
4. Para importar: `Import Settings` → Selecciona el `.zip`

---

## 🚀 Shortcuts de PyCharm Útiles

| Shortcut | Acción |
|----------|--------|
| `Ctrl + Space` | Autocompletado |
| `Ctrl + J` | Ver live templates disponibles |
| `Ctrl + Alt + L` | Formatear código |
| `Ctrl + /` | Comentar/descomentar |
| `Shift + F10` | Run |
| `Shift + F9` | Debug |
| `Ctrl + Shift + F10` | Run current file |

---

## 📚 Recursos Adicionales

- [PyCharm Documentation - Live Templates](https://www.jetbrains.com/help/pycharm/using-live-templates.html)
- [Python PEP 8 Style Guide](https://pep8.org/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

**¡Feliz coding! 🐍✨**