import requests

URL_BASE = 'http://127.0.0.1:5000'

def registrar_usuario():
    print("\n--- REGISTRO DE NUEVO USUARIO ---")
    usuario = input("Ingresá el nombre de usuario: ")
    contrasena = input("Ingresá la contraseña: ")
    datos = {"usuario": usuario, "contraseña": contrasena}
    try:
        respuesta = requests.post(f"{URL_BASE}/registro", json=datos)
        print(f"Código de estado: {respuesta.status_code}")
        print(f"Respuesta del servidor: {respuesta.json()}\n")
    except requests.exceptions.ConnectionError:
        print("\nError: No se pudo conectar. ¿El servidor está corriendo?")

def iniciar_sesion():
    print("\n--- INICIO DE SESIÓN ---")
    usuario = input("Ingresá tu nombre de usuario: ")
    contrasena = input("Ingresá tu contraseña: ")
    datos = {"usuario": usuario, "contraseña": contrasena}
    try:
        print("\nVerificando credenciales...")
        respuesta = requests.post(f"{URL_BASE}/login", json=datos)
        print(f"Código de estado: {respuesta.status_code}")
        print(f"Respuesta del servidor: {respuesta.json()}\n")
    except requests.exceptions.ConnectionError:
        print("\nError: No se pudo conectar. ¿El servidor está corriendo?")

def ver_tareas():
    print("\n--- SOLICITANDO TAREAS (HTML) ---")
    try:
        print("\nPidiendo el panel web al servidor...")
        # Hacemos la petición GET
        respuesta = requests.get(f"{URL_BASE}/tareas")
        print(f"Código de estado: {respuesta.status_code}")
        # Usamos .text en lugar de .json() porque estamos esperando un texto HTML
        print(f"Respuesta del servidor (HTML):\n\n{respuesta.text}\n")
    except requests.exceptions.ConnectionError:
        print("\nError: No se pudo conectar. ¿El servidor está corriendo?")

if __name__ == '__main__':
    print("=== API FLASK - CLIENTE DE PRUEBAS ===")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Ver tareas (Recibir HTML)")
    opcion = input("Elegí una opción (1, 2 o 3): ")
    
    if opcion == '1':
        registrar_usuario()
    elif opcion == '2':
        iniciar_sesion()
    elif opcion == '3':
        ver_tareas()
    else:
        print("Opción no válida.")