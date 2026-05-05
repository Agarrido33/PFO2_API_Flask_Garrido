import requests

# URL de nuestro servidor local (la base de nuestra API)
URL_BASE = 'http://127.0.0.1:5000'

def registrar_usuario():
    print("\n--- REGISTRO DE NUEVO USUARIO ---")
    usuario = input("Ingresá el nombre de usuario: ")
    contrasena = input("Ingresá la contraseña: ")

    # Armamos el JSON con los datos que nos pide el PFO 2
    datos = {
        "usuario": usuario,
        "contraseña": contrasena
    }

    try:
        print("\nEnviando datos al servidor...")
        # Hacemos la petición POST al endpoint /registro
        respuesta = requests.post(f"{URL_BASE}/registro", json=datos)
        
        # Mostramos qué nos respondió nuestro servidor Flask
        print(f"Código de estado: {respuesta.status_code}")
        print(f"Respuesta del servidor: {respuesta.json()}\n")
        
    except requests.exceptions.ConnectionError:
        print("\nError: No se pudo conectar. ¿Te aseguraste de que el servidor esté corriendo?")

if __name__ == '__main__':
    registrar_usuario()
    