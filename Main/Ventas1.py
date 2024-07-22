import tkinter as tk
from tkinter import simpledialog, messagebox

class VentasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Ventas")

        # Widgets de la ventana principal
        self.label = tk.Label(root, text="--- Sistema de Ventas ---", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.btn_acceder_ventas = tk.Button(root, text="Acceder al Apartado de Ventas", command=self.acceder_apartado_ventas)
        self.btn_acceder_ventas.pack(pady=5)

        self.productos = []

    def acceder_apartado_ventas(self):
        print("Accediendo al apartado de ventas")
        self.buscar_productos()

    def buscar_productos(self):
        n = simpledialog.askinteger("Buscar Productos", "¿Cuántos productos desea buscar?", minvalue=1)
        if n:
            for _ in range(n):
                self.buscar_producto()

            self.seleccionar_metodo_pago()

    def buscar_producto(self):
        producto = simpledialog.askstring("Buscar Producto", "Ingrese el nombre del producto:")
        if producto:
            self.agregar_producto_a_venta(producto)

    def agregar_producto_a_venta(self, producto):
        print(f"Agregando '{producto}' a la venta...")
        cantidad = self.seleccionar_cantidad_producto(producto)
        self.productos.append((producto, cantidad))

    def seleccionar_cantidad_producto(self, producto):
        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad para '{producto}':", minvalue=1)
        print(f"Seleccionando {cantidad} unidades de {producto}...")
        return cantidad

    def seleccionar_metodo_pago(self):
        metodo_pago = simpledialog.askstring("Método de Pago", "Seleccione el método de pago (tarjeta/efectivo):")
        if metodo_pago:
            print(f"Método de pago seleccionado: {metodo_pago}")
            self.verificar_pago()

    def verificar_pago(self):
        monto_venta = sum(cantidad for _, cantidad in self.productos)  # Asume que el precio de cada producto es 1 unidad
        print(f"El monto total de la venta es: {monto_venta}")
        pago_cliente = simpledialog.askfloat("Verificar Pago", f"Ingrese el monto pagado por el cliente (Monto total: {monto_venta}):")
        if pago_cliente >= monto_venta:
            messagebox.showinfo("Pago Verificado", "Accediendo a emisión de tickets...")
        else:
            messagebox.showerror("Pago Insuficiente", "Dinero insuficiente")

if __name__ == "__main__":
    root = tk.Tk()
    app = VentasApp(root)
    root.mainloop()
