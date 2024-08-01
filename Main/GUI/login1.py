from ComprasProveedores1 import *
from InventarioGUI import *
from Productos1 import *
from ProveedoresOp1 import *
from Ventas1 import *
from Main.VentaP import *

usuarios = [
    "admin",
    "admin"
]


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Tiendita")
        self.resizable(False, False)
        self.center_window(600, 400)
        self.create_login_screen()
        self.corte_realizado = False

    def center_window(self, width, height):
        # Obtener el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular las coordenadas x e y para centrar la ventana
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Establecer la geometría de la ventana
        self.geometry(f'{width}x{height}+{x}+{y}')


    def create_login_screen(self):
        self.clear_screen()
        self.overrideredirect(False)
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
        self.center_window(600, 400)
        self.resizable(False, False)
        self.overrideredirect(True)
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
        tk.Button(self, text="Salir",width=30, command=self.validar_corte_caja).pack(pady=5)

    def validar_corte_caja(self):
        if self.corte_realizado:
            Proveedores.escribir_archivo_csv_principal()
            Producto.escribir_archivo_csv_productos_principal()
            PedidosProveedor.escribir_archivo_csv_principal_compras()
            Ventas.escribir_ventas_historial_csv()
            self.destroy()
        else:
            messagebox.showerror("Error","Realizar corte de caja")

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
            if Producto.lista_productos:
                self.withdraw()  # Hide the main window
                menuC = ComprasProveedorApp(self)
                menuC.protocol("WM_DELETE_WINDOW", self.deiconify)  # Show main window on close
                menuC.mainloop()
            else:
                messagebox.showwarning("Advertencia", "Registre un producto.")
        else:
            messagebox.showwarning("Advertencia", "Registre un proveedor.")

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
