"""Ventana principal: arma el Notebook con las pestañas según el rol del usuario."""
import tkinter as tk
from tkinter import ttk

from gui.estilos import BG, aplicar_estilo_oscuro
from gui.tab_tickets import TabTickets
from gui.tab_usuarios import TabUsuarios


class TicketApp(tk.Tk):
    def __init__(self, usuario_actual):
        super().__init__()
        self.usuario_actual = usuario_actual

        self.title(f"Gestión de Tickets de Soporte TI — {usuario_actual['nombre']} ({usuario_actual['rol']})")
        self.geometry("1250x720")
        self.configure(bg=BG)
        aplicar_estilo_oscuro(self)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_tickets = TabTickets(notebook, usuario_actual)
        notebook.add(self.tab_tickets, text="Tickets")

        if usuario_actual["rol"] == "admin":
            self.tab_usuarios = TabUsuarios(notebook, on_cambio=self.tab_tickets.refrescar_soporte)
            notebook.add(self.tab_usuarios, text="Usuarios")
