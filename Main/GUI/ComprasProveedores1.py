import tkinter as tk
from tkinter import messagebox
from Productos import *
from Proveedores import *
from PedidosProveedor import *


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Registro de Pedidos")
        self.geometry("400x300")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self, text="--- Registro de Ventas ---", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self, text="Compras a Proveedores", command=self.menu_compras_proveedor).pack(pady=5)
        tk.Button(self, text="Salir", command=self.quit).pack(pady=20)

    def menu_compras_proveedor(self):
        self.clear_window()
        tk.Label(self, text="--- Menu de compras a proveedores ---", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self, text="Realizar pedido de compra", command=self.pedido_proveedor).pack(pady=5)
        tk.Button(self, text="Validación de entregas", command=self.validacion_entregas).pack(pady=5)
        tk.Button(self, text="Registrar devoluciones", command=self.registrar_devoluciones).pack(pady=5)
        tk.Button(self, text="Generar historiales", command=self.menu_historiales).pack(pady=5)
        tk.Button(self, text="Volver", command=self.create_main_menu).pack(pady=5)

    def pedido_proveedor(self):
        self.clear_window()
        tk.Label(self, text="--- Registro de pedidos ---", font=("Helvetica", 16)).pack(pady=10)
        Proveedores.mostrar()

        tk.Label(self, text="Nombre del Proveedor:").pack(pady=5)
        entry_nombre_proveedor = tk.Entry(self)
        entry_nombre_proveedor.pack(pady=5)

        tk.Label(self, text="Código del Producto:").pack(pady=5)
        entry_nombre_producto = tk.Entry(self)
        entry_nombre_producto.pack(pady=5)

        tk.Label(self, text="Marca del Producto:").pack(pady=5)
        entry_marca_producto = tk.Entry(self)
        entry_marca_producto.pack(pady=5)

        tk.Label(self, text="Cantidad de Productos:").pack(pady=5)
        entry_cantidad_producto = tk.Entry(self)
        entry_cantidad_producto.pack(pady=5)

        def agregar_pedido():
            nombre_proveedor = entry_nombre_proveedor.get().strip()
            nombre_producto = entry_nombre_producto.get().strip()
            marca_producto = entry_marca_producto.get().strip()
            cantidad_producto = entry_cantidad_producto.get().strip()

            proveedor = Proveedores.validar_provedor(nombre_proveedor)
            if proveedor:
                producto = Producto.validar_codigo(nombre_producto)
                if producto:
                    producto_marca = Producto.validar_marca(marca_producto)
                    if producto_marca:
                        try:
                            cantidad_producto = int(cantidad_producto)
                            if cantidad_producto > 0:
                                pedido = PedidosProveedor(nombre_proveedor, nombre_producto, marca_producto,
                                                          cantidad_producto)
                                pedido.guardar()
                                messagebox.showinfo("Éxito", "Pedido agregado exitosamente.")
                            else:
                                messagebox.showerror("Error", "Cantidad de productos debe ser mayor a 0.")
                        except ValueError:
                            messagebox.showerror("Error", "Ingrese una cantidad válida.")
                    else:
                        messagebox.showerror("Error", "Marca de producto no registrada.")
                else:
                    messagebox.showerror("Error", "Código de producto no registrado.")
            else:
                messagebox.showerror("Error", "Nombre de proveedor no registrado.")

        tk.Button(self, text="Agregar pedido", command=agregar_pedido).pack(pady=20)
        tk.Button(self, text="Volver", command=self.menu_compras_proveedor).pack(pady=5)

    def validacion_entregas(self):
        messagebox.showinfo("Validación de entregas", "Funcionalidad en desarrollo.")

    def registrar_devoluciones(self):
        messagebox.showinfo("Registrar devoluciones", "Funcionalidad en desarrollo.")

    def menu_historiales(self):
        self.clear_window()
        tk.Label(self, text="--- Menu Historiales ---", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self, text="Historial de compras", command=self.historial_compras).pack(pady=5)
        tk.Button(self, text="Historial de compras por proveedor", command=self.historial_compras_por_proveedor).pack(
            pady=5)
        tk.Button(self, text="Volver", command=self.menu_compras_proveedor).pack(pady=5)

    def historial_compras(self):
        PedidosProveedor.mostrar_pedidos()

    def historial_compras_por_proveedor(self):
        messagebox.showinfo("Historial de compras por proveedor", "Funcionalidad en desarrollo.")

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
