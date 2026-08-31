"""Paleta y configuración del tema oscuro, compartida por toda la GUI."""
from tkinter import ttk

BG = "#1e1e2e"
BG_PANEL = "#282838"
FG = "#e0e0e0"
ACCENT = "#3b82f6"
FIELD_BG = "#32324a"
BTN_BG = "#3b3b55"
OK = "#22c55e"

CATEGORIAS = ["Hardware", "Software", "Redes", "Seguridad", "Otros (especificar)"]
PRIORIDADES = ["Baja", "Media", "Alta", "Crítica"]
SATISFACCION = ["", "Muy Satisfecho", "Satisfecho", "Neutral", "Insatisfecho", "Muy Insatisfecho"]
ESTADOS = ["Abierto", "Asignado", "En Proceso", "Resuelto", "Cerrado", "Cancelado"]


def aplicar_estilo_oscuro(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TFrame", background=BG)
    style.configure("Panel.TFrame", background=BG_PANEL)
    style.configure("TLabel", background=BG, foreground=FG, font=("Segoe UI", 9))
    style.configure("Panel.TLabel", background=BG_PANEL, foreground=FG, font=("Segoe UI", 9))
    style.configure("Titulo.TLabel", background=BG, foreground=FG, font=("Segoe UI", 15, "bold"))
    style.configure("Seccion.TLabel", background=BG_PANEL, foreground=ACCENT, font=("Segoe UI", 10, "bold"))
    style.configure("Numero.TLabel", background=BG_PANEL, foreground=OK, font=("Segoe UI", 13, "bold"))

    style.configure("TEntry", fieldbackground=FIELD_BG, foreground=FG, insertcolor=FG, borderwidth=0)

    style.configure("TCombobox", fieldbackground=FIELD_BG, background=FIELD_BG, foreground=FG)
    style.map("TCombobox",
              fieldbackground=[("readonly", FIELD_BG), ("!focus", FIELD_BG), ("focus", FIELD_BG)],
              foreground=[("readonly", FG), ("!focus", FG), ("focus", FG)],
              selectbackground=[("readonly", FIELD_BG)],
              selectforeground=[("readonly", FG)])
    root.option_add("*TCombobox*Listbox.background", FIELD_BG)
    root.option_add("*TCombobox*Listbox.foreground", FG)

    style.configure("TButton", background=BTN_BG, foreground=FG, padding=6, borderwidth=0, font=("Segoe UI", 9, "bold"))
    style.map("TButton", background=[("active", ACCENT)])

    style.configure("Treeview", background=FIELD_BG, fieldbackground=FIELD_BG, foreground=FG,
                     rowheight=26, borderwidth=0, font=("Segoe UI", 9))
    style.configure("Treeview.Heading", background=BTN_BG, foreground=FG, font=("Segoe UI", 9, "bold"))
    style.map("Treeview", background=[("selected", ACCENT)])

    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", background=BTN_BG, foreground=FG, padding=(14, 6))
    style.map("TNotebook.Tab", background=[("selected", ACCENT)])
