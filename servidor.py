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

# Configuro el puerto 5000 para escuchar las peticiones
if __name__ == '__main__':
    print("Iniciando servidor API Flask en el puerto 5000...")
    app.run(debug=True, port=5000)