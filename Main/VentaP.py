from Inventario import *
from VentasMain import *
from Productos import *

class Ventas:
    ventas_list = []

    def __init__(self, producto, cantidad, precio_unitario):
        self.producto = producto
        self.cantidad = cantidad
        self.total = int(cantidad) * int(precio_unitario)
        self.guardar_venta()

    def guardar_venta(self):
        venta = {
            'producto': self.producto,
            'cantidad': self.cantidad,
            'total': self.total
        }
        Ventas.ventas_list.append(venta)

    @staticmethod
    def mostrar_ventas():
        for venta in Ventas.ventas_list:
            print(f"Producto: {venta['producto']}, Cantidad: {venta['cantidad']}, Total: {venta['total']}")



def buscar_producto(producto):
    print(producto)
    while not producto:
        producto = input("Ingrese el nombre del producto: ")
        print(f"Buscando el producto '{producto}'...")
        for i in Producto.lista_productos:
            if i.nombre == producto:
                return producto
            else:
                print("Producto no encontrado")
                producto = ""

def seleccionar_cantidad_producto(producto):
    cantidad = input("Ingrese la cantidad del producto: ")
    for i in Producto.lista_productos:
        if i.nombre == producto:
            if int(cantidad) > int(i.stock):
                print("La cantidad excede el stock")
                cantidad = ""
            elif int(cantidad) == 0:
                print("La cantidad debe ser mayor a 0")
                cantidad = ""
            else:
                print(f"Seleccionando {cantidad} unidades...")
                return cantidad
def menuVentas():
    print("----Ventas---")
    print("1 - Agregar Venta")
    print("2 - Mostrar Historial Ventas")
    print("0 - Salir")
    opcion= int(input("Seleccione una opcion: "))
    if opcion == 1:
        while True:
            print("1.- Agregar producto")
            print("2.- salir")
            opcion2= int(input("Seleccione una opcion: "))
            if opcion2 == 1:
                producto=input("Ingrese el nombre del producto: ")
                validaNP = Producto.buscar_nombre(producto)
                if validaNP:
                   #print(seleccionar_cantidad_producto(validaNP))
                   cant= (input("Ingrese la cantidad"))
                   precio=input("Ingrese el precio del producto: ")
                   Ventas(producto, cant, precio)
                   Inventario.actualizarSalidas(producto, cant)
                  # Ventas.guardar_venta(nueva)
                else:
                    print("Producto no encontrado")
            elif opcion2 == 2:
                print("Saliendo...")
                break
    elif opcion == 2:
        Ventas.mostrar_ventas()




