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
from Main.Inventario import *

class InventarioApp(tk.Tk):
    def __init__(self,main_app):
        super().__init__()
        self.title("Inventario de Productos")
        self.geometry("600x400")
        self.inventario = Inventarios()
        self.create_widgets()
        self.main_app = main_app

    def create_widgets(self):
        self.clear_frame()
        self.geometry("600x400")
        tk.Label(self, text="--- Menú Principal ---", font=("Arial", 16)).pack(pady=10)
        tk.Button(self, text="Generar informe de inventario", width=30, command=self.generar_informe_inventario).pack(pady=5)
        tk.Button(self, text="Generar informe de stock", width=30, command=self.generar_informe_stock).pack(pady=5)
        tk.Button(self, text="Ajuste de inventario", width=30, command=self.ajuste_inventario).pack(pady=5)
        tk.Button(self, text="Revisión de fechas de caducidad", width=30, command=self.revision_fechas_caducidad).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.volver_menu_principal).pack(pady=20)

    def volver_menu_principal(self):
        self.destroy()
        self.main_app.deiconify()

    def generar_informe_inventario(self):
        self.clear_frame()
        self.geometry("1300x600")
        tk.Label(self, text="Reporte de Inventario", font=("Arial", 16)).pack(pady=10)

        # Crear un frame para el Text y el Scrollbar
        text_frame = tk.Frame(self)
        text_frame.pack(pady=10)

        self.resultado_text = tk.Text(text_frame, height=20, width=200, state=tk.DISABLED, wrap=tk.NONE)
        self.resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.resultado_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resultado_text.config(yscrollcommand=scrollbar.set)

        productos = self.inventario.obtenerInventario()
        self.resultado_text.config(state=tk.NORMAL)
        if productos:
            self.resultado_text.insert(tk.END,
                                       f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Proveedor':<20} {'Entradas':<10} {'Salidas':<10} {'Stock':<10} {'Existencias_anteriores':<20} {'Ajustes':<10}\n")
            for producto in productos:
                self.resultado_text.insert(tk.END,
                                           f"{producto.codigo:<10} {producto.nombre:<20} {producto.marca:<15} {producto.precio:<10} {producto.proveedor:<20} {producto.entradas:<10} {producto.salidas:<10} {producto.stock:<10} {producto.existenciasAnteriores:<20} {producto.ajuste:<10}\n")
                producto.existenciasAnteriores = producto.stock
            Producto.escribir_archivo_csv_productos_principal()
        else:
            self.resultado_text.insert(tk.END, "No hay productos registrados")
        self.resultado_text.config(state=tk.DISABLED)

        # Frame para los botones de generación de archivos en la misma línea
        archivo_frame = tk.Frame(self)
        archivo_frame.pack(pady=5)

        tk.Button(archivo_frame, text="Generar archivo CSV", command= Inventario.escribir_archivo_csv).pack(side=tk.LEFT, padx=5)
        tk.Button(archivo_frame, text="Generar archivo JSON", command= Inventario.escribir_archivo_json).pack(side=tk.LEFT, padx=5)
        tk.Button(archivo_frame, text="Generar archivo PDF", command= Inventario.escribir_archivo_pdf).pack(side=tk.LEFT, padx=5)
        tk.Button(archivo_frame, text="Generar archivo XLSX", command= Inventario.escribir_archivo_xlsx).pack(side=tk.LEFT, padx=5)

        tk.Button(self,text="Limpiar entradas,salidas y ajuste", command=self.procesar_limpieza).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

        #self.inventario.obtenerInventario()
    def procesar_limpieza(self):
        if self.inventario.limpiar():
            messagebox.showinfo("Limpieza", "Limpieza de entradas, salidas y ajustes realizado")
        else:
            messagebox.showinfo("Sin datos","no hay productos registrados")

    def generar_informe_stock(self):

        self.clear_frame()
        self.geometry("600x600")
        tk.Label(self, text="Reporte de Stock", font=("Arial", 16)).pack(pady=10)

        # Crear un frame para el Text y el Scrollbar
        text_frame = tk.Frame(self)
        text_frame.pack(pady=10)

        self.resultado_text = tk.Text(text_frame, height=20, width=200, state=tk.DISABLED, wrap=tk.NONE)
        self.resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.resultado_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resultado_text.config(yscrollcommand=scrollbar.set)

        productos = self.inventario.informeStock()
        self.resultado_text.config(state=tk.NORMAL)
        if productos:
            self.resultado_text.insert(tk.END,
                                       f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Stock':<10}\n")
            for producto in productos:
                self.resultado_text.insert(tk.END,
                                           f"{producto.codigo:<10} {producto.nombre:<20} {producto.marca:<15} {producto.precio:<10} {producto.stock:<10}\n")
        else:
            self.resultado_text.insert(tk.END, "No hay productos registrados")
        self.resultado_text.config(state=tk.DISABLED)

        # Frame para los botones de generación de archivos en la misma línea
        archivo_frame = tk.Frame(self)
        archivo_frame.pack(pady=5)

        tk.Button(archivo_frame, text="Generar archivo CSV", command=Inventario.escribir_archivo_stock_csv).pack(side=tk.LEFT,
                                                                                                           padx=5)
        tk.Button(archivo_frame, text="Generar archivo JSON", command=Inventario.escribir_archivo_stock_json).pack(
            side=tk.LEFT, padx=5)
        tk.Button(archivo_frame, text="Generar archivo PDF", command=Inventario.escribir_archivo_stock_pdf).pack(side=tk.LEFT,
                                                                                                           padx=5)
        tk.Button(archivo_frame, text="Generar archivo XLSX", command=Inventario.escribir_archivo_stock_xlsx).pack(
            side=tk.LEFT, padx=5)

        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

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

        if not nombre or not cantidad or not precio:
            messagebox.showerror("Error","Ingrese todos los campos requeridos")
            return

        if not nombre or not Producto.validar_nombre(nombre):
            messagebox.showerror("Error", "El nombre del producto no existe")
            return

        if not cantidad.isdigit() or int(cantidad) < 0 or int(cantidad) > Producto.validar_stock(nombre):
            messagebox.showerror("Error", "Cantidad no válida")
            return

        try:
            precio = float(precio)
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Precio no válido")
            return

        total = self.inventario.calculoAjuste(int(cantidad), nombre, precio)
        Inventario.actualizarSalidas(nombre, int(cantidad))
        mensaje_stock=Inventario.mensajes_stock(nombre)
        messagebox.showinfo("Éxito", f"Ajuste realizado exitosamente\ntotal a reponer {total}\n{mensaje_stock}")
        Producto.escribir_archivo_csv_productos_principal()
        self.create_widgets()

    def revision_fechas_caducidad(self):
        lista_proximos,lista_cambios=self.inventario.fechas_caducidad()
        self.clear_frame()
        self.geometry("600x600")
        tk.Label(self, text="Reporte de fechas de caducidad", font=("Arial", 16)).pack(pady=10)

        # Crear un frame para el Text y el Scrollbar
        text_frame = tk.Frame(self)
        text_frame.pack(pady=10)

        self.resultado_text = tk.Text(text_frame, height=20, width=200, state=tk.DISABLED, wrap=tk.NONE)
        self.resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.resultado_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resultado_text.config(yscrollcommand=scrollbar.set)


        self.resultado_text.config(state=tk.NORMAL)
        if lista_proximos or lista_cambios:
            for cambios in lista_cambios:
                self.resultado_text.insert(tk.END,cambios+"\n")
            for proximos in lista_proximos:
                self.resultado_text.insert(tk.END,proximos+"\n")
        else:
            self.resultado_text.insert(tk.END, "No hay productos proximos a caducar")
        self.resultado_text.config(state=tk.DISABLED)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

class Inventarios:
    def __init__(self):
        self.producto = Producto.lista_productos
        self.proveedor = Proveedores.proveedores
    def mensajes_stock(self, nombre):
        for product in Producto.lista_productos:
            if product.nombre == nombre:
                if int(product.stock) < 5 and int(product.stock) > 0:
                    print("Stock bajo de ", product.nombre)
                elif int(product.stock) == 0:
                    print("No hay stock de ", product.nombre)

    def obtenerInventario(self):
        if Proveedores.proveedores:
            if Producto.lista_productos:
                #while True:
                    #print("Desea crear un archivo del informe de inventario?")
                    #print("1. Si")
                    #print("2. No")
                    #opcion = input("Seleccione una opcion")
                    #if opcion == "1":
                        #self.menu_archivos()
                        #break
                    #elif opcion == "2":
                        #break
                print("INFORME DE INVENTARIO CREADO EL: ", datetime.now())
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Proveedor':<20} {'Entradas':<10} {'Salidas':<10} {'Stock':<10} {'Existencias_anteriores'} {'Ajustes':<10}")
                print("=" * 105)
                for product in self.producto:
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.proveedor:<20} {product.entradas:<10} {product.salidas:<10} {product.stock:<10} {product.existenciasAnteriores} {product.ajuste:<10}")
                    #product.entradas=0
                    #product.salidas=0
                    #product.ajuste=0
                    print("=" * 105)
                return self.producto
            else:
                print('No hay proveedores registrados')
        else:
            print('No hay productos registrados')

    def limpiar(self):
        if self.producto:
            for product in self.producto:
                product.entradas = 0
                product.salidas = 0
                product.ajuste = 0
            return True
        else:
            return False


    def informeStock(self):
        if self.producto:
            if self.proveedor:
                Inventario.escribir_archivo_stock_csv()
                Inventario.escribir_archivo_stock_json()
                Inventario.escribir_archivo_stock_pdf()
                Inventario.escribir_archivo_stock_xlsx()
                print("INFORME DE STOCK DISPONIBLE")
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Stock':<10}")
                print("=" * 105)
                for product in self.producto:
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.stock:<10}")
                print("=" * 105)
                #for product in self.producto:
                    #Inventario.mensajes_stock(product.nombre)
                return self.producto
            else:
                print('No hay proveedores registrados')
                return None
        else:
            print('No hay productos registrados')
            return None

    def calculoAjuste(self,cantidad,nombre,precio):
        for product in self.producto:
            if product.nombre == nombre:
                total_reponer = int(cantidad) * int(precio)
                print("Ajuste realizada")
                print("Total a reponer: ", total_reponer)
                product.ajuste = cantidad
                return total_reponer

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
        lista_proximos = []
        lista_cambios = []
        formato = "%d/%m/%Y"
        for product in self.producto:
            fecha_caducidad = datetime.strptime(product.fecha_caducidad, formato)
            fecha_actual = datetime.now()
            diferencia_dias = (fecha_caducidad - fecha_actual).days
            if diferencia_dias <= 10:
                if diferencia_dias <= 2:
                    print("Realizar cambio de: ", product.nombre)
                    lista_cambios.append(f"Realizar cambio de {product.nombre}")
                else:
                    print(product.nombre, "Próximo a caducar")
                    lista_proximos.append(f"{product.nombre} próximo a caducar")
            else:
                print("Sin productos próximos a caducar")
                break
        return lista_proximos, lista_cambios

if __name__ == "__main__":
    app = InventarioApp()
    app.mainloop()
