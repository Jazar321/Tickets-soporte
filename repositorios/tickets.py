"""CRUD de tickets: crear, listar, actualizar, asignar."""
import psycopg2.extras
from core.conexion import get_connection

CAMPOS_TICKET = [
    "nombre_usuario",
    "correo_electronico",
    "telefono_extension",
    "departamento_area",
    "categoria",
    "prioridad",
    "descripcion_problema",
    "posibles_causas",
    "satisfaccion_usuario",
    "estado",
]


def crear_ticket(datos: dict, creado_por_id: int) -> str:
    """Inserta el ticket, genera su número de seguimiento y devuelve ese número."""
    columnas = ", ".join(CAMPOS_TICKET)
    placeholders = ", ".join(["%s"] * len(CAMPOS_TICKET))
    valores = [datos.get(c, "") for c in CAMPOS_TICKET]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO tickets ({columnas}, creado_por) "
                f"VALUES ({placeholders}, %s) RETURNING id, fecha_creacion",
                valores + [creado_por_id],
            )
            ticket_id, fecha_creacion = cur.fetchone()
            numero = f"TK-{fecha_creacion.year}-{ticket_id:05d}"
            cur.execute("UPDATE tickets SET numero_seguimiento = %s WHERE id = %s", (numero, ticket_id))
        conn.commit()
    return numero


def listar_tickets(filtro_texto: str = "", filtro_estado: str = "", solo_asignado_a: int = None) -> list:
    query = """
        SELECT t.*, u.nombre AS asignado_nombre
        FROM tickets t
        LEFT JOIN usuarios u ON u.id = t.asignado_a
        WHERE 1=1
    """
    params = []

    if filtro_texto:
        query += " AND (t.nombre_usuario ILIKE %s OR t.numero_seguimiento ILIKE %s OR t.departamento_area ILIKE %s)"
        like = f"%{filtro_texto}%"
        params.extend([like, like, like])

    if filtro_estado and filtro_estado != "Todos":
        query += " AND t.estado = %s"
        params.append(filtro_estado)

    if solo_asignado_a:
        query += " AND t.asignado_a = %s"
        params.append(solo_asignado_a)

    query += " ORDER BY t.fecha_creacion DESC"

    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()


def obtener_ticket(ticket_id: int) -> dict:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT t.*, u.nombre AS asignado_nombre
                FROM tickets t
                LEFT JOIN usuarios u ON u.id = t.asignado_a
                WHERE t.id = %s
                """,
                (ticket_id,),
            )
            return cur.fetchone()


def actualizar_ticket(ticket_id: int, datos: dict) -> None:
    set_clause = ", ".join([f"{c} = %s" for c in CAMPOS_TICKET])
    valores = [datos.get(c, "") for c in CAMPOS_TICKET]
    valores.append(ticket_id)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE tickets SET {set_clause}, fecha_actualizacion = NOW() WHERE id = %s",
                valores,
            )
        conn.commit()


def eliminar_ticket(ticket_id: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tickets WHERE id = %s", (ticket_id,))
        conn.commit()


def asignar_ticket(ticket_id: int, asignado_a_id: int, asignado_por_id: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tickets SET asignado_a = %s, fecha_actualizacion = NOW() WHERE id = %s",
                (asignado_a_id, ticket_id),
            )
            cur.execute(
                "INSERT INTO ticket_asignaciones (ticket_id, asignado_a, asignado_por) VALUES (%s, %s, %s)",
                (ticket_id, asignado_a_id, asignado_por_id),
            )
        conn.commit()


def historial_asignaciones(ticket_id: int) -> list:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT a.fecha_asignacion, u1.nombre AS asignado_a_nombre, u2.nombre AS asignado_por_nombre
                FROM ticket_asignaciones a
                LEFT JOIN usuarios u1 ON u1.id = a.asignado_a
                LEFT JOIN usuarios u2 ON u2.id = a.asignado_por
                WHERE a.ticket_id = %s
                ORDER BY a.fecha_asignacion DESC
                """,
                (ticket_id,),
            )
            return cur.fetchall()
