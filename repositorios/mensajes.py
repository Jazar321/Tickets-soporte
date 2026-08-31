"""Hilo de seguimiento de cada ticket (mensajes entre agentes)."""
import psycopg2.extras
from core.conexion import get_connection


def agregar_mensaje(ticket_id: int, autor_id: int, mensaje: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO ticket_mensajes (ticket_id, autor_id, mensaje) VALUES (%s, %s, %s)",
                (ticket_id, autor_id, mensaje),
            )
            cur.execute("UPDATE tickets SET fecha_actualizacion = NOW() WHERE id = %s", (ticket_id,))
        conn.commit()


def listar_mensajes(ticket_id: int) -> list:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT m.*, u.nombre AS autor_nombre
                FROM ticket_mensajes m
                LEFT JOIN usuarios u ON u.id = m.autor_id
                WHERE m.ticket_id = %s
                ORDER BY m.fecha_creacion ASC
                """,
                (ticket_id,),
            )
            return cur.fetchall()
