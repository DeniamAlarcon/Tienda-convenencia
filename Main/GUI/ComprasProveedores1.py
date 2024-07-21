import tkinter as tk
from tkinter import messagebox
from Main.PedidosProveedor import *
from Main.VentasMain import *

class ComprasProveedorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Compras a Proveedores")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.clear_frame()
        tk.Label(self, text="--- Menú de Compras a Proveedores ---", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Realizar pedido de compra", width=30, command=self.pedido_proveedor).pack(pady=5)
        tk.Button(self, text="Validación de entregas", width=30, command=self.validacion_entregas).pack(pady=5)
        tk.Button(self, text="Registrar devoluciones", width=30, command=self.registrar_devoluciones).pack(pady=5)
        tk.Button(self, text="Generar Historiales de compra", width=30, command=self.generar_historiales_compra).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.destroy).pack(pady=20)

    def pedido_proveedor(self):
        self.clear_frame()
        tk.Label(self, text="Registro de pedidos", font=("Arial", 16)).pack(pady=10)

        Proveedores.mostrar()
        tk.Label(self, text="Nombre del proveedor").pack()
        self.proveedor_entry = tk.Entry(self)
        self.proveedor_entry.pack()

        tk.Label(self, text="Nombre del producto").pack()
        self.producto_entry = tk.Entry(self)
        self.producto_entry.pack()

        tk.Label(self, text="Marca del producto").pack()
        self.marca_entry = tk.Entry(self)
        self.marca_entry.pack()

        tk.Label(self, text="Cantidad de productos").pack()
        self.cantidad_entry = tk.Entry(self)
        self.cantidad_entry.pack()

        tk.Button(self, text="Agregar pedido", command=self.procesar_pedido_proveedor).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_pedido_proveedor(self):
        nombre_proveedor = self.proveedor_entry.get()
        nombre_producto = self.producto_entry.get()
        marca_producto = self.marca_entry.get()
        cantidad_producto = self.cantidad_entry.get()

        if not nombre_proveedor or not nombre_producto or not marca_producto or not cantidad_producto:
            messagebox.showerror("Error", "Favor de llenar todos los campos")
            return

        proveedor = Proveedores.validar_provedor(nombre_proveedor)
        if not proveedor:
            messagebox.showerror("Error", "Proveedor no registrado")
            return

        if not Producto.validar_nombre(nombre_producto):
            messagebox.showerror("Error", "Producto no registrado")
            return

        if not Producto.validar_marca(marca_producto):
            messagebox.showerror("Error", "Marca de producto no registrada")
            return

        if not cantidad_producto.isdigit() or int(cantidad_producto) <= 0:
            messagebox.showerror("Error", "Cantidad de productos inválida")
            return

        precio = VentasMain.total_venta_actual(nombre_producto, int(cantidad_producto))
        pedido = PedidosProveedor(nombre_proveedor, nombre_producto, marca_producto, cantidad_producto, precio)
        pedido.guardar()

        messagebox.showinfo("Éxito", "Pedido registrado correctamente")
        self.create_widgets()

    def validacion_entregas(self):
        self.clear_frame()
        tk.Label(self, text="Validación de Entregas", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="ID del pedido").pack()
        self.id_pedido_entry = tk.Entry(self)
        self.id_pedido_entry.pack()

        tk.Label(self, text="Cantidad de productos").pack()
        self.cantidad_entregas_entry = tk.Entry(self)
        self.cantidad_entregas_entry.pack()

        tk.Button(self, text="Validar entrega", command=self.procesar_validacion_entrega).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_validacion_entrega(self):
        id_pedido = self.id_pedido_entry.get()
        cantidad = self.cantidad_entregas_entry.get()

        if not id_pedido or not cantidad:
            messagebox.showerror("Error", "Favor de llenar todos los campos")
            return

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        try:
            PedidosProveedor.pedidos_proveedorID(id_pedido, int(cantidad))
            messagebox.showinfo("Éxito", "Entrega validada correctamente")
        except ValueError:
            messagebox.showerror("Error", "Ingrese datos correctos")

        self.create_widgets()

    def registrar_devoluciones(self):
        self.clear_frame()
        tk.Label(self, text="Registro de Devoluciones", font=("Arial", 16)).pack(pady=10)

        Inventario.informeStockC()
        tk.Label(self, text="Producto para la devolución").pack()
        self.producto_devolucion_entry = tk.Entry(self)
        self.producto_devolucion_entry.pack()

        tk.Label(self, text="Cantidad de productos").pack()
        self.cantidad_devolucion_entry = tk.Entry(self)
        self.cantidad_devolucion_entry.pack()

        tk.Button(self, text="Registrar devolución", command=self.procesar_registro_devolucion).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_registro_devolucion(self):
        producto = self.producto_devolucion_entry.get()
        cantidad = self.cantidad_devolucion_entry.get()

        if not producto or not cantidad:
            messagebox.showerror("Error", "Favor de llenar todos los campos")
            return

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Cantidad inválida")
            return

        inventario = Inventario()
        if inventario.actualizarSalidas(producto, int(cantidad)):
            messagebox.showinfo("Éxito", "Devolución registrada correctamente")
        else:
            messagebox.showerror("Error", "Error al registrar la devolución")

        self.create_widgets()

    def generar_historiales_compra(self):
        self.clear_frame()
        tk.Label(self, text="Historiales de Compra", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Historial de compras", command=self.mostrar_historial_compras).pack(pady=10)
        tk.Button(self, text="Historial de compras por proveedor", command=self.historial_compras_proveedor).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def mostrar_historial_compras(self):
        self.clear_frame()
        tk.Label(self, text="Historial de Compras", font=("Arial", 16)).pack(pady=10)
        self.resultado_text = tk.Text(self, height=20, width=80)
        self.resultado_text.pack(pady=10)
        PedidosProveedor.mostrar_pedidos()
        tk.Button(self, text="Volver", command=self.generar_historiales_compra).pack(pady=10)

    def historial_compras_proveedor(self):
        self.clear_frame()
        tk.Label(self, text="Historial de Compras por Proveedor", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Nombre del proveedor").pack()
        self.proveedor_historial_entry = tk.Entry(self)
        self.proveedor_historial_entry.pack()

        tk.Button(self, text="Mostrar historial", command=self.procesar_historial_compras_proveedor).pack(pady=10)
        tk.Button(self, text="Volver", command=self.generar_historiales_compra).pack(pady=10)

    def procesar_historial_compras_proveedor(self):
        nombre_proveedor = self.proveedor_historial_entry.get()

        if not nombre_proveedor:
            messagebox.showerror("Error", "Favor de ingresar el nombre del proveedor")
            return

        proveedor = Proveedores.validar_provedor(nombre_proveedor)
        if not proveedor:
            messagebox.showerror("Error", "Proveedor no registrado")
            return

        self.clear_frame()
        tk.Label(self, text=f"Historial de Compras de {nombre_proveedor}", font=("Arial", 16)).pack(pady=10)
        self.resultado_text = tk.Text(self, height=20, width=80)
        self.resultado_text.pack(pady=10)
        PedidosProveedor.pedidos_proveedor(nombre_proveedor)
        tk.Button(self, text="Volver", command=self.generar_historiales_compra).pack(pady=10)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = ComprasProveedorApp()
    app.mainloop()
