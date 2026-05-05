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
# Configuro el puerto 5000 para escuchar las peticiones
if __name__ == '__main__':
    print("Iniciando servidor API Flask en el puerto 5000...")
    app.run(debug=True, port=5000)