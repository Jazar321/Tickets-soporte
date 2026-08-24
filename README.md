# Gestión de Tickets de Soporte TI

CRUD de escritorio (Tkinter) para gestionar tickets de soporte, con base de datos
**compartida** en Supabase (PostgreSQL gratuito) para que todo el equipo del
bootcamp trabaje contra los mismos datos.

## 1. Crear la base de datos compartida (solo una persona lo hace)

1. Ir a https://supabase.com → crear cuenta gratis → "New Project".
2. Elegir nombre, contraseña de base de datos (guárdala, la va a necesitar el equipo) y región.
3. Una vez creado, ir a **SQL Editor** → pegar el contenido de `schema.sql` → **Run**.
4. Ir a **Project Settings → Database → Connection pooling** y copiar:
   - Host
   - Port (usar el **6543**, el del *pooler*, para que soporte varias conexiones simultáneas del equipo)
   - Database name
   - User
5. Compartir con el equipo: host, puerto, usuario y la contraseña del proyecto (por un medio privado, no lo subas a GitHub).

## 2. Cada integrante del equipo (en su propia laptop)

```bash
git clone <url-del-repo>
cd ticket_crud
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt

copy .env.example .env     # Windows
# cp .env.example .env      # Mac/Linux
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

## Notas

- El archivo `.env` **nunca** se sube a GitHub (ya está en `.gitignore`); cada quien
  tiene el suyo local con las mismas credenciales.
- El tier gratuito de Supabase da 500 MB de base de datos, más que suficiente para
  un proyecto de bootcamp.
- Si en unos meses el proyecto pausa el uso por 7+ días, Supabase pausa el proyecto
  gratuito automáticamente; basta con reactivarlo desde el dashboard cuando lo necesiten de nuevo.
# Tickets-soporte
