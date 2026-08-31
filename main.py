"""Punto de entrada: muestra el login y, si es exitoso, abre la app principal."""
from gui.login import LoginWindow
from gui.app import TicketApp

if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()
    if login.usuario:
        app = TicketApp(login.usuario)
        app.mainloop()
