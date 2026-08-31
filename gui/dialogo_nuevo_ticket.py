"""Ventana emergente para dar de alta un ticket nuevo."""
import tkinter as tk
from tkinter import ttk, messagebox

from repositorios import tickets as tickets_repo
from gui.estilos import BG_PANEL, FIELD_BG, FG, CATEGORIAS, PRIORIDADES


class NuevoTicketDialog(tk.Toplevel):
    def __init__(self, parent, usuario_actual, on_creado):
        super().__init__(parent)
        self.title("Nuevo Ticket")
        self.configure(bg=BG_PANEL)
        self.geometry("480x560")
        self.usuario_actual = usuario_actual
        self.on_creado = on_creado

        campos = [
            ("Nombre del solicitante", "nombre_usuario", "entry"),
            ("Correo Electrónico", "correo_electronico", "entry"),
            ("Teléfono / Extensión", "telefono_extension", "entry"),
            ("Departamento / Área", "departamento_area", "entry"),
            ("Categoría", "categoria", "combo", CATEGORIAS),
            ("Prioridad", "prioridad", "combo", PRIORIDADES),
            ("Descripción del Problema", "descripcion_problema", "text"),
            ("Posibles Causas", "posibles_causas", "text"),
        ]
        self.widgets = {}
        for item in campos:
            label, key, tipo = item[0], item[1], item[2]
            ttk.Label(self, text=label, style="Panel.TLabel").pack(anchor="w", padx=15, pady=(8, 0))
            if tipo == "entry":
                w = ttk.Entry(self, width=45)
            elif tipo == "combo":
                w = ttk.Combobox(self, values=item[3], width=42, state="readonly")
            elif tipo == "text":
                w = tk.Text(self, width=45, height=4, bg=FIELD_BG, fg=FG, insertbackground=FG, borderwidth=0)
            w.pack(padx=15, fill="x")
            self.widgets[key] = w

        ttk.Button(self, text="Crear Ticket", command=self.crear).pack(pady=20)

    def crear(self):
        datos = {}
        for key, w in self.widgets.items():
            if isinstance(w, tk.Text):
                datos[key] = w.get("1.0", "end").strip()
            else:
                datos[key] = w.get().strip()
        if not datos["nombre_usuario"]:
            messagebox.showwarning("Falta información", "El nombre del solicitante es obligatorio.")
            return
        datos["satisfaccion_usuario"] = ""
        datos["estado"] = "Abierto"
        try:
            numero = tickets_repo.crear_ticket(datos, self.usuario_actual["id"])
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            return
        messagebox.showinfo("Ticket creado", f"Se creó el ticket {numero}")
        self.on_creado()
        self.destroy()
