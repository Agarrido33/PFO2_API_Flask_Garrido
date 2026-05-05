import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

# Levanto la app de Flask
app = Flask(__name__)
DB_NAME = "tareas_db.sqlite"

def inicializar_bd():
    # Me conecto a la base SQLite (si no existe, el motor la crea sola)
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    # Armo la tabla de usuarios. 
    # Le pongo UNIQUE al usuario para que no se me repitan en los registros.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )
    ''')
    
    # Guardo los cambios y cierro la conexión para no dejarla colgada
    conexion.commit()
    conexion.close()
    print("Base de datos y tablas inicializadas correctamente.")

# Ejecuto la función para asegurarme de que la BD esté lista antes de arrancar la API
inicializar_bd()

# --- ENDPOINTS DE LA API ---

# Primer endpoint: Recibo el JSON con los datos del usuario nuevo, encripto su contraseña y lo guardo en la base.
@app.route('/registro', methods=['POST'])
def registrar_usuario():
    # Capturo los datos que llegan desde el cliente en formato JSON
    datos = request.json
    usuario = datos.get('usuario')
    contrasena = datos.get('contraseña')
    
    # Valido que no me manden campos vacíos
    if not usuario or not contrasena:
        return jsonify({"error": "Faltan datos. Se requiere usuario y contraseña"}), 400
        
    # Hasheo (encripto) la contraseña por seguridad usando werkzeug
    contrasena_hasheada = generate_password_hash(contrasena)
    
    # Me conecto a la base para guardar el usuario
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    try:
        # Intento insertar el nuevo usuario en la tabla
        cursor.execute('INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)', (usuario, contrasena_hasheada))
        conexion.commit()
        mensaje = {"mensaje": f"Usuario '{usuario}' registrado con éxito."}
        codigo_estado = 201 # 201 significa 'Creado'
    except sqlite3.IntegrityError:
        # Si el usuario ya existe, la base salta porque le pusimos 'UNIQUE'
        mensaje = {"error": f"El usuario '{usuario}' ya existe."}
        codigo_estado = 409 # 409 significa 'Conflicto'
    finally:
        # Siempre cierro la conexión
        conexion.close()
        
    return jsonify(mensaje), codigo_estado

# Segundo endpoint: Verifico que el usuario exista en la base y que la contraseña tipeada coincida con el hash guardado.
@app.route('/login', methods=['POST'])
def iniciar_sesion():
    # Capturo los datos que llegan desde el cliente
    datos = request.json
    usuario = datos.get('usuario')
    contrasena = datos.get('contraseña')
    
    if not usuario or not contrasena:
        return jsonify({"error": "Faltan datos. Se requiere usuario y contraseña"}), 400
        
    # Me conecto a la base para buscar al usuario
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    # Busco solamente la contraseña hasheada del usuario ingresado
    cursor.execute('SELECT contrasena FROM usuarios WHERE usuario = ?', (usuario,))
    resultado = cursor.fetchone()
    conexion.close()
    
    # Validamos: ¿Existe el usuario? ¿La contraseña tipeada coincide con el hash guardado?
    if resultado and check_password_hash(resultado[0], contrasena):
        # Código 200 significa 'OK'
        return jsonify({"mensaje": "Inicio de sesión exitoso. ¡Acceso concedido a las tareas!"}), 200
    else:
        # Código 401 significa 'No Autorizado'
        return jsonify({"error": "Credenciales inválidas. Usuario o contraseña incorrectos."}), 401
    

# Tercer endpoint: Devuelvo el panel de tareas renderizado en formato HTML    
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    # Armo una respuesta HTML muy sencilla directamente desde Flask
    html_respuesta = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Panel de Tareas</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
            .contenedor { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <div class="contenedor">
            <h1>Tus Tareas Pendientes</h1>
            <p>¡Bienvenido! Este es el HTML devuelto por tu API Flask.</p>
            <ul>
                <li>Tarea 1: Finalizar PFO 2 de Redes</li>
                <li>Tarea 2: Entregar el trabajo en el campus</li>
            </ul>
        </div>
    </body>
    </html>
    """
    # Devuelvo el HTML y el código 200 de éxito
    return html_respuesta, 200    

# Configuro el puerto 5000 para escuchar las peticiones
if __name__ == '__main__':
    print("Iniciando servidor API Flask en el puerto 5000...")
    app.run(debug=True, port=5000)