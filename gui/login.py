"""Ventana de inicio de sesión — punto de entrada antes de abrir la app principal."""
import tkinter as tk
from tkinter import ttk, messagebox

from repositorios import usuarios as usuarios_repo
from gui.estilos import BG, aplicar_estilo_oscuro


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Iniciar sesión - Soporte TI")
        self.geometry("360x300")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.usuario = None
        aplicar_estilo_oscuro(self)

        ttk.Label(self, text="Soporte TI", style="Titulo.TLabel").pack(pady=(30, 20))

        frame = ttk.Frame(self)
        frame.pack(padx=30, fill="x")

        ttk.Label(frame, text="Correo").pack(anchor="w")
        self.e_correo = ttk.Entry(frame, width=32)
        self.e_correo.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Contraseña").pack(anchor="w")
        self.e_password = ttk.Entry(frame, width=32, show="•")
        self.e_password.pack(fill="x", pady=(0, 20))
        self.e_password.bind("<Return>", lambda e: self.intentar_login())

        ttk.Button(frame, text="Iniciar sesión", command=self.intentar_login).pack(fill="x")

    def intentar_login(self):
        correo = self.e_correo.get().strip()
        password = self.e_password.get()
        if not correo or not password:
            messagebox.showwarning("Faltan datos", "Escribe correo y contraseña.")
            return
        try:
            usuario = usuarios_repo.verificar_login(correo, password)
        except Exception as e:
            messagebox.showerror("Error de conexión", str(e))
            return
        if not usuario:
            messagebox.showerror("Acceso denegado", "Correo, contraseña incorrectos, o cuenta inactiva.")
            return
        self.usuario = usuario
        self.destroy()
