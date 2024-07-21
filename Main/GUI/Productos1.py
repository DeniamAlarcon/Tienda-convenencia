import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re

from Main.Productos import Producto
from Main.Proveedores import Proveedores

def validar_tamanio(tamanio):
    unidades_validas = ["kg", "g", "L", "ml", "pcs", "m", "cm", "in"]
    pattern = re.compile(r'^(\d+(\.\d+)?)(kg|g|L|ml|pcs|m|cm|in)$')
    match = pattern.match(tamanio)
    if match:
        unidad = match.group(3)
        return unidad in unidades_validas
    return False

def validarDigitos(digito):
    return digito.isdigit()

def validar_fecha(fecha):
    formato = "%d/%m/%Y"
    try:
        datetime.strptime(fecha, formato)
        return True
    except ValueError:
        return False

def validar_caducidad(fecha):
    formato = "%d/%m/%Y"
    fecha_actual = datetime.now()
    fecha_dada = datetime.strptime(fecha, formato)
    return fecha_dada < fecha_actual

def validar_cantidad(cantidad):
    return cantidad.isdigit() and int(cantidad) > 0

def validar_precio(precio):
    return precio.isdigit() and int(precio) > 0

class ProductosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Productos")
        self.geometry("600x600")
        self.create_widgets()

    def create_widgets(self):
        self.clear_frame()
        tk.Label(self, text="--- Menu de Productos ---", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Registrar Producto", width=30, command=self.registrar_producto).pack(pady=5)
        tk.Button(self, text="Detalles de Producto", width=30, command=self.detalles_producto).pack(pady=5)
        tk.Button(self, text="Actualizar Producto", width=30, command=self.actualizar_producto).pack(pady=5)
        tk.Button(self, text="Crear Archivos", width=30, command=self.menu_archivos).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.destroy).pack(pady=20)

    def registrar_producto(self):
        self.clear_frame()
        tk.Label(self, text="Registrar Producto", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Código").pack()
        self.codigo_entry = tk.Entry(self)
        self.codigo_entry.pack()

        tk.Label(self, text="Nombre").pack()
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.pack()

        tk.Label(self, text="Marca").pack()
        self.marca_entry = tk.Entry(self)
        self.marca_entry.pack()

        tk.Label(self, text="Proveedor").pack()
        self.proveedor_entry = tk.Entry(self)
        self.proveedor_entry.pack()

        tk.Label(self, text="Cantidad").pack()
        self.cantidad_entry = tk.Entry(self)
        self.cantidad_entry.pack()

        tk.Label(self, text="Tamaño (ej. 10kg, 250ml, 30pcs)").pack()
        self.tamanio_entry = tk.Entry(self)
        self.tamanio_entry.pack()

        tk.Label(self, text="Precio").pack()
        self.precio_entry = tk.Entry(self)
        self.precio_entry.pack()

        tk.Label(self, text="Fecha de Vencimiento (dd/mm/yyyy)").pack()
        self.fecha_vencimiento_entry = tk.Entry(self)
        self.fecha_vencimiento_entry.pack()

        tk.Button(self, text="Registrar", command=self.procesar_registro).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_registro(self):
        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        marca = self.marca_entry.get()
        proveedor = self.proveedor_entry.get()
        cantidad = self.cantidad_entry.get()
        tamanio = self.tamanio_entry.get()
        precio = self.precio_entry.get()
        fecha_vencimiento = self.fecha_vencimiento_entry.get()

        if not codigo or not nombre or not marca or not proveedor or not cantidad or not tamanio or not precio or not fecha_vencimiento:
            messagebox.showerror("Error", "Favor de llenar todos los campos requeridos")
            return

        if not Producto.validar_codigo(codigo):
            messagebox.showerror("Error", "Código de producto ya registrado")
            return

        if Producto.buscar_nombre(nombre):
            messagebox.showerror("Error", "Nombre de producto ya registrado")
            return

        if not Proveedores.validar_provedor(proveedor):
            messagebox.showerror("Error", "Proveedor no encontrado")
            return

        if not validar_cantidad(cantidad):
            messagebox.showerror("Error", "Cantidad no válida")
            return

        if not validar_tamanio(tamanio):
            messagebox.showerror("Error", "Tamaño no válido")
            return

        if not validar_precio(precio):
            messagebox.showerror("Error", "Precio no válido")
            return

        if not validar_fecha(fecha_vencimiento):
            messagebox.showerror("Error", "Fecha no válida")
            return

        if validar_caducidad(fecha_vencimiento):
            messagebox.showerror("Error", "El producto está caduco")
            return

        registro = Producto(codigo, nombre, marca, proveedor, cantidad, tamanio, precio, fecha_vencimiento)
        if registro.registrar():
            messagebox.showinfo("Éxito", "Producto registrado exitosamente")
            self.create_widgets()
        else:
            messagebox.showerror("Error", "Producto no registrado")

    def detalles_producto(self):
        self.clear_frame()
        tk.Label(self, text="Detalles de Producto", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Busqueda por Nombre", width=30, command=self.buscar_por_nombre).pack(pady=5)
        tk.Button(self, text="Gestión de Productos", width=30, command=self.gestion_productos).pack(pady=5)
        tk.Button(self, text="Volver", width=30, command=self.create_widgets).pack(pady=10)

    def buscar_por_nombre(self):
        self.clear_frame()
        tk.Label(self, text="Buscar Producto por Nombre", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Nombre del Producto").pack()
        self.nombre_busqueda_entry = tk.Entry(self)
        self.nombre_busqueda_entry.pack()
        tk.Button(self, text="Buscar", command=self.procesar_busqueda_nombre).pack(pady=10)
        tk.Button(self, text="Volver", command=self.detalles_producto).pack(pady=10)
        self.resultado_text = tk.Text(self, height=10, width=50, state=tk.DISABLED)
        self.resultado_text.pack(pady=10)

    def procesar_busqueda_nombre(self):
        nombre = self.nombre_busqueda_entry.get()
        resultados = Producto.detalles_nombre(nombre)
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete(1.0, tk.END)

        if resultados:
            for producto in resultados:
                self.resultado_text.insert(tk.END, f"ID: {producto.id}, Nombre: {producto.nombre}, Marca: {producto.marca}, Proveedor: {producto.proveedor}, Cantidad: {producto.cantidad}, Tamaño: {producto.tamanio}, Precio: {producto.precio}, Fecha de Vencimiento: {producto.fecha_vencimiento}\n")
        else:
            self.resultado_text.insert(tk.END, "No se encontraron productos con ese nombre")

        self.resultado_text.config(state=tk.DISABLED)

    def gestion_productos(self):
        self.clear_frame()
        tk.Label(self, text="Gestión de Productos", font=("Arial", 16)).pack(pady=10)
        self.resultado_text = tk.Text(self, height=20, width=80, state=tk.DISABLED)
        self.resultado_text.pack(pady=10)
        productos = Producto.detalles()
        self.resultado_text.config(state=tk.NORMAL)
        if productos:
            for producto in productos:
                self.resultado_text.insert(tk.END, f"ID: {producto.id}, Nombre: {producto.nombre}, Marca: {producto.marca}, Proveedor: {producto.proveedor}, Cantidad: {producto.cantidad}, Tamaño: {producto.tamanio}, Precio: {producto.precio}, Fecha de Vencimiento: {producto.fecha_vencimiento}\n")
        else:
            self.resultado_text.insert(tk.END, "No hay productos registrados")
        self.resultado_text.config(state=tk.DISABLED)

        tk.Button(self, text="Volver", command=self.detalles_producto).pack(pady=10)

    def actualizar_producto(self):
        self.clear_frame()
        tk.Label(self, text="Actualizar Producto", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Código del Producto").pack()
        self.codigo_actualizar_entry = tk.Entry(self)
        self.codigo_actualizar_entry.pack()

        tk.Label(self, text="Nuevo Nombre (dejar en blanco para no cambiar)").pack()
        self.nombre_actualizar_entry = tk.Entry(self)
        self.nombre_actualizar_entry.pack()

        tk.Label(self, text="Nuevo Proveedor (dejar en blanco para no cambiar)").pack()
        self.proveedor_actualizar_entry = tk.Entry(self)
        self.proveedor_actualizar_entry.pack()

        tk.Label(self, text="Nuevo Tamaño (dejar en blanco para no cambiar)").pack()
        self.tamanio_actualizar_entry = tk.Entry(self)
        self.tamanio_actualizar_entry.pack()

        tk.Label(self, text="Nuevo Precio (dejar en blanco para no cambiar)").pack()
        self.precio_actualizar_entry = tk.Entry(self)
        self.precio_actualizar_entry.pack()

        tk.Button(self, text="Actualizar", command=self.procesar_actualizacion).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_actualizacion(self):
        codigo = self.codigo_actualizar_entry.get()
        nombre = self.nombre_actualizar_entry.get()
        proveedor = self.proveedor_actualizar_entry.get()
        tamanio = self.tamanio_actualizar_entry.get()
        precio = self.precio_actualizar_entry.get()

        if nombre and Producto.buscar_nombre(nombre):
            messagebox.showerror("Error", "Nombre de producto ya registrado")
            return

        if proveedor and not Proveedores.validar_provedor(proveedor):
            messagebox.showerror("Error", "Proveedor no encontrado")
            return

        if tamanio and not validar_tamanio(tamanio):
            messagebox.showerror("Error", "Tamaño no válido")
            return

        if precio and not validar_precio(precio):
            messagebox.showerror("Error", "Precio no válido")
            return

        Producto.actualizar(codigo, nombre, proveedor, tamanio, precio)
        messagebox.showinfo("Éxito", "Producto actualizado exitosamente")
        self.create_widgets()

    def menu_archivos(self):
        self.clear_frame()
        tk.Label(self, text="--- Menu de Archivos ---", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Crear Archivo CSV", width=30, command=Producto.crear_archivo_csv).pack(pady=5)
        tk.Button(self, text="Crear Archivo JSON", width=30, command=Producto.crear_archivo_json).pack(pady=5)
        tk.Button(self, text="Crear Archivo PDF", width=30, command=Producto.crear_archivo_pdf).pack(pady=5)
        tk.Button(self, text="Crear Archivo XLSX", width=30, command=Producto.crear_archivo_xlsx).pack(pady=5)
        tk.Button(self, text="Volver", width=30, command=self.create_widgets).pack(pady=20)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = ProductosApp()
    app.mainloop()
