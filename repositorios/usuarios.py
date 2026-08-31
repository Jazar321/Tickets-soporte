"""Todo lo relacionado a cuentas de soporte/admin: login, alta y baja."""
import bcrypt
import psycopg2.extras
from core.conexion import get_connection


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verificar_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def crear_usuario(nombre: str, correo: str, password: str, rol: str) -> int:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO usuarios (nombre, correo, password_hash, rol) "
                "VALUES (%s, %s, %s, %s) RETURNING id",
                (nombre, correo, hash_password(password), rol),
            )
            nuevo_id = cur.fetchone()[0]
        conn.commit()
    return nuevo_id


def verificar_login(correo: str, password: str):
    """Devuelve el dict del usuario si login es correcto y está activo, si no None."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
            usuario = cur.fetchone()
    if not usuario:
        return None
    if not usuario["activo"]:
        return None
    if not verificar_password(password, usuario["password_hash"]):
        return None
    return usuario


def listar_usuarios() -> list:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, nombre, correo, rol, activo, fecha_creacion FROM usuarios ORDER BY nombre")
            return cur.fetchall()


def listar_soporte_activo() -> list:
    """Para llenar el combo de 'asignar a' - solo soporte/admin activos."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, nombre, correo FROM usuarios WHERE activo = TRUE ORDER BY nombre")
            return cur.fetchall()


def cambiar_estado_usuario(usuario_id: int, activo: bool) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE usuarios SET activo = %s WHERE id = %s", (activo, usuario_id))
        conn.commit()
