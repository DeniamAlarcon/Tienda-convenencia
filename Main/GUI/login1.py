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
        self.title("Tiendita")
        self.geometry("400x340")
        self.resizable(False, False)
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self, text="---Inicio de sesión---").pack(pady=15)

        tk.Label(self, text="Usuario:").pack()
        self.usuario_entry = tk.Entry(self,width=30,highlightcolor="red")
        self.usuario_entry.pack(pady=15)

        tk.Label(self, text="Contraseña:").pack()
        self.contraseña_entry = tk.Entry(self, show="*",width=30)
        self.contraseña_entry.pack(pady=15)

        tk.Button(self, text="Ingresar",width=30, command=self.solicitar_credenciales).pack(pady=15)

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
        self.geometry("400x340")
        self.resizable(False, False)
        Proveedores.leer_archivo()
        Producto.leer_archivo()
        PedidosProveedor.leer_archivo()
        Ventas.leer_ventas_historial_csv()

        tk.Label(self, text="--- Menu principal ---").pack(pady=5)
        tk.Button(self, text="Proveedores", width=30,command=self.menuProveedores).pack(pady=5)
        tk.Button(self, text="Productos", width=30,command=self.menuProductos).pack(pady=5)
        tk.Button(self, text="Compras", width=30,command=self.menu_compras).pack(pady=5)
        tk.Button(self, text="Inventarios", width=30,command=self.menuInventarios).pack(pady=5)
        tk.Button(self, text="Ventas",width=30, command=self.menuVentas).pack(pady=5)
        tk.Button(self, text="Salir",width=30, command=self.quit).pack(pady=5)

    def menuProveedores(self):
        self.withdraw()  # Hide the main window
        menuProv = ProveedorApp(self)
        menuProv.protocol("WM_DELETE_WINDOW", self.deiconify)  # Show main window on close
        menuProv.mainloop()

    def menuProductos(self):
        if Proveedores.proveedores:
            self.withdraw()  # Hide the main window
            menuPro = ProductosApp(self)
            menuPro.protocol("WM_DELETE_WINDOW", self.deiconify)  # Show main window on close
            menuPro.mainloop()
        else:
            messagebox.showwarning("Advertencia","Registre un proveedor")

    def menuVentas(self):
        if Proveedores.proveedores:
            if Producto.lista_productos:
                self.withdraw()  # Hide the main window
                menuV = VentasApp(self)
                menuV.protocol("WM_DELETE_WINDOW", self.deiconify)  # Show main window on close
                menuV.mainloop()
            else:
                messagebox.showwarning("Advertencia", "Registre un producto.")
        else:
            messagebox.showwarning("Advertencia", "Registre un proveedor.")

    def menuInventarios(self):
        if Proveedores.proveedores:
            if Producto.lista_productos:
                self.withdraw()  # Hide the main window
                menuProv = InventarioApp(self)
                menuProv.protocol("WM_DELETE_WINDOW", self.deiconify)  # Show main window on close
                menuProv.mainloop()
            else:
                messagebox.showwarning("Advertencia", "Registre un producto.")
        else:
            messagebox.showwarning("Advertencia", "Registre un proveedor.")

    def menu_compras(self):
        if Proveedores.mostrar():
            self.withdraw()  # Hide the main window
            menuC = ComprasProveedorApp(self)
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
