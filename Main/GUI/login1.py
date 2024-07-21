import tkinter as tk
from tkinter import messagebox
from Productos1 import *
from InventarioGUI import *
from ProveedoresOp1 import *
from Main.ComprasProveedores import *
from Ventas1 import *
from ComprasProveedores1 import *
from Main.Productos import *
import re

usuarios = [
    "admin",
    "admin"
]

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión")
        self.geometry("500x500")
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self, text="---Inicio de sesión---").pack()

        tk.Label(self, text="Usuario:").pack()
        self.usuario_entry = tk.Entry(self)
        self.usuario_entry.pack()

        tk.Label(self, text="Contraseña:").pack()
        self.contraseña_entry = tk.Entry(self, show="*")
        self.contraseña_entry.pack()

        tk.Button(self, text="Ingresar", command=self.solicitar_credenciales).pack()

    def solicitar_credenciales(self):
        usuario = self.usuario_entry.get()
        contraseña = self.contraseña_entry.get()

        if not usuario or not contraseña:
            messagebox.showwarning("Advertencia", "Ingrese los campos solicitados.")
        elif usuarios[0] == usuario and usuarios[1] == contraseña:
            self.create_menu_screen()
        else:
            messagebox.showerror("Error", "Usuario o contraseña no válidos.")

    def create_menu_screen(self):
        self.clear_screen()
        Proveedores.leer_archivo()
        Producto.leer_archivo()

        tk.Label(self, text="--- Menu principal ---").pack()
        tk.Button(self, text="Proveedores", command=self.menuProveedores).pack()
        tk.Button(self, text="Productos", command=self.menuProductos).pack()
        tk.Button(self, text="Compras", command=self.menu_compras).pack()
        tk.Button(self, text="Inventarios", command=self.menuInventarios).pack()
        tk.Button(self, text="Ventas", command=self.menuVentas).pack()
        tk.Button(self, text="Salir", command=self.quit).pack()

    def menuProveedores(self):
        self.withdraw()  # Hide the main window
        menuProv = ProveedorApp()
        menuProv.protocol("WM_DELETE_WINDOW", self.deiconify)  # Show main window on close
        menuProv.mainloop()
    def menuProductos(self):
        self.withdraw()  # Hide the main window
        menuPro = ProductosApp()
        menuPro.protocol("WM_DELETE_WINDOW", self.deiconify)  # Show main window on close
        menuPro.mainloop()

    def menuVentas(self):
        self.withdraw()  # Hide the main window
        menuV = VentasApp()
        menuV.protocol("WM_DELETE_WINDOW", self.deiconify)  # Show main window on close
        menuV.mainloop()

    def menuInventarios(self):
        self.withdraw()  # Hide the main window
        menuProv = InventarioApp()
        menuProv.protocol("WM_DELETE_WINDOW", self.deiconify)  # Show main window on close
        menuProv.mainloop()

    def menu_compras(self):
        if Proveedores.mostrar():
            self.withdraw()  # Hide the main window
            menuC = ComprasProveedorApp()
            menuC.protocol("WM_DELETE_WINDOW", self.deiconify)  # Show main window on close
            menuC.mainloop()
        else:
            messagebox.showwarning("Advertencia", "Registre un proveedor.")

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
