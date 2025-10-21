# import time
#
# current_time = time.time()
# print(current_time)  # seconds since Jan 1st, 1970
#
#
# # Write your code below 👇
# import time
#
# def speed_calc_decorator(function):
#
#     def wrapper_function():
#         start = time.time()
#         result = function()
#         end = time.time()
#         total = end - start
#         print(f"{function.__name__} run speed: {total}")
#         return result
#     return wrapper_function
#
# @speed_calc_decorator
# def fast_function():
#     for i in range(1000000):
#         i * i
#
# @speed_calc_decorator
# def slow_function():
#     for i in range(10000000):
#         i * i
#
# fast_function()
# slow_function()

# from flask import Flask, request
#
# app = Flask(__name__)
#
# @app.route("/")
# def saludo():
#     return '''
#     <h1>Bienvenido a la pagina web</h1>
#         <h2>Opciones disponibles:</h2>
#             <ul>
#                 <li>formulario</li>
#                 <li>procesar</li>
#     '''
# # Por defecto, las rutas solo aceptan GET
# @app.route('/formulario')
# def mostrar_formulario():
#     return '''
#         <form method="POST" action="/procesar">
#             <input type="text" name="nombre" placeholder="Tu nombre">
#             <button type="submit">Enviar</button>
#         </form>
#     '''
#
# # methods=['GET', 'POST'] permite ambos métodos
# @app.route('/procesar', methods=['GET', 'POST'])
# def procesar():
#     if request.method == 'POST':
#         # Obtener datos del formulario
#         nombre = request.form.get('nombre')
#         return f"¡Hola {nombre}! (enviado por POST)"
#     else:
#         return "Esta página espera un POST"
#
# # Solo POST
# @app.route('/api/crear', methods=['POST'])
# def crear():
#     return "Recurso creado"
#
# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route('/usuarios')
# def usuarios():
#     lista_usuarios = [
#         {"nombre": "Ana", "edad": 28, "activo": True},
#         {"nombre": "Luis", "edad": 35, "activo": False},
#         {"nombre": "María", "edad": 22, "activo": True}
#     ]
#     return render_template('usuarios.html', usuarios=lista_usuarios)
#
# if __name__ == '__main__':
#     app.run(debug=True)

# TODO: Create the logging_decorator() function 👇
def logging_decorator(function):
    def wrapper(*args):
        print(f"You called {function.__name__}{args}")
        result = function(*args)
        print(f"It returned: {result}")
        return result
    return wrapper

# TODO: Use the decorator 👇

@logging_decorator
def a_function(*args):
    return sum(args)

a_function(1,2,3)
