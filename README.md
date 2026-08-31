# Gestión de Tickets de Soporte TI

CRUD de escritorio (Tkinter) para gestionar tickets de soporte, con base de datos
**compartida** en Supabase (PostgreSQL gratuito) para que todo el equipo del
bootcamp trabaje contra los mismos datos.

## Estructura del proyecto

```
├── main.py                       Punto de entrada: login → app principal
├── crear_admin.py                Script de un solo uso: crea la primera cuenta admin
├── schema.sql                    Tablas de la base de datos
│
├── core/                         Configuración y conexión a la base de datos
│   ├── config.py                 Lee las credenciales desde .env
│   └── conexion.py                get_connection() — usado por todos los repositorios
│
├── repositorios/                 Capa de acceso a datos (una tabla por archivo)
│   ├── usuarios.py                Login, alta/baja de soporte y admin
│   ├── tickets.py                 CRUD de tickets, folio automático, asignación
│   └── mensajes.py                Hilo de seguimiento de cada ticket
│
└── gui/                           Interfaz Tkinter
    ├── estilos.py                 Paleta oscura y catálogos (categorías, estados, etc.)
    ├── login.py                   Ventana de inicio de sesión
    ├── dialogo_nuevo_ticket.py    Ventana emergente para crear un ticket
    ├── tab_tickets.py             Pestaña de tickets (lista + detalle + seguimiento)
    ├── tab_usuarios.py            Pestaña de usuarios (solo admin)
    └── app.py                     Ventana principal, arma las pestañas según el rol
```

La `gui/` solo llama a los `repositorios/`, nunca ejecuta SQL directamente —
así si mañana cambian de PostgreSQL a otra base, solo se toca `core/` y
`repositorios/`, sin tocar ninguna pantalla.


## 1. Crear la base de datos compartida (solo una persona lo hace)

1. Ir a https://supabase.com → crear cuenta gratis → "New Project".
2. Elegir nombre, contraseña de base de datos (guárdala, la va a necesitar el equipo) y región.
3. Una vez creado, ir a **SQL Editor** → pegar el contenido de `schema.sql` → **Run**.
4. Ir a **Project Settings → Database → Connection pooling** y copiar:
   - Host
   - Port (usar el **6543**, el del *pooler*, para que soporte varias conexiones simultáneas del equipo)
   - Database name
   - User
5. Compartir con el equipo: host, puerto, usuario y la contraseña del proyecto .

## 2. Cada integrante del equipo 

```bash
git clone https://github.com/Jazar321/Tickets-soporte
cd ticket_crud
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

```

Editar `.env` y poner las credenciales que les compartieron:

```
DB_HOST=aws-0-us-east-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=postgres.xxxxxxxxxxxx
DB_PASSWORD=la_contraseña_del_proyecto
```

## 3. Crear el primer usuario administrador (solo una vez, cualquier integrante)

```bash
python crear_admin.py
```

Te pide nombre, correo y contraseña, y crea la primera cuenta con rol `admin`.
Con esa cuenta ya pueden entrar a la app y, desde la pestaña **Usuarios**, dar de
alta al resto del equipo (rol `soporte` o `admin`).

## 4. Ejecutar la app

```bash
python main.py
```

Pide correo y contraseña (login). Según el rol:

- **admin**: ve la pestaña "Tickets" y además "Usuarios" (alta/baja de soporte).
- **soporte**: ve la pestaña "Tickets", puede crear tickets, asignarlos, cambiar
  su estado y agregar mensajes de seguimiento. Puede filtrar "solo mis tickets asignados".

Cada ticket nace con un folio único (`TK-2026-00001`) y tiene un hilo de mensajes
donde cualquier persona de soporte puede agregar notas de seguimiento sin
sobreescribir lo que puso otro compañero — así queda un historial completo de
quién hizo qué y cuándo.

Todos verán y editarán los mismos tickets en tiempo real (al refrescar la lista).

