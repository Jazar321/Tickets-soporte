import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}


def validar_config():
    """Revisa que el .env esté completo antes de intentar conectar."""
    faltantes = [k for k, v in DB_CONFIG.items() if not v]
    if faltantes:
        raise RuntimeError(
            f"Faltan variables en tu archivo .env: {faltantes}. "
            f"Copia .env.example como .env y llénalo con tus credenciales de Supabase."
        )
