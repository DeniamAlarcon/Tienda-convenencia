from Productos import *

def registrarProducto():
    codigo = input("Ingrese el codigo del producto: ")
    while not codigo:
        codigo = input("Ingrese el codigo del producto: ")

    nombre = input("Ingrese el nombre del producto: ")
    while not codigo:
        nombre = input("Ingrese el nombre del producto: ")

    marca = input("Ingrese la marca del producto: ")
    while not marca:
        marca = input("Ingrese la marca del producto: ")

    proveedor = input("Ingrese el proveedor del producto: ")
    while not proveedor:
        proveedor = input("Ingrese el proveedor del producto: ")

    cantidad = input("Ingrese la cantidad del producto: ")
    while not cantidad:
        cantidad = input("Ingrese la cantidad del producto: ")

    tamanio = input("Ingrese el tamaño del producto: ")
    while not tamanio:
        tamanio = input("Ingrese el tamaño del producto: ")

    precio = input("Ingrese el precio del producto: ")
    while not precio:
        precio = input("Ingrese el precio del producto: ")

    fecha_vencimiento = input("Ingrese la fecha de vencimiento: ")
    while not fecha_vencimiento:
        fecha_vencimiento = input("Ingrese la fecha de vencimiento: ")

    registro = Producto(codigo, nombre, marca, proveedor, cantidad, tamanio, precio, fecha_vencimiento)
    if registro.registrar():
        print("Producto registrado exitosamente")
    else:
        print("Producto no registrado")


def menuProductos():
    while True:
        print("---Menu de productos---")
        print("1. Registrar")
        print("2. Detalles")
        print("3. Salir")
        opcion = input("Ingrese opcion: ")
        if opcion == "1":
            registrarProducto()
        elif opcion == "2":
            Producto.detalles()
        elif opcion == "3":
            break

menuProductos()