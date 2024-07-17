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
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Proveedor':<20} {'Entradas':<10} {'Salidas':<10} {'Stock':<10}")
                print("=" * 105)
                for product in self.producto:
                    # Imprimir cada producto con su información formateada en columnas
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.proveedor:<20} {product.entradas:<10} {product.salidas:<10} {product.stock:<10}")
                    product.entradas=0
                    product.salidas=0
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
                Inventario.mensajes_stock(self,nombre)


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
        print("INFORME DE STOCK DISPONIBLE")
        print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Stock':<10}")
        print("=" * 105)
        for product in self.producto:
            print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.stock:<10}")
        print("=" * 105)

def menuInventario():
    inventario = Inventario()
    while True:
        print("1. Generacion de informe de inventario")
        print("2. Generacion de stock")
        print("3. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            inventario.obtenerInventario()
        elif opcion == "2":
            inventario.informeStock()
        elif opcion == "3":
            break

