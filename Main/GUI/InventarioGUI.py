import tkinter as tk
from tkinter import messagebox
import csv
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.units import inch
from openpyxl import Workbook
from datetime import datetime
from Main.Productos import *
from Main.Proveedores import *

class InventarioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventario de Productos")
        self.geometry("600x400")
        self.inventario = Inventario()
        self.create_widgets()

    def create_widgets(self):
        self.clear_frame()

        tk.Label(self, text="--- Menú Principal ---", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Generar informe de inventario", width=30, command=self.generar_informe_inventario).pack(pady=5)
        tk.Button(self, text="Generar informe de stock", width=30, command=self.generar_informe_stock).pack(pady=5)
        tk.Button(self, text="Ajuste de inventario", width=30, command=self.ajuste_inventario).pack(pady=5)
        tk.Button(self, text="Revisión de fechas de caducidad", width=30, command=self.revision_fechas_caducidad).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.quit).pack(pady=20)

    def generar_informe_inventario(self):
        self.inventario.obtenerInventario()

    def generar_informe_stock(self):
        self.inventario.informeStock()

    def ajuste_inventario(self):
        self.clear_frame()

        tk.Label(self, text="--- Ajuste de Inventario ---", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Nombre del Producto").pack()
        self.nombre_ajuste_entry = tk.Entry(self)
        self.nombre_ajuste_entry.pack()

        tk.Label(self, text="Cantidad Dañada").pack()
        self.cantidad_ajuste_entry = tk.Entry(self)
        self.cantidad_ajuste_entry.pack()

        tk.Label(self, text="Precio del Producto").pack()
        self.precio_ajuste_entry = tk.Entry(self)
        self.precio_ajuste_entry.pack()

        tk.Button(self, text="Realizar Ajuste", command=self.procesar_ajuste).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_ajuste(self):
        nombre = self.nombre_ajuste_entry.get()
        cantidad = self.cantidad_ajuste_entry.get()
        precio = self.precio_ajuste_entry.get()

        if not nombre or not Producto.validar_nombre(nombre):
            messagebox.showerror("Error", "El nombre del producto no existe")
            return

        if not cantidad.isdigit() or int(cantidad) < 0 or int(cantidad) >= Producto.validar_stock(nombre):
            messagebox.showerror("Error", "Cantidad no válida")
            return

        try:
            precio = float(precio)
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Precio no válido")
            return

        self.inventario.calculoAjuste(int(cantidad), nombre, precio)
        self.inventario.actualizarSalidas(nombre, int(cantidad))

        messagebox.showinfo("Éxito", "Ajuste realizado exitosamente")
        self.create_widgets()

    def revision_fechas_caducidad(self):
        self.inventario.fechas_caducidad()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

class Inventario:
    def __init__(self):
        self.producto = Producto.lista_productos
        self.proveedor = Proveedores.proveedores

    def obtenerInventario(self):
        if self.proveedor:
            if self.producto:
                while True:
                    print("Desea crear un archivo del informe de inventario?")
                    print("1. Si")
                    print("2. No")
                    opcion = input("Seleccione una opcion")
                    if opcion == "1":
                        self.menu_archivos()
                        break
                    elif opcion == "2":
                        break
                print("INFORME DE INVENTARIO CREADO EL: ", datetime.now())
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Proveedor':<20} {'Entradas':<10} {'Salidas':<10} {'Stock':<10} {'Existencias_anteriores'} {'Ajustes':<10}")
                print("=" * 105)
                for product in self.producto:
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.proveedor:<20} {product.entradas:<10} {product.salidas:<10} {product.stock:<10} {product.existenciasAnteriores} {product.ajuste:<10}")
                    product.entradas=0
                    product.salidas=0
                    product.ajuste=0
                    print("=" * 105)
            else:
                print('No hay proveedores registrados')
        else:
            print('No hay productos registrados')

    def informeStock(self):
        if self.producto:
            if self.proveedor:
                self.escribir_archivo_stock_csv()
                self.escribir_archivo_stock_json()
                self.escribir_archivo_stock_pdf()
                self.escribir_archivo_stock_xlsx()
                print("INFORME DE STOCK DISPONIBLE")
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Stock':<10}")
                print("=" * 105)
                for product in self.producto:
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.stock:<10}")
                print("=" * 105)
                for product in self.producto:
                    self.mensajes_stock(product.nombre)
            else:
                print('No hay proveedores registrados')
        else:
            print('No hay productos registrados')

    def calculoAjuste(self,cantidad,nombre,precio):
        for product in self.producto:
            if product.nombre == nombre:
                total_reponer = int(cantidad) * int(precio)
                print("Ajuste realizada")
                print("Total a reponer: ", total_reponer)
                product.ajuste = cantidad

    def ajuste_inventario(self):
        if self.proveedor:
            if self.producto:
                nombre = ""
                while not nombre:
                    nombre = input("Ingrese el nombre del producto: ")
                    if nombre:
                        if not Producto.validar_nombre(nombre):
                            print("El nombre del producto no existe")
                            nombre = ""
                    else:
                        print("Favor de ingresar el dato requerido")

                cantidad = ""
                while not cantidad:
                    cantidad = input("Ingrese la cantidad de producto dañado: ")
                    if cantidad:
                        if cantidad.isdigit():
                            if int(cantidad) < Producto.validar_stock(nombre):
                                if int(cantidad) < 0:
                                    print("Ingrese una cantidad mayor a 0")
                                    cantidad = ""
                                else:
                                    cantidad = int(cantidad)
                                    break
                            else:
                                print("La cantidad ingresada excede el stock")
                                cantidad = ""
                        else:
                            print("Favor de ingresar el dato numérico")
                            cantidad = ""
                    else:
                        print("Favor de ingresar el dato requerido")

                precio = ""
                while not precio:
                    try:
                        precio = input("Ingrese el precio del producto: ")
                        if precio:
                            if int(precio) < 0:
                                print("Ingrese un precio mayor a 0")
                                precio = ""
                            else:
                                self.calculoAjuste(cantidad, nombre, precio)
                                self.actualizarSalidas(nombre, cantidad)
                        else:
                            print("Favor de ingresar el dato requerido")
                    except ValueError:
                        print("Precio no válido")
            else:
                print('No hay productos registrados')
        else:
            print('No hay proveedores registrados')

    def fechas_caducidad(self):
        formato = "%d/%m/%Y"
        for product in self.producto:
            fecha_caducidad = datetime.strptime(product.fecha_caducidad, formato)
            fecha_actual = datetime.now()
            diferencia_dias = (fecha_caducidad - fecha_actual).days
            if diferencia_dias <= 10:
                if diferencia_dias <= 2:
                    print("Realizar cambio de: ", product.nombre)
                else:
                    print(product.nombre, "Próximo a caducar")
            else:
                print("Sin productos próximos a caducar")
                break

if __name__ == "__main__":
    app = InventarioApp()
    app.mainloop()
