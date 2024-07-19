import tkinter as tk
from tkinter import messagebox

class Producto:
    lista_productos = []

    def __init__(self, codigo, nombre, marca, proveedor, cantidad, tamanio, precio, fecha_caducidad):
        self.codigo = codigo
        self.nombre = nombre
        self.marca = marca
        self.proveedor = proveedor
        self.cantidad = cantidad
        self.tamanio = tamanio
        self.precio = precio
        self.fecha_caducidad = fecha_caducidad

    def registrar(self):
        Producto.lista_productos.append(self)
        return True

    @classmethod
    def buscar_nombre(cls, nombre):
        for product in cls.lista_productos:
            if product.nombre == nombre:
                return True
        return False

    @classmethod
    def detalles_nombre(cls, nombre):
        for product in cls.lista_productos:
            if product.nombre == nombre:
                return product
        return None

    @classmethod
    def detalles(cls):
        if len(cls.lista_productos) != 0:
            for product in cls.lista_productos:
                print(product.codigo, product.nombre, product.marca, product.proveedor, product.cantidad, product.tamanio, product.precio, product.fecha_caducidad)
        else:
            print("producto no encontrado")

    @classmethod
    def buscarProducto(cls, id):
        for product in cls.lista_productos:
            if product.codigo == id:
                return product
        return None

    @classmethod
    def actualizar(cls, id, nombre, proveedor, tamanio, precio):
        producto = cls.buscarProducto(id)
        if producto:
            producto.nombre = nombre if nombre else producto.nombre
            producto.proveedor = proveedor if proveedor else producto.proveedor
            producto.tamanio = tamanio if tamanio else producto.tamanio
            producto.precio = precio if precio else producto.precio
            print("Producto actualizado")
        else:
            print("Producto no encontrado")

    @classmethod
    def validar_codigo(cls, codigo):
        for product in cls.lista_productos:
            if product.codigo == codigo:
                return True
        return False

    @classmethod
    def validar_marca(cls, marca):
        for product in cls.lista_productos:
            if product.marca == marca:
                return True
        return False

def registrar_producto():
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    marca = entry_marca.get()
    proveedor = entry_proveedor.get()
    cantidad = entry_cantidad.get()
    tamanio = entry_tamanio.get()
    precio = entry_precio.get()
    fecha_caducidad = entry_fecha_caducidad.get()

    if Producto.validar_codigo(codigo):
        messagebox.showerror("Error", "Código ya registrado.")
    elif Producto.buscar_nombre(nombre):
        messagebox.showerror("Error", "Nombre de producto ya registrado.")
    else:
        producto = Producto(codigo, nombre, marca, proveedor, cantidad, tamanio, precio, fecha_caducidad)
        producto.registrar()
        messagebox.showinfo("Éxito", "Producto registrado correctamente.")

def buscar_producto():
    nombre = entry_buscar_nombre.get()
    producto = Producto.detalles_nombre(nombre)
    if producto:
        messagebox.showinfo("Producto Encontrado", f"Código: {producto.codigo}\nNombre: {producto.nombre}\nMarca: {producto.marca}\nProveedor: {producto.proveedor}\nCantidad: {producto.cantidad}\nTamaño: {producto.tamanio}\nPrecio: {producto.precio}\nFecha Caducidad: {producto.fecha_caducidad}")
    else:
        messagebox.showerror("Error", "Producto no encontrado.")

# Interfaz Gráfica
root = tk.Tk()
root.title("Gestión de Productos")

# Registro de Producto
frame_registro = tk.Frame(root)
frame_registro.pack(pady=10)

tk.Label(frame_registro, text="Código").grid(row=0, column=0)
tk.Label(frame_registro, text="Nombre").grid(row=1, column=0)
tk.Label(frame_registro, text="Marca").grid(row=2, column=0)
tk.Label(frame_registro, text="Proveedor").grid(row=3, column=0)
tk.Label(frame_registro, text="Cantidad").grid(row=4, column=0)
tk.Label(frame_registro, text="Tamaño").grid(row=5, column=0)
tk.Label(frame_registro, text="Precio").grid(row=6, column=0)
tk.Label(frame_registro, text="Fecha de Caducidad").grid(row=7, column=0)

entry_codigo = tk.Entry(frame_registro)
entry_nombre = tk.Entry(frame_registro)
entry_marca = tk.Entry(frame_registro)
entry_proveedor = tk.Entry(frame_registro)
entry_cantidad = tk.Entry(frame_registro)
entry_tamanio = tk.Entry(frame_registro)
entry_precio = tk.Entry(frame_registro)
entry_fecha_caducidad = tk.Entry(frame_registro)

entry_codigo.grid(row=0, column=1)
entry_nombre.grid(row=1, column=1)
entry_marca.grid(row=2, column=1)
entry_proveedor.grid(row=3, column=1)
entry_cantidad.grid(row=4, column=1)
entry_tamanio.grid(row=5, column=1)
entry_precio.grid(row=6, column=1)
entry_fecha_caducidad.grid(row=7, column=1)

tk.Button(frame_registro, text="Registrar Producto", command=registrar_producto).grid(row=8, column=0, columnspan=2, pady=10)

# Buscar Producto
frame_buscar = tk.Frame(root)
frame_buscar.pack(pady=10)

tk.Label(frame_buscar, text="Buscar Producto por Nombre").grid(row=0, column=0, columnspan=2)

entry_buscar_nombre = tk.Entry(frame_buscar)
entry_buscar_nombre.grid(row=1, column=0)

tk.Button(frame_buscar, text="Buscar", command=buscar_producto).grid(row=1, column=1)

root.mainloop()
