import psycopg2
from core.config import DB_CONFIG, validar_config


def get_connection():
    """Punto único de conexión a la base — todos los repositorios lo usan."""
    validar_config()
    return psycopg2.connect(**DB_CONFIG)
