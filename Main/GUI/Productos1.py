import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re

from login1 import *
from Main.Productos import Producto
from Main.Proveedores import Proveedores
from login1 import *

def validar_tamanio(tamanio):
    unidades_validas = ["kg", "g", "L", "ml", "pcs", "m", "cm", "in", "gr"]
    pattern = re.compile(r'^(\d+(\.\d+)?)(kg|g|L|ml|pcs|m|cm|in|gr)$')
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
    if fecha:
        formato = "%d/%m/%Y"
        fecha_actual = datetime.now()
        fecha_dada = datetime.strptime(fecha, formato)
        return fecha_dada < fecha_actual

def validar_cantidad(cantidad):
    return cantidad.isdigit() and int(cantidad) > 0

def validar_precio(precio):
    return precio.isdigit() and int(precio) > 0

class ProductosApp(tk.Tk):
    def __init__(self,main_app):
        super().__init__()
        self.title("Gestión de Productos")
        self.geometry("600x600")
        self.create_widgets()
        self.main_app = main_app

    def create_widgets(self):
        self.clear_frame()
        tk.Label(self, text="--- Menu de Productos ---", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Registrar Producto", width=30, command=self.registrar_producto).pack(pady=5)
        tk.Button(self, text="Detalles de Producto", width=30, command=self.detalles_producto).pack(pady=5)
        tk.Button(self, text="Actualizar Producto", width=30, command=self.actualizar_producto).pack(pady=5)
        tk.Button(self, text="Eliminar Producto", width=30, command=self.eliminar_producto).pack(pady=5)
        tk.Button(self, text="Crear Archivos", width=30, command=self.menu_archivos).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.volver_menu_principal).pack(pady=20)

    def volver_menu_principal(self):
        self.destroy()
        self.main_app.deiconify()

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

        if Producto.validar_codigo(codigo):
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
            Producto.escribir_archivo_csv_productos_principal()
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
        self.geometry("650x500")
        tk.Label(self, text="Buscar Producto por Nombre", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Nombre del Producto").pack()
        self.nombre_busqueda_entry = tk.Entry(self)
        self.nombre_busqueda_entry.pack()
        tk.Button(self, text="Buscar", command=self.procesar_busqueda_nombre).pack(pady=10)
        tk.Button(self, text="Volver", command=self.detalles_producto).pack(pady=10)
        self.resultado_text = tk.Text(self, height=10, width=75, state=tk.DISABLED)
        self.resultado_text.pack(pady=10)

    def procesar_busqueda_nombre(self):
        nombre = self.nombre_busqueda_entry.get()
        resultados = Producto.detalles_nombre(nombre)
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete(1.0, tk.END)
        if nombre != "":
            if resultados:
                for producto in resultados:
                    if producto.nombre == nombre:
                        self.resultado_text.insert(tk.END,
                                                   f"{'Codigo': <8}{'Nombre': <8}{'Marca': <10}{'Proveedor': <10}{'Cantidad': <10}{'Tamaño': <8}{'Precio': <8}{'Vencimiento': <4}\n")
                        self.resultado_text.insert(tk.END,

                                                   f"{producto.codigo:<8}{producto.nombre:<8}{producto.marca:<10}{producto.proveedor:<10}{producto.cantidad:<10}{producto.tamanio:<8}{producto.precio:<8}{producto.fecha_caducidad:<}\n")

            else:
                self.resultado_text.insert(tk.END, "No se encontraron productos con ese nombre")
        else:
            self.resultado_text.insert(tk.END,  f"{'Codigo': <8}{'Nombre': <8}{'Marca': <10}{'Proveedor': <10}{'Cantidad': <10}{'Tamaño': <8}{'Precio': <8}{'Vencimiento': <4}\n")
            for producto in resultados:
                self.resultado_text.insert(tk.END,f"{producto.codigo:<8}{producto.nombre:<8}{producto.marca:<10}{producto.proveedor:<10}{producto.cantidad:<10}{producto.tamanio:<8}{producto.precio:<8}{producto.fecha_caducidad:<}\n")

        self.resultado_text.config(state=tk.DISABLED)

    def gestion_productos(self):
        self.clear_frame()
        tk.Label(self, text="Gestión de Productos", font=("Arial", 16)).pack(pady=10)
        self.resultado_text = tk.Text(self, height=20, width=80, state=tk.DISABLED)
        self.resultado_text.pack(pady=10)
        productos = Producto.detalles()
        self.resultado_text.config(state=tk.NORMAL)
        if productos:
            self.resultado_text.insert(tk.END, f"{'Codigo': <8}{'Nombre': <8}{'Marca': <10}{'Proveedor': <10}{'Cantidad': <10}{'Tamaño': <8}{'Precio': <8}{'Vencimiento': <4}\n")
            for producto in productos:
                self.resultado_text.insert(tk.END, f"{producto.codigo:<8}{producto.nombre:<8}{producto.marca:<10}{producto.proveedor:<10}{producto.cantidad:<10}{producto.tamanio:<8}{producto.precio:<8}{producto.fecha_caducidad:<}\n")
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
        self.boton_buscar=(tk.Button(self, text="Buscar", command=self.mostar_datos_productos))
        self.boton_buscar.pack(pady=10)


        tk.Label(self, text="Nuevo Nombre").pack()
        self.nombre_actualizar_entry = tk.Entry(self)
        self.nombre_actualizar_entry.pack()

        tk.Label(self, text="Nuevo Proveedor").pack()
        self.proveedor_actualizar_entry = tk.Entry(self)
        self.proveedor_actualizar_entry.pack()

        tk.Label(self, text="Nuevo Tamaño").pack()
        self.tamanio_actualizar_entry = tk.Entry(self)
        self.tamanio_actualizar_entry.pack()

        tk.Label(self, text="Nuevo Precio").pack()
        self.precio_actualizar_entry = tk.Entry(self)
        self.precio_actualizar_entry.pack()

        tk.Label(self, text="Nueva fecha de caducidad (dd/mm/yyyy)").pack()
        self.fecha_actualizar_entry = tk.Entry(self)
        self.fecha_actualizar_entry.pack()

        tk.Button(self, text="Actualizar", command=self.procesar_actualizacion).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def mostar_datos_productos(self):
        resultados = Producto.buscarProducto(self.codigo_actualizar_entry.get())
        if resultados:
            self.nombre_actualizar_entry.insert(tk.END, resultados.nombre)
            self.proveedor_actualizar_entry.insert(tk.END, resultados.proveedor)
            self.tamanio_actualizar_entry.insert(tk.END, resultados.tamanio)
            self.precio_actualizar_entry.insert(tk.END, resultados.precio)
            self.fecha_actualizar_entry.insert(tk.END, resultados.fecha_caducidad)
            self.codigo_actualizar_entry.config(state=tk.DISABLED)
            self.boton_buscar.config(state="disabled")
        else:
            messagebox.showerror("Error", "No se encontro el producto")


    def procesar_actualizacion(self):
        codigo = self.codigo_actualizar_entry.get()
        nombre = self.nombre_actualizar_entry.get()
        proveedor = self.proveedor_actualizar_entry.get()
        tamanio = self.tamanio_actualizar_entry.get()
        precio = self.precio_actualizar_entry.get()
        fecha_caducidad = self.fecha_actualizar_entry.get()

        if not codigo:
            messagebox.showerror("Error","ingrese el campo codigo para actualizar")
            return

        if codigo and not Producto.validar_codigo(codigo):
            messagebox.showerror("Error", "Producto no encontrado")
            return

        if not nombre or not proveedor or not tamanio or not precio or not fecha_caducidad:
            messagebox.showerror("Error", "Ingrese todos los campos")
            return

        if nombre and not Producto.buscar_nombre_GUI(nombre,codigo):
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

        if fecha_caducidad and not validar_fecha(fecha_caducidad):
            messagebox.showerror("Error","Fecha no válida")
            return

        if validar_caducidad(fecha_caducidad):
            messagebox.showerror("Error", "El producto está caduco")
            return

        print(codigo,nombre,tamanio,precio,fecha_caducidad, " esto me importa demasiado")
        Producto.actualizar(codigo, nombre, proveedor, tamanio, precio, fecha_caducidad)
        messagebox.showinfo("Éxito", "Producto actualizado exitosamente")
        Producto.escribir_archivo_csv_productos_principal()
        self.create_widgets()

    def eliminar_producto(self):
        self.clear_frame()
        tk.Label(self, text="Eliminar Producto", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Codigo del Producto").pack()
        self.id_eliminar_entry = tk.Entry(self)
        self.id_eliminar_entry.pack()
        tk.Button(self, text="Eliminar", command=self.procesar_eliminacion).pack(pady=10)

        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_eliminacion(self):
        try:
            id = self.id_eliminar_entry.get()
            if Producto.eliminar_producto(id):
                messagebox.showinfo("Éxito", "Producto eliminado")
                Producto.escribir_archivo_csv_productos_principal()
                self.create_widgets()
                #self.id_eliminar_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Producto no encontrado")
                self.id_eliminar_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un codigo de producto válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el producto: {e}")

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
