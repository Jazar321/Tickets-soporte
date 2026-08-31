"""Pestaña 'Usuarios' (solo admin): alta y baja de gente de soporte."""
from tkinter import ttk, messagebox

from repositorios import usuarios as usuarios_repo


class TabUsuarios(ttk.Frame):
    def __init__(self, parent, on_cambio=None):
        super().__init__(parent)
        self.on_cambio = on_cambio  # callback para refrescar el combo de asignación en Tickets
        self._construir_ui()
        self.refrescar_usuarios()

    def _construir_ui(self):
        cont = ttk.Frame(self)
        cont.pack(fill="both", expand=True)

        izquierda = ttk.Frame(cont, style="Panel.TFrame")
        izquierda.pack(side="left", fill="y", padx=(0, 10), ipadx=10, ipady=10)

        ttk.Label(izquierda, text="Nuevo usuario de soporte", style="Seccion.TLabel").pack(anchor="w", padx=10, pady=(10, 6))
        ttk.Label(izquierda, text="Nombre", style="Panel.TLabel").pack(anchor="w", padx=10)
        self.u_nombre = ttk.Entry(izquierda, width=30)
        self.u_nombre.pack(padx=10, pady=(0, 6))
        ttk.Label(izquierda, text="Correo", style="Panel.TLabel").pack(anchor="w", padx=10)
        self.u_correo = ttk.Entry(izquierda, width=30)
        self.u_correo.pack(padx=10, pady=(0, 6))
        ttk.Label(izquierda, text="Contraseña temporal", style="Panel.TLabel").pack(anchor="w", padx=10)
        self.u_password = ttk.Entry(izquierda, width=30, show="•")
        self.u_password.pack(padx=10, pady=(0, 6))
        ttk.Label(izquierda, text="Rol", style="Panel.TLabel").pack(anchor="w", padx=10)
        self.u_rol = ttk.Combobox(izquierda, values=["soporte", "admin"], width=27, state="readonly")
        self.u_rol.set("soporte")
        self.u_rol.pack(padx=10, pady=(0, 10))
        ttk.Button(izquierda, text="Crear usuario", command=self.crear_usuario_nuevo).pack(padx=10, fill="x")

        derecha = ttk.Frame(cont)
        derecha.pack(side="left", fill="both", expand=True)

        columnas = ("nombre", "correo", "rol", "activo")
        self.tree_usuarios = ttk.Treeview(derecha, columns=columnas, show="headings", selectmode="browse")
        for col, titulo, ancho in [("nombre", "Nombre", 160), ("correo", "Correo", 200),
                                     ("rol", "Rol", 80), ("activo", "Activo", 60)]:
            self.tree_usuarios.heading(col, text=titulo)
            self.tree_usuarios.column(col, width=ancho, anchor="w")
        self.tree_usuarios.pack(fill="both", expand=True)

        botones = ttk.Frame(derecha)
        botones.pack(pady=8)
        ttk.Button(botones, text="Activar", command=lambda: self.cambiar_activo_usuario(True)).pack(side="left", padx=5)
        ttk.Button(botones, text="Dar de baja", command=lambda: self.cambiar_activo_usuario(False)).pack(side="left", padx=5)

    def refrescar_usuarios(self):
        for fila in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(fila)
        try:
            usuarios = usuarios_repo.listar_usuarios()
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            return
        for u in usuarios:
            self.tree_usuarios.insert("", "end", iid=u["id"], values=(
                u["nombre"], u["correo"], u["rol"], "Sí" if u["activo"] else "No"
            ))

    def crear_usuario_nuevo(self):
        nombre = self.u_nombre.get().strip()
        correo = self.u_correo.get().strip()
        password = self.u_password.get()
        rol = self.u_rol.get()
        if not (nombre and correo and password):
            messagebox.showwarning("Faltan datos", "Llena nombre, correo y contraseña.")
            return
        try:
            usuarios_repo.crear_usuario(nombre, correo, password, rol)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self.u_nombre.delete(0, "end")
        self.u_correo.delete(0, "end")
        self.u_password.delete(0, "end")
        self.refrescar_usuarios()
        if self.on_cambio:
            self.on_cambio()

    def cambiar_activo_usuario(self, activo: bool):
        seleccion = self.tree_usuarios.selection()
        if not seleccion:
            messagebox.showwarning("Nada seleccionado", "Selecciona un usuario de la lista.")
            return
        usuario_id = int(seleccion[0])
        try:
            usuarios_repo.cambiar_estado_usuario(usuario_id, activo)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self.refrescar_usuarios()
        if self.on_cambio:
            self.on_cambio()
