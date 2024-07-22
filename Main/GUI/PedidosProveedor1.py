import tkinter as tk
from tkinter import messagebox

class PedidosProveedor:
    pedidos = []

    def __init__(self, proveedor, nombre, marca, cantidad):
        self.proveedor = proveedor
        self.nombre = nombre
        self.marca = marca
        self.cantidad = cantidad

    def guardar(self):
        PedidosProveedor.pedidos.append(self)

    @classmethod
    def mostrar_pedidos(cls):
        if not cls.pedidos:
            return "No hay pedidos guardados."
        else:
            return "\n".join(
                f"Proveedor: {pedido.proveedor}, Nombre: {pedido.nombre}, Marca: {pedido.marca}, Cantidad: {pedido.cantidad}"
                for pedido in cls.pedidos
            )

def agregar_pedido():
    proveedor = entry_proveedor.get()
    nombre = entry_nombre.get()
    marca = entry_marca.get()
    cantidad = entry_cantidad.get()

    if not (proveedor and nombre and marca and cantidad):
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return

    try:
        cantidad = int(cantidad)
    except ValueError:
        messagebox.showwarning("Advertencia", "La cantidad debe ser un número.")
        return

    pedido = PedidosProveedor(proveedor, nombre, marca, cantidad)
    pedido.guardar()
    messagebox.showinfo("Éxito", "Pedido guardado exitosamente.")
    limpiar_campos()

def mostrar_pedidos():
    pedidos_text = PedidosProveedor.mostrar_pedidos()
    pedidos_win = tk.Toplevel()
    pedidos_win.title("Lista de Pedidos")

    tk.Label(pedidos_win, text="Pedidos Guardados:").pack(pady=10)
    tk.Text(pedidos_win, wrap="word", height=20, width=50).pack(pady=10)
    text_pedidos = tk.Text(pedidos_win, wrap="word", height=20, width=50)
    text_pedidos.pack(pady=10)
    text_pedidos.insert(tk.END, pedidos_text)
    text_pedidos.config(state=tk.DISABLED)

def limpiar_campos():
    entry_proveedor.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_marca.delete(0, tk.END)
    entry_cantidad.delete(0, tk.END)

root = tk.Tk()
root.title("Registro de Pedidos de Proveedores")

tk.Label(root, text="Proveedor:").grid(row=0, column=0, padx=10, pady=10)
entry_proveedor = tk.Entry(root)
entry_proveedor.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Nombre:").grid(row=1, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Marca:").grid(row=2, column=0, padx=10, pady=10)
entry_marca = tk.Entry(root)
entry_marca.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Cantidad:").grid(row=3, column=0, padx=10, pady=10)
entry_cantidad = tk.Entry(root)
entry_cantidad.grid(row=3, column=1, padx=10, pady=10)

tk.Button(root, text="Agregar Pedido", command=agregar_pedido).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="Mostrar Pedidos", command=mostrar_pedidos).grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
