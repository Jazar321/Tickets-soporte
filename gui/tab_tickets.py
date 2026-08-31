"""Pestaña 'Tickets': lista, detalle, asignación y seguimiento."""
import tkinter as tk
from tkinter import ttk, messagebox

from repositorios import tickets as tickets_repo
from repositorios import usuarios as usuarios_repo
from repositorios import mensajes as mensajes_repo
from gui.estilos import BG_PANEL, FIELD_BG, FG, CATEGORIAS, PRIORIDADES, SATISFACCION, ESTADOS
from gui.dialogo_nuevo_ticket import NuevoTicketDialog


class TabTickets(ttk.Frame):
    def __init__(self, parent, usuario_actual):
        super().__init__(parent)
        self.usuario_actual = usuario_actual
        self.ticket_actual = None
        self.soporte_disponible = []

        self._construir_ui()
        self.refrescar_soporte()
        self.refrescar_lista()

    # ------------------------------------------------------------------
    def _construir_ui(self):
        cont = ttk.Frame(self)
        cont.pack(fill="both", expand=True)

        izquierda = ttk.Frame(cont)
        izquierda.pack(side="left", fill="y", padx=(0, 10))

        ttk.Button(izquierda, text="+ Nuevo Ticket", command=self.abrir_nuevo_ticket).pack(fill="x", pady=(0, 8))

        filtros = ttk.Frame(izquierda)
        filtros.pack(fill="x", pady=(0, 8))
        self.buscar_entry = ttk.Entry(filtros, width=22)
        self.buscar_entry.pack(side="left", padx=(0, 5))
        self.filtro_estado = ttk.Combobox(filtros, values=["Todos"] + ESTADOS, width=12, state="readonly")
        self.filtro_estado.set("Todos")
        self.filtro_estado.pack(side="left", padx=(0, 5))
        ttk.Button(filtros, text="Buscar", command=self.refrescar_lista).pack(side="left")

        if self.usuario_actual["rol"] == "soporte":
            self.solo_mios = tk.BooleanVar(value=False)
            ttk.Checkbutton(izquierda, text="Solo mis tickets asignados", variable=self.solo_mios,
                             command=self.refrescar_lista).pack(anchor="w", pady=(0, 5))
        else:
            self.solo_mios = None

        columnas = ("numero", "nombre", "categoria", "prioridad", "estado", "asignado")
        self.tree = ttk.Treeview(izquierda, columns=columnas, show="headings", selectmode="browse", height=25)
        titulos = {"numero": "Folio", "nombre": "Solicitante", "categoria": "Categoría",
                   "prioridad": "Prioridad", "estado": "Estado", "asignado": "Asignado a"}
        anchos = {"numero": 100, "nombre": 130, "categoria": 90, "prioridad": 70, "estado": 90, "asignado": 110}
        for col in columnas:
            self.tree.heading(col, text=titulos[col])
            self.tree.column(col, width=anchos[col], anchor="w")
        self.tree.pack(fill="y", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.cargar_ticket_seleccionado)

        self.panel_detalle = ttk.Frame(cont, style="Panel.TFrame")
        self.panel_detalle.pack(side="left", fill="both", expand=True, ipadx=10, ipady=10)
        self._construir_panel_vacio()

    def _limpiar_panel_detalle(self):
        for w in self.panel_detalle.winfo_children():
            w.destroy()

    def _construir_panel_vacio(self):
        self._limpiar_panel_detalle()
        ttk.Label(self.panel_detalle, text="Selecciona un ticket de la lista, o crea uno nuevo.",
                  style="Panel.TLabel").pack(padx=20, pady=20)

    # ------------------------------------------------------------------
    def abrir_nuevo_ticket(self):
        NuevoTicketDialog(self, self.usuario_actual, on_creado=self.refrescar_lista)

    def refrescar_lista(self):
        for fila in self.tree.get_children():
            self.tree.delete(fila)
        filtro_asignado = None
        if self.solo_mios is not None and self.solo_mios.get():
            filtro_asignado = self.usuario_actual["id"]
        try:
            tickets = tickets_repo.listar_tickets(self.buscar_entry.get().strip(), self.filtro_estado.get(), filtro_asignado)
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            return
        for t in tickets:
            self.tree.insert("", "end", iid=t["id"], values=(
                t["numero_seguimiento"], t["nombre_usuario"], t["categoria"],
                t["prioridad"], t["estado"], t["asignado_nombre"] or "Sin asignar"
            ))

    def refrescar_soporte(self):
        try:
            self.soporte_disponible = usuarios_repo.listar_soporte_activo()
        except Exception:
            self.soporte_disponible = []

    def cargar_ticket_seleccionado(self, event=None):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        ticket_id = int(seleccion[0])
        t = tickets_repo.obtener_ticket(ticket_id)
        if not t:
            return
        self.ticket_actual = t
        self._dibujar_detalle_ticket(t)

    def _dibujar_detalle_ticket(self, t):
        self._limpiar_panel_detalle()
        p = self.panel_detalle

        ttk.Label(p, text=t["numero_seguimiento"], style="Numero.TLabel").pack(anchor="w", padx=15, pady=(10, 5))

        info = ttk.Frame(p, style="Panel.TFrame")
        info.pack(fill="x", padx=15)
        datos_ro = [
            ("Solicitante", t["nombre_usuario"]),
            ("Correo", t["correo_electronico"] or "-"),
            ("Teléfono/Ext.", t["telefono_extension"] or "-"),
            ("Departamento", t["departamento_area"] or "-"),
        ]
        for i, (label, valor) in enumerate(datos_ro):
            ttk.Label(info, text=f"{label}:", style="Panel.TLabel").grid(row=i, column=0, sticky="w", pady=1)
            ttk.Label(info, text=valor, style="Panel.TLabel").grid(row=i, column=1, sticky="w", padx=(8, 0), pady=1)

        ttk.Label(p, text="Descripción del Problema", style="Seccion.TLabel").pack(anchor="w", padx=15, pady=(12, 2))
        ttk.Label(p, text=t["descripcion_problema"] or "-", style="Panel.TLabel", wraplength=550,
                  justify="left").pack(anchor="w", padx=15)

        ttk.Label(p, text="Posibles Causas", style="Seccion.TLabel").pack(anchor="w", padx=15, pady=(12, 2))
        self.det_causas = tk.Text(p, width=65, height=3, bg=FIELD_BG, fg=FG, insertbackground=FG, borderwidth=0)
        self.det_causas.insert("1.0", t["posibles_causas"] or "")
        self.det_causas.pack(padx=15, fill="x")

        fila = ttk.Frame(p, style="Panel.TFrame")
        fila.pack(fill="x", padx=15, pady=(12, 0))

        ttk.Label(fila, text="Categoría", style="Panel.TLabel").grid(row=0, column=0, sticky="w")
        self.det_categoria = ttk.Combobox(fila, values=CATEGORIAS, width=16, state="readonly")
        self.det_categoria.set(t["categoria"] or "")
        self.det_categoria.grid(row=1, column=0, padx=(0, 10))

        ttk.Label(fila, text="Prioridad", style="Panel.TLabel").grid(row=0, column=1, sticky="w")
        self.det_prioridad = ttk.Combobox(fila, values=PRIORIDADES, width=10, state="readonly")
        self.det_prioridad.set(t["prioridad"] or "")
        self.det_prioridad.grid(row=1, column=1, padx=(0, 10))

        ttk.Label(fila, text="Estado", style="Panel.TLabel").grid(row=0, column=2, sticky="w")
        self.det_estado = ttk.Combobox(fila, values=ESTADOS, width=12, state="readonly")
        self.det_estado.set(t["estado"] or "")
        self.det_estado.grid(row=1, column=2, padx=(0, 10))

        ttk.Label(fila, text="Satisfacción (al cerrar)", style="Panel.TLabel").grid(row=0, column=3, sticky="w")
        self.det_satisfaccion = ttk.Combobox(fila, values=SATISFACCION, width=16, state="readonly")
        self.det_satisfaccion.set(t["satisfaccion_usuario"] or "")
        self.det_satisfaccion.grid(row=1, column=3)

        fila2 = ttk.Frame(p, style="Panel.TFrame")
        fila2.pack(fill="x", padx=15, pady=(12, 0))
        ttk.Label(fila2, text=f"Asignado a: {t['asignado_nombre'] or 'Sin asignar'}",
                  style="Panel.TLabel").pack(side="left")
        nombres_soporte = [f"{u['nombre']} ({u['correo']})" for u in self.soporte_disponible]
        self.det_asignar = ttk.Combobox(fila2, values=nombres_soporte, width=28, state="readonly")
        self.det_asignar.pack(side="left", padx=10)
        ttk.Button(fila2, text="Asignar", command=self.asignar_ticket_actual).pack(side="left")

        ttk.Button(p, text="Guardar cambios", command=self.guardar_ticket_actual).pack(pady=12)

        ttk.Label(p, text="Seguimiento (mensajes del equipo)", style="Seccion.TLabel").pack(anchor="w", padx=15, pady=(6, 2))
        self.frame_mensajes = tk.Text(p, width=68, height=8, bg="#1c1c2a", fg=FG, borderwidth=0, state="disabled")
        self.frame_mensajes.pack(padx=15, fill="x")
        self._cargar_mensajes(t["id"])

        fila_msg = ttk.Frame(p, style="Panel.TFrame")
        fila_msg.pack(fill="x", padx=15, pady=(6, 10))
        self.nuevo_mensaje = ttk.Entry(fila_msg, width=55)
        self.nuevo_mensaje.pack(side="left", padx=(0, 8))
        self.nuevo_mensaje.bind("<Return>", lambda e: self.agregar_mensaje_actual())
        ttk.Button(fila_msg, text="Agregar mensaje", command=self.agregar_mensaje_actual).pack(side="left")

    def _cargar_mensajes(self, ticket_id):
        try:
            mensajes = mensajes_repo.listar_mensajes(ticket_id)
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            return
        self.frame_mensajes.config(state="normal")
        self.frame_mensajes.delete("1.0", "end")
        if not mensajes:
            self.frame_mensajes.insert("end", "Sin mensajes todavía.")
        for m in mensajes:
            fecha = m["fecha_creacion"].strftime("%Y-%m-%d %H:%M")
            self.frame_mensajes.insert("end", f"[{fecha}] {m['autor_nombre']}:\n{m['mensaje']}\n\n")
        self.frame_mensajes.config(state="disabled")

    def guardar_ticket_actual(self):
        if not self.ticket_actual:
            return
        datos = {
            "nombre_usuario": self.ticket_actual["nombre_usuario"],
            "correo_electronico": self.ticket_actual["correo_electronico"],
            "telefono_extension": self.ticket_actual["telefono_extension"],
            "departamento_area": self.ticket_actual["departamento_area"],
            "categoria": self.det_categoria.get(),
            "prioridad": self.det_prioridad.get(),
            "descripcion_problema": self.ticket_actual["descripcion_problema"],
            "posibles_causas": self.det_causas.get("1.0", "end").strip(),
            "satisfaccion_usuario": self.det_satisfaccion.get(),
            "estado": self.det_estado.get(),
        }
        try:
            tickets_repo.actualizar_ticket(self.ticket_actual["id"], datos)
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            return
        messagebox.showinfo("Guardado", "Cambios guardados.")
        self.refrescar_lista()

    def asignar_ticket_actual(self):
        if not self.ticket_actual or not self.det_asignar.get():
            return
        idx = self.det_asignar.current()
        usuario_id = self.soporte_disponible[idx]["id"]
        try:
            tickets_repo.asignar_ticket(self.ticket_actual["id"], usuario_id, self.usuario_actual["id"])
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            return
        self.refrescar_lista()
        self.cargar_ticket_seleccionado()

    def agregar_mensaje_actual(self):
        if not self.ticket_actual:
            return
        texto = self.nuevo_mensaje.get().strip()
        if not texto:
            return
        try:
            mensajes_repo.agregar_mensaje(self.ticket_actual["id"], self.usuario_actual["id"], texto)
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            return
        self.nuevo_mensaje.delete(0, "end")
        self._cargar_mensajes(self.ticket_actual["id"])
