"""
Script de un solo uso: crea el primer usuario administrador.
Correlo UNA vez (cualquier integrante del equipo, ya con su .env configurado)
para poder entrar por primera vez a la app.

    python crear_admin.py
"""
import getpass
from repositorios import usuarios as usuarios_repo

print("=== Crear usuario administrador inicial ===")
nombre = input("Nombre completo: ").strip()
correo = input("Correo: ").strip()
password = getpass.getpass("Contraseña: ").strip()

try:
    nuevo_id = usuarios_repo.crear_usuario(nombre, correo, password, rol="admin")
    print(f"Administrador creado con id {nuevo_id}. Ya puedes iniciar sesión en la app.")
except Exception as e:
    print(f"Error: {e}")
