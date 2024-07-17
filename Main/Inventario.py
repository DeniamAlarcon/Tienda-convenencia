from Productos import *
from Proveedores import *
from datetime import datetime

class Inventario:
    def __init__(self):
        self.producto = Producto.lista_productos
        self.proveedor = Proveedores.proveedores

    def obtenerInventario(self):
        if self.proveedor:
            if self.producto:
                print("INFORME DE INVENTARIO CREADO EL: ", datetime.now())
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Proveedor':<20} {'Entradas':<10} {'Salidas':<10} {'Stock':<10} {'Ajustes':<10}")
                print("=" * 105)
                for product in self.producto:
                    # Imprimir cada producto con su información formateada en columnas
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.proveedor:<20} {product.entradas:<10} {product.salidas:<10} {product.stock:<10} {product.ajuste}:<10")
                    product.entradas=0
                    product.salidas=0
                    product.ajuste=0
                    print("=" * 105)
            else:
                print('No hay proveedores registrados')
        else:
            print('No hay productos registrados')


    def mensajes_stock(self,nombre):
        for product in self.producto:
            if product.nombre == nombre:
                if product.stock < 5 and product.stock >0:
                    print("Stock bajo de ",product.nombre)
                elif product.stock == 0:
                    print("No hay stock de ",product.nombre)

    def actualizarEntradas(self, nombre, cantidad):
        for product in self.producto:
            if product.nombre == nombre:
                product.entradas = int(product.entradas) + int(cantidad)
                product.stock = int(product.stock) + int(cantidad)
                Inventario.mensajes_stock(self, nombre)


    def actualizarSalidas(self, nombre, cantidad):
        for product in self.producto:
            if product.nombre == nombre:
                if product.stock > cantidad:
                    product.salidas = int(product.salidas) + int(cantidad)
                    product.stock = int(product.stock) - int(cantidad)
                    print("Devolucion realizada")
                    Inventario.mensajes_stock(self,nombre)
                else:
                    print("No hay suficiente stock para realizar la accion")
            else:
                print("Producto no encontrado")

    def informeStock(self):
        if self.producto:
            if self.proveedor:
                print("INFORME DE STOCK DISPONIBLE")
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Stock':<10}")
                print("=" * 105)
                for product in self.producto:
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.stock:<10}")
                print("=" * 105)
                for product in self.producto:
                    Inventario.mensajes_stock(self,product.nombre)
            else:
                print('No hay proveedores registrados')
        else:
            print('No hay productos registrados')

    def calculoAjuste(self,cantidad,nombre,precio):
        for product in self.producto:
            if product.nombre == nombre:
                total_reponer = int(cantidad)*int(precio)
                print("Ajuste realizada")
                print("Total a reponer: ",total_reponer)
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
                        if cantidad < Producto.validar_stock(nombre):
                            if int(cantidad) < 0:
                                print("Ingrese una cantidad mayor a 0")
                                cantidad = ""
                        else:
                            print("La cantidad ingresada excede el stock")
                            cantidad = ""
                    else:
                        print("Favor de ingresar el dato requerido")

                precio = ""
                while not precio:
                    precio = input("Ingrese el precio del producto: ")
                    if precio:
                        if int(precio) < 0:
                            print("Ingrese una precio mayor a 0")
                            precio = ""
                    else:
                        print("Favor de ingresar el dato requerido")

                Inventario.calculoAjuste(self,cantidad,nombre,precio)
            else:
                print('No hay productos registrados')
        else:
            print('No hay proveedores registrados')


def menuInventario():
    inventario = Inventario()
    while True:
        print("1. Generacion de informe de inventario")
        print("2. Generacion de stock")
        print("3. Ajuste de inventario(robos,perdidas,daños)")
        print("4. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            inventario.obtenerInventario()
        elif opcion == "2":
            inventario.informeStock()
        elif opcion == "3":
            inventario.ajuste_inventario()
            while True:
                print("1. Ingresar otro ajuste")
                print("2. Salir")
                opcion1 = input("Ingrese una opcion: ")
                if opcion1 == "1":
                    inventario.ajuste_inventario()
                elif opcion1 == "2":
                    break
        elif opcion == "4":
            break

